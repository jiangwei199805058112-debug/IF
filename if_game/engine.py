from __future__ import annotations

from typing import Any, Callable

from .event_loader import load_day_flow, load_sample_characters, load_seed_events
from .models import CharacterProfile, MemoryEntry, OutcomeDelta, PerceivedRelationshipState, RelationshipState


DIRECTION_VALUES = {
    "none": 0,
    "slight_up": 1,
    "medium_up": 2,
    "large_up": 3,
    "slight_down": -1,
    "medium_down": -2,
    "large_down": -3,
    "crisis_trigger": -4,
    "conditional": 0,
}

LEVEL_VALUES = {"low": -1, "medium": 0, "high": 1}

FEEDBACK_TEXT = {
    "stable": "关系还算稳定。",
    "slight_unease": "你有一点不安，但还不能确定原因。",
    "obvious_abnormal": "这件事让你明显感觉不对。",
    "strong_suspicion": "你开始强烈怀疑对方没有说完整。",
    "relationship_crisis": "这已经接近关系危机。",
}

ENTRY_STAGE = {
    "chatting": "正在聊天",
    "ambiguous": "暧昧中",
    "new_relationship": "刚恋爱",
    "正在聊天": "正在聊天",
    "暧昧中": "暧昧中",
    "刚恋爱": "刚恋爱",
}


def _clamp(value: int, low: int = -10, high: int = 10) -> int:
    return max(low, min(high, value))


def _direction_value(name: str) -> int:
    return DIRECTION_VALUES.get(name, 0)


def _level_value(name: str) -> int:
    return LEVEL_VALUES.get(name, 0)


def _event_map(events: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if "events" in events:
        return {event["event_id"]: event for event in events["events"]}
    return events


def _branch_map(event: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {branch["branch_id"]: branch for branch in event.get("branches", [])}


def _choice_map(event: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for choice in event.get("choices", []):
        result[str(choice.get("id", ""))] = choice
        result[str(choice.get("tag", ""))] = choice
        result[str(choice.get("label", ""))] = choice
    return result


def initialize_relationship(entry_mode: str, profile_pair: dict[str, Any]) -> RelationshipState:
    player = CharacterProfile.from_dict(profile_pair["player"])
    npc = CharacterProfile.from_dict(profile_pair["npc"])
    stage = ENTRY_STAGE.get(entry_mode, "暧昧中")

    base_trust = _level_value(player.personality.trust_baseline) + _level_value(npc.personality.trust_baseline)
    base_security = -_level_value(player.personality.security_need)
    base_pressure = 1 if "忙" in npc.work_status or "加班" in npc.work_status else 0

    state = RelationshipState(
        day=1,
        stage=stage,
        trust=base_trust,
        security=base_security,
        pressure=base_pressure,
        profile_pair_id=str(profile_pair.get("id", "")),
        pair_title=str(profile_pair.get("title", "")),
        player=player,
        npc=npc,
    )
    state.transcript.append(f"开局：{stage}。样例组合：{state.pair_title}。")
    state.transcript.append(f"玩家：{player.display_name}；NPC：{npc.display_name}。")
    return state


def _apply_delta(state: RelationshipState, delta: OutcomeDelta) -> None:
    state.trust = _clamp(state.trust + _direction_value(delta.trust))
    state.security = _clamp(state.security + _direction_value(delta.security))
    state.pressure = _clamp(state.pressure + _direction_value(delta.pressure))
    state.conflict = _clamp(state.conflict + _direction_value(delta.conflict))
    state.disappointment = _clamp(state.disappointment + _direction_value(delta.disappointment))
    state.flaw = _clamp(state.flaw + _direction_value(delta.flaw))
    if delta.crisis and "crisis" not in state.active_hooks:
        state.active_hooks.append("crisis")


def apply_event_branch(
    state: RelationshipState,
    event: dict[str, Any],
    branch: dict[str, Any],
    choice_tag: str,
) -> PerceivedRelationshipState:
    state.triggered_events.append(event["event_id"])
    event_delta = OutcomeDelta.from_dict(branch.get("outcome_delta"))
    _apply_delta(state, event_delta)

    choice = _choice_map(event).get(choice_tag, {})
    choice_delta = OutcomeDelta.from_dict(choice.get("outcome_delta"))
    _apply_delta(state, choice_delta)

    for hook in branch.get("next_hooks", []):
        if hook not in state.active_hooks:
            state.active_hooks.append(str(hook))

    feedback = generate_perceived_feedback(state, event, branch)
    maybe_write_memory(state, event, branch)
    return feedback


def generate_perceived_feedback(
    state: RelationshipState,
    event: dict[str, Any] | None = None,
    branch: dict[str, Any] | None = None,
) -> PerceivedRelationshipState:
    if branch:
        feedback_data = branch.get("perceived_feedback", {})
        level = str(feedback_data.get("level", "slight_unease"))
        summary = str(feedback_data.get("text", FEEDBACK_TEXT.get(level, FEEDBACK_TEXT["slight_unease"])))
    else:
        if "crisis" in state.active_hooks:
            level = "relationship_crisis"
        elif state.flaw >= 4:
            level = "strong_suspicion"
        elif state.conflict >= 3 or state.disappointment >= 3:
            level = "obvious_abnormal"
        elif state.pressure >= 2 or state.security <= -2:
            level = "slight_unease"
        else:
            level = "stable"
        summary = FEEDBACK_TEXT[level]

    state.perceived = PerceivedRelationshipState(level, summary)
    return state.perceived


def maybe_write_memory(state: RelationshipState, event: dict[str, Any], branch: dict[str, Any]) -> None:
    memory_data = branch.get("memory", {})
    if not memory_data.get("write", False):
        return
    entry = MemoryEntry(
        day=state.day,
        event_id=str(event["event_id"]),
        branch_id=str(branch["branch_id"]),
        summary=str(memory_data.get("summary", event["title"])),
        resolved=bool(memory_data.get("resolved", False)),
    )
    state.memory_entries.append(entry)
    state.transcript.append(f"记忆账本：{entry.summary}")


def resolve_stage(state: RelationshipState) -> str:
    has_lash_out = any(("拉黑" in entry.summary or "冷战" in entry.summary) for entry in state.memory_entries)
    has_repair = any(("修复" in entry.summary or "说清" in entry.summary) and entry.resolved for entry in state.memory_entries)

    if state.trust <= -8 and state.disappointment >= 7:
        return "分手"
    if state.trust <= -5 and has_lash_out:
        return "分分合合倾向"
    if "crisis" in state.active_hooks or (state.trust <= -5 and state.conflict >= 4):
        return "分手危机"
    if state.conflict >= 4 or state.disappointment >= 4:
        return "冷淡"
    if has_repair and state.trust >= 1 and state.conflict <= 2:
        return "确认关系" if state.stage == "暧昧中" else "升温"
    if state.trust >= 2 and state.security >= -1 and len(state.memory_entries) <= 1:
        return "升温"
    return "继续暧昧"


def _select_interactive(
    prompt_title: str,
    items: list[dict[str, Any]],
    label_key: str,
    input_func: Callable[[str], str],
) -> dict[str, Any]:
    lines = [prompt_title]
    for index, item in enumerate(items, start=1):
        lines.append(f"{index}. {item.get(label_key, item.get('id', ''))}")
    raw = input_func("\n".join(lines) + "\n直接回车使用第 1 项：").strip()
    if not raw:
        return items[0]
    try:
        choice_index = int(raw) - 1
    except ValueError:
        choice_index = 0
    if 0 <= choice_index < len(items):
        return items[choice_index]
    return items[0]


def run_day(
    state: RelationshipState,
    day_config: dict[str, Any],
    events: dict[str, Any],
    scripted_choices: dict[str, Any] | None = None,
    interactive: bool = False,
    input_func: Callable[[str], str] = input,
) -> None:
    state.day = int(day_config["day"])
    state.transcript.append("")
    state.transcript.append(f"第 {state.day} 天：{day_config['default_rhythm']}")
    notes = day_config.get("notes")
    if notes:
        state.transcript.append(f"日程提示：{notes}")

    if day_config.get("midpoint_feedback"):
        feedback = generate_perceived_feedback(state)
        state.transcript.append(f"第 7 天中期反馈：{feedback.visible_summary}")

    event_id = day_config.get("event_id")
    if not event_id:
        return

    event = _event_map(events)[event_id]
    state.transcript.append(f"事件：{event['title']}")
    state.transcript.append(str(event.get("description", "")))

    script = (scripted_choices or {}).get(event_id, {})
    branch_id = script.get("branch_id") or day_config.get("default_branch_id")
    choice_tag = script.get("choice_tag") or day_config.get("default_choice_tag")

    branch_lookup = _branch_map(event)
    branch = branch_lookup.get(branch_id) or event.get("branches", [])[0]

    choices = event.get("choices", [])
    if interactive:
        prompt = "\n".join(
            [
                f"事件：{event['title']}",
                f"你看到：{branch.get('visible_info', '')}",
                f"对方解释：{branch.get('npc_explanation', '')}",
                "选择你的处理方式：",
            ]
        )
        selected_choice = _select_interactive(prompt, choices, "label", input_func)
        choice_tag = str(selected_choice.get("id", selected_choice.get("tag", "")))
    elif not choice_tag and choices:
        choice_tag = str(choices[0].get("id", choices[0].get("tag", "")))

    state.transcript.append(f"你看到：{branch.get('visible_info', '')}")
    state.transcript.append(f"对方解释：{branch.get('npc_explanation', '')}")
    if choice_tag:
        choice = _choice_map(event).get(choice_tag, {})
        state.transcript.append(f"你的选择：{choice.get('label', choice_tag)}")

    feedback = apply_event_branch(state, event, branch, str(choice_tag or ""))
    state.transcript.append(f"感知反馈：{feedback.visible_summary}")


def run_14_day_simulation(
    entry_mode: str,
    profile_pair_id: str,
    scripted_choices: dict[str, Any] | None = None,
    interactive: bool = False,
    input_func: Callable[[str], str] = input,
) -> dict[str, Any]:
    profiles = load_sample_characters()
    events = load_seed_events()
    day_flow = load_day_flow()

    pairs = profiles.get("pairs", {})
    if profile_pair_id not in pairs:
        raise KeyError(f"Unknown profile pair: {profile_pair_id}")

    state = initialize_relationship(entry_mode, pairs[profile_pair_id])
    for day_config in day_flow:
        run_day(state, day_config, events, scripted_choices, interactive, input_func)

    final_stage = resolve_stage(state)
    state.stage = final_stage
    final_feedback = generate_perceived_feedback(state)
    visible_summary = f"第 14 天阶段结算：{final_stage}。{final_feedback.visible_summary}"
    state.transcript.append("")
    state.transcript.append(visible_summary)
    if state.memory_entries:
        state.transcript.append("本轮留下的记忆：")
        for entry in state.memory_entries:
            state.transcript.append(f"- 第 {entry.day} 天：{entry.summary}")
    else:
        state.transcript.append("本轮没有写入重大记忆。")

    return {
        "final_stage": final_stage,
        "visible_summary": visible_summary,
        "memory_count": len(state.memory_entries),
        "triggered_events": list(dict.fromkeys(state.triggered_events)),
        "transcript": state.transcript,
    }

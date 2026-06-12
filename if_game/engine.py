from __future__ import annotations

from typing import Any, Callable

from .daily_actions import (
    derive_atmosphere_after_event,
    format_aftershock_context,
    format_daily_action_result,
    format_daily_status_header,
    format_midpoint_feedback,
    get_daily_actions,
    resolve_daily_action,
)
from .event_loader import load_day_flow, load_playtest_scenarios, load_sample_characters, load_seed_events
from .models import (
    CharacterProfile,
    MemoryEntry,
    OutcomeDelta,
    PerceivedRelationshipState,
    RelationshipReview,
    RelationshipState,
)
from .relationship_flow_integration import (
    apply_relationship_delta_to_state,
    build_aggregator_input_from_event,
    format_relationship_delta_summary,
)
from .questionnaire.initial_modifiers import format_initial_modifier_summary
from .relationship_state_aggregator import aggregate_relationship_event


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

ENTRY_GOALS = {
    "chatting": "正在聊天：看能否稳定聊天并进入暧昧。",
    "ambiguous": "暧昧中：看能否确认关系或明确边界。",
    "new_relationship": "刚恋爱：看能否处理早期不安和磨合。",
    "正在聊天": "正在聊天：看能否稳定聊天并进入暧昧。",
    "暧昧中": "暧昧中：看能否确认关系或明确边界。",
    "刚恋爱": "刚恋爱：看能否处理早期不安和磨合。",
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


def emit_interactive_lines(lines: list[str], interactive: bool) -> None:
    if not interactive:
        return
    for line in lines:
        print(line)


def _emit_new_transcript_lines(
    state: RelationshipState,
    start_index: int,
    interactive: bool,
) -> int:
    emit_interactive_lines(state.transcript[start_index:], interactive)
    return len(state.transcript)


def _pause_for_next_day(
    day: int,
    interactive: bool,
    input_func: Callable[[str], str],
) -> None:
    if not interactive or day >= 14:
        return
    emit_interactive_lines(["按回车继续。"], True)
    input_func("")


def initialize_relationship(
    entry_mode: str,
    profile_pair: dict[str, Any],
    relationship_config: dict[str, Any] | None = None,
) -> RelationshipState:
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
    state.transcript.append(f"开局：{stage}。")
    for line in _format_relationship_config_lines(state.pair_title, relationship_config):
        state.transcript.append(line)
    state.transcript.append(f"玩家：{player.display_name}；NPC：{npc.display_name}。")
    state.transcript.append("本轮目标：")
    state.transcript.append("- 在 14 天内判断这段关系是否值得继续推进。")
    state.transcript.append("- 你可以选择靠近、观察、谈边界、修复冲突或主动降温。")
    state.transcript.append(f"- {ENTRY_GOALS.get(entry_mode, ENTRY_GOALS['ambiguous'])}")
    return state


def _format_relationship_config_lines(
    pair_title: str,
    relationship_config: dict[str, Any] | None,
) -> list[str]:
    config = relationship_config or {
        "setup_method": "快速预设组合",
        "quick_preset_title": pair_title,
        "player_tendency": "由快速预设决定",
        "npc_tendency": "由快速预设决定",
        "conflict_theme": "由快速预设决定",
    }

    setup_method = str(config.get("setup_method", "关系配置"))
    lines = [f"关系配置：{setup_method}。"]
    if setup_method == "快速预设组合":
        lines.append(f"快速预设：{config.get('quick_preset_title', pair_title)}。")

    player_tendency = str(config.get("player_tendency", "")).strip()
    npc_tendency = str(config.get("npc_tendency", "")).strip()
    conflict_theme = str(config.get("conflict_theme", "")).strip()
    if player_tendency:
        lines.append(f"玩家倾向：{player_tendency}。")
    if npc_tendency:
        lines.append(f"NPC 倾向：{npc_tendency}。")
    if conflict_theme:
        lines.append(f"主要矛盾：{conflict_theme}。")
    return lines


def _initial_modifier_summary(initial_modifiers: dict[str, Any] | None) -> list[str]:
    if not initial_modifiers:
        return []
    summary = initial_modifiers.get("initial_modifier_summary")
    if isinstance(summary, list):
        return [line for line in summary if isinstance(line, str) and line]
    return format_initial_modifier_summary(initial_modifiers)


def _append_initial_modifier_summary(
    state: RelationshipState,
    initial_modifiers: dict[str, Any] | None,
) -> list[str]:
    summary = _initial_modifier_summary(initial_modifiers)
    if not summary:
        return []

    state.transcript.append("本局开局倾向：")
    for line in summary:
        state.transcript.append(f"- {line}")
    return summary


def _apply_delta(state: RelationshipState, delta: OutcomeDelta) -> None:
    state.trust = _clamp(state.trust + _direction_value(delta.trust))
    state.security = _clamp(state.security + _direction_value(delta.security))
    state.pressure = _clamp(state.pressure + _direction_value(delta.pressure))
    state.conflict = _clamp(state.conflict + _direction_value(delta.conflict))
    state.disappointment = _clamp(state.disappointment + _direction_value(delta.disappointment))
    state.flaw = _clamp(state.flaw + _direction_value(delta.flaw))
    if delta.crisis and "crisis" not in state.active_hooks:
        state.active_hooks.append("crisis")


def _effective_branch_for_choice(
    event: dict[str, Any],
    branch: dict[str, Any],
    choice_tag: str,
) -> dict[str, Any]:
    if event.get("event_id") != "CONFLICT_001":
        return branch
    if str(branch.get("branch_id", "")) not in {"CONFLICT_001_C", "CONFLICT_001_E"}:
        return branch

    if choice_tag == "private_talk":
        return _branch_with_overrides(
            branch,
            branch_id="CONFLICT_001_PRIVATE_TALK",
            truth="约定私下复盘",
            visible_info="你们都还带着情绪，但没有把话停在沉默里。",
            npc_explanation="我现在还有点乱，但我们可以晚点私下把这件事说清。",
            behavior_tags=["私下沟通", "修复尝试"],
            outcome_delta={
                "pressure": "slight_up",
                "conflict": "slight_down",
                "disappointment": "slight_down",
            },
            perceived_feedback={
                "level": "slight_unease",
                "text": "问题没有立刻解决，但修复窗口还在，关键是之后能不能继续说清楚。",
            },
            memory={
                "write": True,
                "summary": "冲突后约定私下复盘，修复窗口仍然打开",
                "resolved": False,
            },
            next_hooks=["private_repair"],
        )

    if choice_tag == "apologize_boundary":
        return _branch_with_overrides(
            branch,
            branch_id="CONFLICT_001_APOLOGY_BOUNDARY",
            truth="当晚说清楚并承认影响",
            visible_info="你们把最伤人的部分先停下来，重新说具体问题。",
            npc_explanation="这次我也有做得不好的地方，我们把下次怎么做说清楚。",
            behavior_tags=["道歉", "设边界", "修复尝试"],
            outcome_delta={
                "trust": "slight_up",
                "security": "slight_up",
                "pressure": "slight_down",
                "conflict": "medium_down",
                "disappointment": "slight_down",
            },
            perceived_feedback={
                "level": "stable",
                "text": "这次冲突仍有重量，但回应更像修复，而不是冷处理。",
            },
            memory={
                "write": True,
                "summary": "冲突后承认影响并约定下次做法",
                "resolved": True,
            },
            next_hooks=["repair_success", "private_repair"],
        )

    if choice_tag == "reconnect_or_break":
        return _branch_with_overrides(
            branch,
            branch_id="CONFLICT_001_RECONNECT_TALK",
            truth="把是否继续摆到台面上",
            visible_info="你们没有假装没事，而是开始谈这段关系还能不能继续。",
            npc_explanation="如果还要继续，我们不能每次都这样耗着；不行也要说清楚。",
            behavior_tags=["复联谈判", "关系去留"],
            outcome_delta={
                "security": "slight_down",
                "pressure": "medium_up",
                "conflict": "slight_up",
            },
            perceived_feedback={
                "level": "obvious_abnormal",
                "text": "这不像普通修复，更像把关系去留推到台面上。",
            },
            memory={
                "write": True,
                "summary": "冲突后把继续与否摆到台面上",
                "resolved": False,
            },
            next_hooks=["reconnect_talk"],
        )

    return branch


def _branch_with_overrides(branch: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    effective = dict(branch)
    for key, value in overrides.items():
        if isinstance(value, dict):
            effective[key] = dict(value)
        elif isinstance(value, list):
            effective[key] = list(value)
        else:
            effective[key] = value
    return effective


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
    _record_event_resolution(state, event, branch, choice, choice_tag)

    for hook in branch.get("next_hooks", []):
        if hook not in state.active_hooks:
            state.active_hooks.append(str(hook))

    feedback = generate_perceived_feedback(state, event, branch)
    maybe_write_memory(state, event, branch)
    aggregator_input = build_aggregator_input_from_event(
        event,
        {
            "branch": branch,
            "choice": choice,
            "choice_tag": choice_tag,
            "day": state.day,
        },
    )
    relationship_delta = aggregate_relationship_event(aggregator_input)
    apply_relationship_delta_to_state(state, relationship_delta)
    summaries = format_relationship_delta_summary(relationship_delta)
    if summaries:
        state.transcript.append("关系状态变化：")
        for summary in summaries:
            state.transcript.append(f"- {summary}")
    state.atmosphere_tag = derive_atmosphere_after_event(
        str(event.get("event_id", "")),
        str(branch.get("branch_id", "")),
        str(choice_tag),
        state.atmosphere_tag,
    )
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


def _append_unique(values: list[str], value: str) -> None:
    if value and value not in values:
        values.append(value)


def _append_daily_header(state: RelationshipState, entry_mode: str) -> None:
    atmosphere = str(getattr(state, "atmosphere_tag", "stable"))
    state.atmosphere_history.append({"day": state.day, "atmosphere_tag": atmosphere})
    for line in format_daily_status_header(state.day, entry_mode, atmosphere):
        state.transcript.append(line)


def _scripted_daily_action_key(scripted_choices: dict[str, Any] | None, day: int) -> str | None:
    if not scripted_choices:
        return None
    daily_actions = scripted_choices.get("daily_actions", {})
    if not isinstance(daily_actions, dict):
        return None
    value = daily_actions.get(day, daily_actions.get(str(day)))
    return str(value) if value else None


def _apply_daily_relationship_delta(state: RelationshipState, delta: dict[str, Any]) -> None:
    for field in ("trust", "security", "pressure", "conflict", "disappointment", "flaw"):
        if field not in delta:
            continue
        try:
            value = int(delta[field])
        except (TypeError, ValueError):
            value = 0
        if value:
            setattr(state, field, _clamp(int(getattr(state, field)) + value))


def _append_daily_action_history(
    state: RelationshipState,
    day: int,
    action_key: str,
    result: dict[str, Any],
) -> None:
    state.daily_action_history.append(
        {
            "day": day,
            "action_key": action_key,
            "action_label": str(result.get("action_label", "")),
            "atmosphere_tag": str(result.get("atmosphere_tag", "")),
            "context_tags": list(result.get("context_tags", [])),
        }
    )


def _record_event_resolution(
    state: RelationshipState,
    event: dict[str, Any],
    branch: dict[str, Any],
    choice: dict[str, Any],
    choice_tag: str,
) -> None:
    state.event_resolution_log.append(
        {
            "day": state.day,
            "event_id": str(event.get("event_id", "")),
            "event_title": str(event.get("title", "")),
            "branch_id": str(branch.get("branch_id", "")),
            "choice_tag": str(choice_tag),
            "choice_label": str(choice.get("label", choice_tag)),
            "memory_summary": str(branch.get("memory", {}).get("summary", "")),
        }
    )


def _has_memory(state: RelationshipState, keywords: tuple[str, ...]) -> bool:
    return any(any(keyword in entry.summary for keyword in keywords) for entry in state.memory_entries)


def _has_major_crisis_memory(state: RelationshipState) -> bool:
    return _has_memory(state, ("重大谎言暴露", "前任见面被隐瞒", "情绪性拉黑"))


def _has_resolved_repair(state: RelationshipState) -> bool:
    return any(("修复" in entry.summary or "说清楚" in entry.summary) and entry.resolved for entry in state.memory_entries)


def resolve_stage(state: RelationshipState) -> str:
    has_lash_out = any(("拉黑" in entry.summary or "冷战" in entry.summary) for entry in state.memory_entries)
    has_repair = _has_resolved_repair(state)
    has_ambiguous_cooling = state.stage == "暧昧中" and _has_memory(
        state, ("解释敷衍", "异性朋友饭局没有提前说清", "冷战")
    )

    if "crisis" in state.active_hooks and _has_major_crisis_memory(state):
        return "分手危机"
    if state.trust <= -8 and state.disappointment >= 7:
        return "分手"
    if "crisis" in state.active_hooks:
        return "分手危机"
    if has_ambiguous_cooling and (has_lash_out or state.conflict >= 3 or state.disappointment >= 3):
        return "暧昧降温"
    if state.trust <= -5 and state.conflict >= 4:
        return "分手危机"
    if state.trust <= -5 and has_lash_out:
        return "分分合合倾向"
    if state.conflict >= 4 or state.disappointment >= 4:
        return "冷淡"
    if has_repair and state.trust >= 1 and state.conflict <= 2:
        return "确认关系" if state.stage == "暧昧中" else "升温"
    if state.trust >= 2 and state.security >= -1 and len(state.memory_entries) <= 1:
        return "升温"
    return "继续暧昧"


def _build_sub_tags(state: RelationshipState) -> list[str]:
    tags: list[str] = []
    hooks = set(state.active_hooks)

    if _has_resolved_repair(state) or "repair_success" in hooks:
        _append_unique(tags, "有效修复")
    if _has_memory(state, ("重大谎言暴露",)):
        _append_unique(tags, "重大谎言")
    if _has_memory(state, ("异性社交信息被含糊带过", "前任见面被隐瞒", "重大谎言暴露", "情绪性拉黑")):
        _append_unique(tags, "信任受损")
    if _has_memory(state, ("异性朋友饭局没有提前说清", "前任见面被隐瞒", "异性社交信息被含糊带过")) or (
        "boundary_talk" in hooks
    ):
        _append_unique(tags, "边界未清")
    if _has_memory(state, ("冷战", "拉黑")) or "cold_war" in hooks:
        _append_unique(tags, "冷处理循环")
    if _has_memory(state, ("拉黑",)) or "reconnect_talk" in hooks:
        _append_unique(tags, "分分合合倾向")
    if _has_memory(state, ("解释敷衍",)) or "reply_pattern_watch" in hooks:
        _append_unique(tags, "现实压力")
    if state.stage in {"暧昧降温", "分手危机"} and "reconnect_talk" in hooks:
        _append_unique(tags, "关系仍有吸引")

    return tags or ["关系仍需观察"]


def _build_turning_points(state: RelationshipState) -> list[str]:
    hooks = set(state.active_hooks)
    points: list[str] = []

    if "plain_day_repair" in hooks:
        points.append("第 3 天，对方消息延迟后主动解释，最初的信息缺口被补上。")
    if "reply_pattern_watch" in hooks:
        points.append("第 3 天，对方没有主动补充足够细节，不安开始累积。")
    if "trust_talk" in hooks:
        points.append("第 3 天，对象信息缺失，让后续信任谈判变得更重要。")
    if "plain_day" in hooks:
        points.append("第 8 天，异性饭局提前说明，边界没有完全靠猜。")
    if "boundary_talk" in hooks:
        points.append("第 8 天，异性朋友饭局没有提前说清，边界问题被放大。")
    if _has_memory(state, ("前任见面被隐瞒",)):
        points.append("第 8 天，前任见面的信息被省略，信任问题升级。")
    if _has_memory(state, ("重大谎言暴露",)):
        points.append("第 8 天，说法和时间线对不上，不安升级为关系危机。")
    if "repair_success" in hooks:
        points.append("第 12 天，冲突后双方愿意把问题摆到台面上。")
    if "private_repair" in hooks and "repair_success" not in hooks:
        points.append("第 12 天，冲突没有立刻解决，但双方留下了继续说清楚的修复窗口。")
    if "cold_war" in hooks:
        points.append("第 12 天，沉默替代沟通，冷处理成为关系转折点。")
    if "reconnect_talk" in hooks:
        points.append("第 12 天，情绪性拉黑切断联系，后续只能靠复联重新谈。")

    if not points:
        points.append("这 14 天没有出现单一爆点，关系主要由日常回应和边界感累积推动。")
    return points


def _build_risks(state: RelationshipState) -> list[str]:
    hooks = set(state.active_hooks)
    risks: list[str] = []

    if "reply_pattern_watch" in hooks:
        risks.append("回复模式可能继续引发猜测。")
    if "boundary_talk" in hooks or _has_memory(state, ("异性朋友饭局没有提前说清",)):
        risks.append("异性边界仍需要明确。")
    if "cold_war" in hooks:
        risks.append("冷处理可能成为固定冲突模式。")
    if "reply_slowdown" in hooks:
        risks.append("回复变慢会继续放大不安。")
    if "crisis" in hooks:
        risks.append("关系已经进入危机线，后续沟通容易变成分手谈话。")
    if "breakup_talk" in hooks:
        risks.append("被隐瞒的信息如果没有处理清楚，后续可能进入分手谈话。")
    if "reconnect_talk" in hooks:
        risks.append("复联如果只靠情绪拉回，仍可能反复。")

    if not risks:
        risks.append("当前没有明显危机，但稳定节奏仍需要继续维护。")
    return risks


def _build_repair_chances(state: RelationshipState) -> list[str]:
    hooks = set(state.active_hooks)
    chances: list[str] = []

    if "repair_success" in hooks:
        chances.append("保留这次当晚说清楚的沟通方式，后续冲突不要拖成冷战。")
    if "private_repair" in hooks and "repair_success" not in hooks:
        chances.append("把已经约好的私下复盘真正完成，不要让修复窗口重新变成沉默。")
    if "boundary_talk" in hooks:
        chances.append("把异性社交边界具体说清，包括提前说明、可接受频率和不舒服时怎么反馈。")
    if "reply_pattern_watch" in hooks:
        chances.append("建立忙碌时的补充说明习惯，减少靠猜测判断关系状态。")
    if "crisis" in hooks:
        chances.append("先处理隐瞒、撒谎或拉黑本身的责任，再谈是否继续。")
    if "reconnect_talk" in hooks:
        chances.append("复联时需要谈清楚下次冲突是否还会切断联系。")

    if not chances:
        chances.append("继续保持稳定联系，并在新的边界问题出现前提前说明。")
    return chances


def _build_summary(state: RelationshipState, sub_tags: list[str]) -> str:
    if state.stage in {"确认关系", "升温"} and "有效修复" in sub_tags:
        return "这 14 天里，你们遇到过消息延迟和边界确认，但多数问题都被及时解释或修复。"
    if state.stage == "暧昧降温":
        return "这 14 天里，关系没有直接断掉，但解释不足、边界未清和冷处理让暧昧热度明显下降。"
    if state.stage == "冷淡":
        return "互动还在继续，但回复、分享和修复意愿都变弱了，关系进入低温状态。"
    if state.stage == "分手危机":
        return "这 14 天里，隐瞒、谎言或拉黑把信任问题推到危机线，关系需要先处理原则性问题。"
    if state.stage == "分手":
        return "这 14 天里，信任和修复余量都被消耗到很低，关系已经接近结束。"
    if state.stage == "分分合合倾向":
        return "这 14 天里，吸引和不信任同时存在，冲突后又可能靠复联拉回，关系容易反复。"
    return "这 14 天里，关系仍在推进，但关键边界和联系节奏还没有完全说清。"


def build_relationship_review(state: RelationshipState) -> RelationshipReview:
    sub_tags = _build_sub_tags(state)
    main_reasons = [f"第 {entry.day} 天：{entry.summary}。" for entry in state.memory_entries]
    if not main_reasons:
        main_reasons = ["这轮没有留下重大旧账，关系变化主要来自日常回应和边界确认。"]

    return RelationshipReview(
        main_stage=state.stage,
        sub_tags=sub_tags,
        main_reasons=main_reasons,
        turning_points=_build_turning_points(state),
        risks=_build_risks(state),
        repair_chances=_build_repair_chances(state),
        summary=_build_summary(state, sub_tags),
    )


def _build_stage_reason_lines(state: RelationshipState, review: RelationshipReview) -> list[str]:
    lines = ["原因说明："]
    daily_line = _daily_behavior_reason(state)
    if daily_line:
        lines.append(f"- {daily_line}")

    key_line = _key_event_reason(state)
    if key_line:
        lines.append(f"- {key_line}")

    day12_line = _day12_reason(state)
    if day12_line:
        lines.append(f"- {day12_line}")

    lines.append(f"- {_final_stage_reason(state.stage)}")
    if len(lines) == 2 and review.summary:
        lines.insert(1, f"- {review.summary}")
    return lines


def _daily_behavior_reason(state: RelationshipState) -> str:
    active_count = 0
    cold_count = 0
    for item in state.daily_action_history:
        tags = {str(tag) for tag in item.get("context_tags", [])}
        if tags.intersection({"warm_action", "repair_action", "stable_action", "advance_action", "disclosure_action"}):
            active_count += 1
        if "cold_action" in tags:
            cold_count += 1

    if active_count >= 4 and active_count >= cold_count:
        return "你们仍保持联系，主要是因为你多次选择主动沟通维持了联系。"
    if cold_count >= 3 and cold_count > active_count:
        return "多次等待、观察或拉开距离，说明主动性下降导致关系降温。"
    if active_count:
        return "普通日里仍有一些主动回应，避免关系只被关键事件定义。"
    return ""


def _key_event_reason(state: RelationshipState) -> str:
    entries_by_day = {entry.day: entry.summary for entry in state.memory_entries if entry.day in {3, 8, 12}}
    ordered = [(day, entries_by_day[day]) for day in (3, 8, 12) if day in entries_by_day]
    if len(ordered) >= 2:
        joined = "、".join(f"第 {day} 天的“{summary}”" for day, summary in ordered[:3])
        return f"{joined}共同影响了最终关系走向。"
    if len(ordered) == 1:
        day, summary = ordered[0]
        return f"第 {day} 天的{summary}是这轮关系变化的主要节点之一。"
    return ""


def _day12_reason(state: RelationshipState) -> str:
    conflict_log = next(
        (item for item in state.event_resolution_log if item.get("event_id") == "CONFLICT_001"),
        None,
    )
    if not conflict_log:
        return ""

    branch_id = str(conflict_log.get("branch_id", ""))
    choice_tag = str(conflict_log.get("choice_tag", ""))
    hooks = set(state.active_hooks)
    if branch_id in {"CONFLICT_001_PRIVATE_TALK", "CONFLICT_001_APOLOGY_BOUNDARY", "CONFLICT_001_A"} or (
        choice_tag in {"private_talk", "apologize_boundary"} and "cold_war" not in hooks
    ):
        return "第 12 天的修复选择避免关系继续降温，让关系仍保留继续说清楚的空间。"
    if branch_id == "CONFLICT_001_C" or choice_tag == "cold" or "cold_war" in hooks:
        return "第 12 天问题停在沉默里导致降温，未解决冲突被记成后续旧账。"
    if branch_id == "CONFLICT_001_D" or "reconnect_talk" in hooks:
        return "第 12 天连接被切断后只能靠复联重谈，关系因此更接近危机。"
    return ""


def _final_stage_reason(final_stage: str) -> str:
    if final_stage in {"确认关系", "升温"}:
        return f"因为关键问题后仍有回应和修复动作，所以结算偏向{final_stage}。"
    if final_stage == "继续暧昧":
        return "这些问题没有把关系推入危机，但也不足以稳定升温，所以停在继续暧昧。"
    if final_stage in {"暧昧降温", "冷淡"}:
        return f"多个未收尾问题叠加，让关系热度下降到{final_stage}。"
    if final_stage in {"分手危机", "分手"}:
        return f"信任损伤、冲突或连接中断已经压过日常维持，所以结算进入{final_stage}。"
    if final_stage == "分分合合倾向":
        return "吸引和不信任同时存在，关系更容易进入反复拉扯。"
    return f"综合日常互动和关键事件后，关系停在{final_stage}。"


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
    initial_modifiers: dict[str, Any] | None = None,
) -> None:
    state.day = int(day_config["day"])
    day_start_index = len(state.transcript)
    state.transcript.append("")
    state.transcript.append(f"第 {state.day} 天：{day_config['default_rhythm']}")
    _append_daily_header(state, state.stage)
    notes = day_config.get("notes")
    if notes:
        state.transcript.append(f"日程提示：{notes}")

    event_id = day_config.get("event_id")
    if not event_id:
        if not day_config.get("stage_settlement"):
            for line in format_aftershock_context(state.day, state.event_resolution_log):
                state.transcript.append(line)

            result_start_index = _emit_new_transcript_lines(state, day_start_index, interactive)
            actions = get_daily_actions(
                state.day,
                state.stage,
                state.profile_pair_id,
                state.atmosphere_tag,
                context_tags=list(state.active_hooks),
            )
            scripted_action_key = _scripted_daily_action_key(scripted_choices, state.day)
            selected_action = actions[0]
            if scripted_action_key:
                selected_action = next(
                    (action for action in actions if action["action_key"] == scripted_action_key),
                    selected_action,
                )
            if interactive:
                selected_action = _select_interactive("选择今天的行动：", actions, "label", input_func)

            action_key = str(selected_action.get("action_key", ""))
            action_result = resolve_daily_action(
                action_key,
                state.day,
                state.stage,
                state.profile_pair_id,
                state.atmosphere_tag,
                state,
                initial_modifiers=initial_modifiers,
            )
            _apply_daily_relationship_delta(state, dict(action_result.get("relationship_delta", {})))
            state.atmosphere_tag = str(action_result.get("atmosphere_tag", state.atmosphere_tag))
            for line in format_daily_action_result(action_result):
                state.transcript.append(line)
            _append_daily_action_history(state, state.day, action_key, action_result)

        if day_config.get("midpoint_feedback"):
            for line in format_midpoint_feedback(state.atmosphere_tag, state.daily_action_history):
                state.transcript.append(line)
        _emit_new_transcript_lines(state, result_start_index if not day_config.get("stage_settlement") else day_start_index, interactive)
        _pause_for_next_day(state.day, interactive, input_func)
        return

    event = _event_map(events)[event_id]
    state.transcript.append(f"事件：{event['title']}")
    state.transcript.append(str(event.get("description", "")))

    script = (scripted_choices or {}).get(event_id, {})
    branch_id = script.get("branch_id") or day_config.get("default_branch_id")
    choice_tag = script.get("choice_tag") or day_config.get("default_choice_tag")

    branch_lookup = _branch_map(event)
    branch = branch_lookup.get(branch_id) or event.get("branches", [])[0]

    result_start_index = _emit_new_transcript_lines(state, day_start_index, interactive)
    choices = event.get("choices", [])
    if interactive:
        prompt = "\n".join(
            [
                f"你看到：{branch.get('visible_info', '')}",
                f"对方解释：{branch.get('npc_explanation', '')}",
                "选择你的处理方式：",
            ]
        )
        selected_choice = _select_interactive(prompt, choices, "label", input_func)
        choice_tag = str(selected_choice.get("id", selected_choice.get("tag", "")))
    elif not choice_tag and choices:
        choice_tag = str(choices[0].get("id", choices[0].get("tag", "")))

    branch = _effective_branch_for_choice(event, branch, str(choice_tag or ""))
    state.transcript.append(f"你看到：{branch.get('visible_info', '')}")
    state.transcript.append(f"对方解释：{branch.get('npc_explanation', '')}")
    if choice_tag:
        choice = _choice_map(event).get(choice_tag, {})
        state.transcript.append(f"你的选择：{choice.get('label', choice_tag)}")

    feedback = apply_event_branch(state, event, branch, str(choice_tag or ""))
    state.transcript.append(f"感知反馈：{feedback.visible_summary}")
    _emit_new_transcript_lines(state, result_start_index, interactive)
    _pause_for_next_day(state.day, interactive, input_func)


def run_14_day_simulation(
    entry_mode: str,
    profile_pair_id: str,
    scripted_choices: dict[str, Any] | None = None,
    interactive: bool = False,
    input_func: Callable[[str], str] = input,
    initial_modifiers: dict[str, Any] | None = None,
    relationship_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    profiles = load_sample_characters()
    events = load_seed_events()
    day_flow = load_day_flow()

    pairs = profiles.get("pairs", {})
    if profile_pair_id not in pairs:
        raise KeyError(f"Unknown profile pair: {profile_pair_id}")

    state = initialize_relationship(entry_mode, pairs[profile_pair_id], relationship_config)
    initial_modifier_summary = _append_initial_modifier_summary(state, initial_modifiers)
    _emit_new_transcript_lines(state, 0, interactive)
    for day_config in day_flow:
        run_day(state, day_config, events, scripted_choices, interactive, input_func, initial_modifiers)

    final_stage = resolve_stage(state)
    state.stage = final_stage
    final_feedback = generate_perceived_feedback(state)
    review = build_relationship_review(state)
    visible_summary = f"第 14 天阶段结算：{final_stage}。{final_feedback.visible_summary}"
    final_start_index = len(state.transcript)
    state.transcript.append("")
    state.transcript.append(visible_summary)
    for line in _build_stage_reason_lines(state, review):
        state.transcript.append(line)
    if state.memory_entries:
        state.transcript.append("本轮留下的记忆：")
        for entry in state.memory_entries:
            state.transcript.append(f"- 第 {entry.day} 天：{entry.summary}")
    else:
        state.transcript.append("本轮没有写入重大记忆。")
    _emit_new_transcript_lines(state, final_start_index, interactive)

    return {
        "final_stage": final_stage,
        "visible_summary": visible_summary,
        "memory_count": len(state.memory_entries),
        "memory_summaries": [entry.summary for entry in state.memory_entries],
        "relationship_aggregator_log": list(getattr(state, "relationship_aggregator_log", [])),
        "relationship_delta_summaries": list(getattr(state, "relationship_delta_summaries", [])),
        "initial_modifiers": dict(initial_modifiers or {}),
        "initial_modifier_summary": list(initial_modifier_summary),
        "relationship_config": dict(relationship_config or {}),
        "daily_action_history": list(state.daily_action_history),
        "atmosphere_history": list(state.atmosphere_history),
        "event_resolution_log": list(state.event_resolution_log),
        "triggered_events": list(dict.fromkeys(state.triggered_events)),
        "feedback_level": final_feedback.feedback_level,
        "active_hooks": list(dict.fromkeys(state.active_hooks)),
        "review": review.to_dict(),
        "transcript": state.transcript,
    }


def run_playtest_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    result = run_14_day_simulation(
        str(scenario["entry_mode"]),
        str(scenario["profile_pair_id"]),
        scripted_choices=scenario.get("scripted_choices"),
    )
    result["scenario_id"] = str(scenario["id"])
    result["scenario_title"] = str(scenario["title"])
    result["scenario_description"] = str(scenario.get("description", ""))
    return result


def run_all_playtest_scenarios() -> list[dict[str, Any]]:
    scenario_data = load_playtest_scenarios()
    return [run_playtest_scenario(scenario) for scenario in scenario_data.get("scenarios", [])]

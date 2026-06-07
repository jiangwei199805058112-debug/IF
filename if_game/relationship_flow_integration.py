from __future__ import annotations

from typing import Any, Mapping

from .relationship_state_aggregator import RelationshipStateDelta


DIRECTION_LEVELS = {
    "none": 0,
    "conditional": 0,
    "slight_up": 2,
    "medium_up": 5,
    "large_up": 8,
    "slight_down": -2,
    "medium_down": -5,
    "large_down": -8,
    "crisis_trigger": -10,
}

EVENT_TYPE_BY_ID = {
    "MSG_001": "message_delay",
    "SOC_001": "privacy_boundary",
    "CONFLICT_001": "conflict_repair",
}

PATTERN_KEY_BY_EVENT = {
    "MSG_001": "late_reply_inconsistency",
    "SOC_001": "privacy_boundary_conflict",
    "CONFLICT_001": "stonewalling_after_conflict",
}

STATE_DELTA_FIELDS = (
    "trust_delta",
    "satisfaction_delta",
    "intimacy_delta",
    "stability_delta",
    "repair_chance_delta",
    "old_wound_memory_delta",
    "safety_delta",
    "excitement_delta",
    "fairness_delta",
    "dependence_delta",
)


def build_aggregator_input_from_event(
    event: Mapping[str, Any],
    choice: Mapping[str, Any] | str | None = None,
) -> dict[str, Any]:
    """Build a compact aggregator input from the current 14-day event shape.

    The 14-day prototype uses seed-event branches and choice outcome deltas, not
    the newer relationship-system fields. This adapter keeps that old shape
    intact and derives only a small, conservative aggregator input.
    """

    payload = _mapping(choice)
    branch = _mapping(
        payload.get("branch")
        or payload.get("selected_branch")
        or payload.get("branch_data")
    )
    selected_choice = _mapping(payload.get("choice") or payload.get("selected_choice"))
    choice_tag = _choice_tag(choice, payload, selected_choice)

    event_id = str(event.get("event_id", ""))
    branch_id = str(branch.get("branch_id", payload.get("branch_id", "")))
    truth_text = str(branch.get("truth", ""))
    behavior_tags = [str(tag) for tag in branch.get("behavior_tags", [])]

    branch_delta = _mapping(branch.get("outcome_delta"))
    choice_delta = _mapping(selected_choice.get("outcome_delta"))
    merged_delta = _merge_outcome_deltas(branch_delta, choice_delta)

    result: dict[str, Any] = {
        "event_id": event_id,
        "event_type": str(event.get("event_type", EVENT_TYPE_BY_ID.get(event_id, "relationship_event"))),
        "source_id": str(event.get("source_id", "npc_a")),
        "target_id": str(event.get("target_id", "player")),
        "day": payload.get("day", event.get("day", 0)),
        "pattern_key": PATTERN_KEY_BY_EVENT.get(event_id, event_id),
        "truth_harm_level": 0,
        "deception_level": 0,
        "evidence_chain_strength": 0,
        "relationship_rewards_delta": 0,
        "relationship_costs_delta": 0,
    }

    _apply_truth_mapping(result, event_id, branch_id, truth_text, behavior_tags)
    _apply_outcome_delta_mapping(result, merged_delta)
    _apply_choice_mapping(result, choice_tag)
    return result


def apply_relationship_delta_to_state(
    state: dict[str, Any] | Any,
    delta: RelationshipStateDelta,
) -> dict[str, Any] | Any:
    """Attach aggregator output to a state object without changing old scoring."""

    summaries = format_relationship_delta_summary(delta)
    log_entry = {
        "source_id": delta.source_id,
        "target_id": delta.target_id,
        **{field: getattr(delta, field) for field in STATE_DELTA_FIELDS},
        "report_tags": list(delta.report_tags),
        "memory_notes": list(delta.memory_notes),
        "summaries": list(summaries),
    }

    if isinstance(state, dict):
        state.setdefault("relationship_aggregator_log", []).append(log_entry)
        state.setdefault("relationship_delta_summaries", []).extend(summaries)
        return state

    aggregator_log = list(getattr(state, "relationship_aggregator_log", []))
    aggregator_log.append(log_entry)
    setattr(state, "relationship_aggregator_log", aggregator_log)

    delta_summaries = list(getattr(state, "relationship_delta_summaries", []))
    delta_summaries.extend(summaries)
    setattr(state, "relationship_delta_summaries", delta_summaries)
    return state


def format_relationship_delta_summary(delta: RelationshipStateDelta) -> list[str]:
    """Format player-facing relationship delta summaries without hidden truth."""

    lines: list[str] = []

    if delta.trust_delta <= -6:
        lines.append("本次事件明显削弱了信任。")
    elif delta.trust_delta < 0:
        lines.append("本次事件轻微影响了信任。")
    elif delta.trust_delta > 0:
        lines.append("这次互动让信任略有回升。")

    if delta.repair_chance_delta >= 4:
        lines.append("修复尝试提高了后续把问题说开的机会。")
    elif delta.repair_chance_delta < 0:
        lines.append("这次回应让后续修复难度上升。")

    if delta.old_wound_memory_delta > 0:
        lines.append("这件事可能会被记成之后关系里的旧账。")

    if delta.satisfaction_delta < 0 and len(lines) < 3:
        lines.append("关系满意度在这次互动后有所下降。")
    elif delta.satisfaction_delta > 0 and len(lines) < 3:
        lines.append("这次互动让关系体验稍微变好。")

    if delta.intimacy_delta > 0 and len(lines) < 3:
        lines.append("被回应和被理解的感觉有所增加。")
    elif delta.intimacy_delta < 0 and len(lines) < 3:
        lines.append("这次互动让亲近感变弱了一些。")

    if "privacy_boundary_conflict" in delta.report_tags and len(lines) < 4:
        lines.append("这更像边界没有说清，不直接等同于欺骗。")
    if "stonewalling_pattern" in delta.report_tags and len(lines) < 4:
        lines.append("沉默没有回到问题本身，容易变成冷处理模式。")
    if "repair_window_open" in delta.report_tags and len(lines) < 4:
        lines.append("这次仍然留下了继续修复的窗口。")
    if "safe_but_bored_pattern" in delta.report_tags and len(lines) < 4:
        lines.append("关系更安全，但不代表一定更有新鲜感。")
    if "risk_excitement_pattern" in delta.report_tags and len(lines) < 4:
        lines.append("这次有吸引力，也伴随着更高的不稳定感。")

    if not lines:
        lines.append("这次更像短期波动，暂时没有写成重大旧账。")
    return _unique(lines[:4])


def _apply_truth_mapping(
    result: dict[str, Any],
    event_id: str,
    branch_id: str,
    truth_text: str,
    behavior_tags: list[str],
) -> None:
    text = truth_text + " " + " ".join(behavior_tags)

    if "完全撒谎" in text or "重大谎言" in text or "撒谎" in text:
        result.update(
            truth_type="concealment",
            truth_harm_level=9,
            deception_level=9,
            evidence_chain_strength="strong",
            interpretation_type="suspicion",
            interpretation_accuracy="accurate_alertness",
            pattern_key="deleted_or_hidden_digital_trace",
        )
    elif "前任" in text and "隐瞒" in text:
        result.update(
            truth_type="concealment",
            truth_harm_level=8,
            deception_level=8,
            evidence_chain_strength="strong",
            interpretation_type="suspicion",
            interpretation_accuracy="accurate_alertness",
            pattern_key="hidden_contact_or_ex",
        )
    elif "隐瞒" in text or "隐瞒重点" in text:
        result.update(
            truth_type="concealment",
            truth_harm_level=7,
            deception_level=6,
            evidence_chain_strength="moderate",
            interpretation_type="suspicion",
            interpretation_accuracy="accurate_alertness",
            pattern_key="hidden_contact_or_ex",
        )
    elif "半真半假" in text:
        result.update(
            truth_type="boundary_blur",
            truth_harm_level=5,
            deception_level=4,
            evidence_chain_strength="moderate",
            privacy_boundary_conflict=5,
            pattern_key="privacy_boundary_conflict",
        )
    elif "冷战" in text or branch_id == "CONFLICT_001_C":
        result.update(
            truth_type="avoidance",
            truth_harm_level=4,
            conflict_response_type="stonewalling",
            conflict_escalation_risk=6,
            stonewalling_level=7,
            pattern_key="stonewalling_after_conflict",
        )
    elif "拉黑" in text or branch_id == "CONFLICT_001_D":
        result.update(
            truth_type="conflict_attack",
            truth_harm_level=8,
            conflict_response_type="exit_threat",
            conflict_escalation_risk=9,
            stonewalling_level=9,
            pattern_key="exit_threat_pattern",
        )
    elif "公共场合" in text:
        result.update(
            truth_type="conflict_attack",
            truth_harm_level=6,
            conflict_escalation_risk=8,
            pattern_key="public_conflict",
        )
    elif "当晚说清楚" in text or branch_id == "CONFLICT_001_A":
        result.update(
            truth_type="benign_reason",
            truth_harm_level=1,
            conflict_response_type="repair_attempt",
            validation_skill=7,
            active_listening_skill=6,
            repair_attempt_quality=8,
            perceived_responsiveness=7,
            pattern_key="conflict_repair_success",
        )
    elif "解释很敷衍" in text or "解释敷衍" in text:
        result.update(
            truth_type="busy",
            truth_harm_level=2,
            evidence_chain_strength="weak",
            perceived_responsiveness=2,
            pattern_key="late_reply_inconsistency",
        )
    elif "真忙" in text or "完全坦白" in text or "普通同事" in text:
        result.update(
            truth_type="busy" if event_id == "MSG_001" else "benign_reason",
            truth_harm_level=1,
            evidence_chain_strength="weak",
            perceived_responsiveness=6,
        )


def _apply_outcome_delta_mapping(result: dict[str, Any], merged_delta: Mapping[str, int]) -> None:
    trust = int(merged_delta.get("trust", 0))
    security = int(merged_delta.get("security", 0))
    pressure = int(merged_delta.get("pressure", 0))
    conflict = int(merged_delta.get("conflict", 0))
    disappointment = int(merged_delta.get("disappointment", 0))
    flaw = int(merged_delta.get("flaw", 0))

    if trust < 0:
        result["truth_harm_level"] = max(_num(result.get("truth_harm_level")), min(8, abs(trust)))
    elif trust > 0:
        result["relationship_rewards_delta"] = _num(result.get("relationship_rewards_delta")) + min(4, trust // 2)

    if security < 0:
        result["avoidance_cost_pressure_delta"] = max(_num(result.get("avoidance_cost_pressure_delta")), min(8, abs(security)))
    elif security > 0:
        result["relationship_safety_delta"] = _num(result.get("relationship_safety_delta")) + min(4, security // 2)

    if pressure > 0 or conflict > 0:
        result["conflict_escalation_risk"] = max(
            _num(result.get("conflict_escalation_risk")),
            min(9, pressure + conflict),
        )
    if conflict < 0:
        result["repair_attempt_quality"] = max(
            _num(result.get("repair_attempt_quality")),
            min(8, abs(conflict) + 2),
        )

    if disappointment > 0:
        result["relationship_costs_delta"] = _num(result.get("relationship_costs_delta")) + min(8, disappointment)
    elif disappointment < 0:
        result["relationship_rewards_delta"] = _num(result.get("relationship_rewards_delta")) + min(4, abs(disappointment) // 2)

    if flaw > 0:
        result["evidence_chain_strength"] = max(
            _num(result.get("evidence_chain_strength")),
            min(8, flaw + 2),
        )


def _apply_choice_mapping(result: dict[str, Any], choice_tag: str) -> None:
    if choice_tag in {"accept", "接受解释"}:
        result["relationship_rewards_delta"] = _num(result.get("relationship_rewards_delta")) + 1
    elif choice_tag in {"ask_softly", "温和确认", "private_talk", "私下沟通"}:
        result["validation_skill"] = max(_num(result.get("validation_skill")), 5)
        result["repair_attempt_quality"] = max(_num(result.get("repair_attempt_quality")), 4)
    elif choice_tag in {"set_boundary", "设边界", "apologize_boundary", "道歉并设边界"}:
        result["validation_skill"] = max(_num(result.get("validation_skill")), 6)
        result["repair_attempt_quality"] = max(_num(result.get("repair_attempt_quality")), 6)
    elif choice_tag in {"push_hard", "强硬质问", "verify", "查证"}:
        result["conflict_escalation_risk"] = max(_num(result.get("conflict_escalation_risk")), 6)
    elif choice_tag in {"cool_down", "cold", "冷处理"}:
        result["stonewalling_level"] = max(_num(result.get("stonewalling_level")), 5)
        result["conflict_escalation_risk"] = max(_num(result.get("conflict_escalation_risk")), 5)
    elif choice_tag in {"reconnect_or_break", "复联/分手"}:
        result["repair_status"] = "partially_repaired"
        result["repair_attempt_quality"] = max(_num(result.get("repair_attempt_quality")), 4)


def _merge_outcome_deltas(
    branch_delta: Mapping[str, Any],
    choice_delta: Mapping[str, Any],
) -> dict[str, int]:
    keys = {"trust", "security", "pressure", "conflict", "disappointment", "flaw"}
    return {
        key: _direction_value(branch_delta.get(key)) + _direction_value(choice_delta.get(key))
        for key in keys
    }


def _choice_tag(
    choice: Mapping[str, Any] | str | None,
    payload: Mapping[str, Any],
    selected_choice: Mapping[str, Any],
) -> str:
    if isinstance(choice, str):
        return choice
    return str(
        payload.get("choice_tag")
        or selected_choice.get("id")
        or selected_choice.get("tag")
        or selected_choice.get("label")
        or ""
    )


def _direction_value(value: Any) -> int:
    return DIRECTION_LEVELS.get(str(value), 0)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _num(value: Any) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        if isinstance(value, str):
            return {"weak": 2, "low": 2, "moderate": 5, "medium": 5, "strong": 8, "high": 8}.get(value, 0)
        return 0


def _unique(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result

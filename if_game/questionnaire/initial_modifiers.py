from __future__ import annotations

from typing import Any, Mapping


MODIFIER_DELTA_FIELDS = (
    "trust_baseline_delta",
    "intimacy_need_delta",
    "conflict_repair_tendency_delta",
    "privacy_boundary_sensitivity_delta",
    "reassurance_need_delta",
    "suspicion_sensitivity_delta",
    "disclosure_willingness_delta",
)

STATE_FIELD_BY_DELTA = {
    "trust_baseline_delta": "trust_baseline",
    "intimacy_need_delta": "intimacy_need",
    "conflict_repair_tendency_delta": "conflict_repair_tendency",
    "privacy_boundary_sensitivity_delta": "privacy_boundary_sensitivity",
    "reassurance_need_delta": "reassurance_need",
    "suspicion_sensitivity_delta": "suspicion_sensitivity",
    "disclosure_willingness_delta": "disclosure_willingness",
}


def build_initial_relationship_modifiers(score_result: dict[str, Any]) -> dict[str, Any]:
    """Convert questionnaire scores into bounded initial gameplay tendencies.

    Questionnaire results are only opening assumptions. Runtime behavior should
    keep overriding these values as relationship events accumulate.
    """

    dimension_scores = _mapping(score_result.get("dimension_scores"))
    evidence_count = _mapping(score_result.get("evidence_count"))
    completion_rate = _completion_rate(score_result, bool(dimension_scores))

    modifiers = {
        "trust_baseline_delta": _modifier_delta(
            dimension_scores,
            evidence_count,
            completion_rate,
            {"trust_baseline": 1.0},
        ),
        "intimacy_need_delta": _modifier_delta(
            dimension_scores,
            evidence_count,
            completion_rate,
            {
                "attachment_closeness_need": 1.0,
                "desire_emotional_validation_hunger": 0.4,
            },
        ),
        "conflict_repair_tendency_delta": _modifier_delta(
            dimension_scores,
            evidence_count,
            completion_rate,
            {
                "communication_repair_initiative": 1.0,
                "communication_apology_capacity": 0.7,
                "attachment_repair_receptivity": 0.6,
                "communication_directness": 0.4,
            },
        ),
        "privacy_boundary_sensitivity_delta": _modifier_delta(
            dimension_scores,
            evidence_count,
            completion_rate,
            {
                "digital_phone_privacy_need": 1.0,
                "attachment_independence_need": 0.8,
                "trust_privacy_trust": 0.4,
            },
        ),
        "reassurance_need_delta": _modifier_delta(
            dimension_scores,
            evidence_count,
            completion_rate,
            {
                "emotion_reassurance_need": 1.0,
                "attachment_abandonment_anxiety": 0.7,
                "desire_emotional_validation_hunger": 0.5,
            },
        ),
        "suspicion_sensitivity_delta": _modifier_delta(
            dimension_scores,
            evidence_count,
            completion_rate,
            {
                "trust_suspicion_sensitivity": 1.0,
                "trust_checking_impulse": 0.5,
                "trust_old_wound_memory": 0.4,
                "trust_baseline": -0.4,
            },
        ),
        "disclosure_willingness_delta": _modifier_delta(
            dimension_scores,
            evidence_count,
            completion_rate,
            {
                "attachment_vulnerability_fear": -1.0,
                "self_acceptance": 0.7,
                "communication_directness": 0.8,
            },
        ),
    }
    modifiers["initial_report_tags"] = _initial_report_tags(modifiers, completion_rate)
    modifiers["debug_reasons"] = _debug_reasons(modifiers, completion_rate, dimension_scores)
    return modifiers


def apply_initial_modifiers(
    base_state: dict[str, Any] | Mapping[str, Any] | None,
    modifiers: dict[str, Any],
) -> dict[str, Any]:
    """Return a shallow state copy with initial questionnaire deltas applied."""

    state = dict(base_state or {})
    for delta_field, state_field in STATE_FIELD_BY_DELTA.items():
        delta = _number(modifiers.get(delta_field, 0))
        current = _number(state.get(state_field, 0))
        state[state_field] = _bounded_int(current + delta, limit=10)

    existing_tags = state.get("initial_report_tags", [])
    state["initial_report_tags"] = _unique(
        [*_list_of_strings(existing_tags), *_list_of_strings(modifiers.get("initial_report_tags", []))]
    )
    state["questionnaire_initial_modifiers"] = {
        field: int(modifiers.get(field, 0)) for field in MODIFIER_DELTA_FIELDS
    }
    return state


def format_initial_modifier_summary(modifiers: dict[str, Any]) -> list[str]:
    """Format player-facing initial modifier summaries without diagnostic claims."""

    lines: list[str] = []

    _append_direction(
        lines,
        int(modifiers.get("trust_baseline_delta", 0)),
        "开局会更容易先相信合理解释。",
        "开局会保留更多观察空间。",
    )
    _append_direction(
        lines,
        int(modifiers.get("reassurance_need_delta", 0)),
        "遇到不确定回应时，开局更需要明确安抚和说明。",
        "遇到不确定回应时，开局更能先靠自己稳定判断。",
    )
    _append_direction(
        lines,
        int(modifiers.get("suspicion_sensitivity_delta", 0)),
        "细节异常会更早进入观察范围。",
        "细节异常通常不会立刻推高怀疑。",
    )
    _append_direction(
        lines,
        int(modifiers.get("privacy_boundary_sensitivity_delta", 0)),
        "手机、私人信息和个人空间边界会更早影响相处感受。",
        "开局对信息透明和个人空间的边界压力较低。",
    )
    _append_direction(
        lines,
        int(modifiers.get("conflict_repair_tendency_delta", 0)),
        "冲突后更容易留下继续说清楚的窗口。",
        "冲突后需要更具体的外部推动，才更容易回到修复。",
    )
    _append_direction(
        lines,
        int(modifiers.get("disclosure_willingness_delta", 0)),
        "开局更容易把真实需要和脆弱内容说出来。",
        "开局更可能先保留真实需要，等关系更安全再说。",
    )

    if not lines:
        lines.append("当前问卷只提供轻量开局参考，暂不明显调整关系倾向。")

    lines.append("这些只是开局倾向，后续关键事件和重复行为会继续修正。")
    return _unique(lines)


def _modifier_delta(
    dimension_scores: Mapping[str, Any],
    evidence_count: Mapping[str, Any],
    completion_rate: float,
    weights: Mapping[str, float],
) -> int:
    weighted_total = 0.0
    weight_total = 0.0
    touched_evidence = 0
    missing_all = True

    for dimension, weight in weights.items():
        if dimension in dimension_scores:
            missing_all = False
        score = _score(dimension_scores.get(dimension, 50))
        weighted_total += ((score - 50.0) / 10.0) * weight
        weight_total += abs(weight)
        touched_evidence += max(0, int(_number(evidence_count.get(dimension, 0))))

    if weight_total <= 0 or missing_all:
        return 0

    evidence_factor = _evidence_factor(touched_evidence, evidence_count)
    raw_delta = (weighted_total / weight_total) * _completion_factor(completion_rate) * evidence_factor
    return _bounded_int(round(raw_delta), limit=10)


def _completion_rate(score_result: dict[str, Any], has_scores: bool) -> float:
    if "completion_rate" in score_result:
        return max(0.0, min(1.0, _number(score_result.get("completion_rate", 0.0))))
    return 1.0 if has_scores else 0.0


def _completion_factor(completion_rate: float) -> float:
    if completion_rate <= 0:
        return 0.0
    if completion_rate < 0.25:
        return 0.25
    if completion_rate < 0.5:
        return 0.5
    if completion_rate < 0.7:
        return 0.75
    return 1.0


def _evidence_factor(touched_evidence: int, evidence_count: Mapping[str, Any]) -> float:
    if not evidence_count:
        return 1.0
    if touched_evidence <= 0:
        return 0.0
    if touched_evidence == 1:
        return 0.55
    if touched_evidence == 2:
        return 0.75
    return 1.0


def _initial_report_tags(modifiers: Mapping[str, Any], completion_rate: float) -> list[str]:
    tags: list[str] = []
    if completion_rate < 0.25:
        tags.append("low_completion_initial_profile")
    _tag_if(tags, modifiers, "suspicion_sensitivity_delta", "suspicion_under_ambiguity")
    _tag_if(tags, modifiers, "reassurance_need_delta", "high_reassurance_need")
    _tag_if(tags, modifiers, "conflict_repair_tendency_delta", "repair_capable_initial_tendency")
    _tag_if(tags, modifiers, "privacy_boundary_sensitivity_delta", "privacy_boundary_sensitive")
    _tag_if(tags, modifiers, "disclosure_willingness_delta", "open_disclosure_initial_tendency")
    if int(modifiers.get("disclosure_willingness_delta", 0)) <= -3:
        tags.append("guarded_disclosure_initial_tendency")
    return _unique(tags)


def _tag_if(tags: list[str], modifiers: Mapping[str, Any], field: str, tag: str) -> None:
    if int(modifiers.get(field, 0)) >= 3:
        tags.append(tag)


def _debug_reasons(
    modifiers: Mapping[str, Any],
    completion_rate: float,
    dimension_scores: Mapping[str, Any],
) -> list[str]:
    changed = [
        f"{field}={int(modifiers.get(field, 0))}"
        for field in MODIFIER_DELTA_FIELDS
        if int(modifiers.get(field, 0)) != 0
    ]
    if not changed:
        changed.append("no strong initial modifier")
    return [
        f"completion_rate={round(completion_rate, 4)}",
        f"dimension_count={len(dimension_scores)}",
        ", ".join(changed),
        "questionnaire modifiers are initial tendencies and can be overridden by gameplay behavior",
    ]


def _append_direction(lines: list[str], delta: int, positive: str, negative: str) -> None:
    if delta >= 2:
        lines.append(positive)
    elif delta <= -2:
        lines.append(negative)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _list_of_strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def _score(value: Any) -> float:
    return max(0.0, min(100.0, _number(value, default=50.0)))


def _number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _bounded_int(value: float, limit: int) -> int:
    return int(max(-limit, min(limit, value)))


def _unique(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result

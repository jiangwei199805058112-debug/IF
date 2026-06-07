from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


REAL_PROBLEM_TRUTH_TYPES = {
    "neglect",
    "avoidance",
    "concealment",
    "betrayal",
    "manipulation",
}

SUSPECT_JUDGMENTS = {
    "suspect",
    "suspect_problem",
    "suspicious",
    "怀疑",
    "怀疑有问题",
}

TRUST_JUDGMENTS = {
    "trust",
    "trust_no_problem",
    "believe",
    "相信",
    "相信没问题",
}

TRACE_WEIGHTS = {
    "online_but_no_reply": 8,
    "social_media_updated_but_no_reply": 14,
    "message_seen_but_ignored": 12,
    "selective_availability": 14,
    "late_night_implausible_call": 10,
    "explanation_timing_conflict": 16,
    "deleted_chat_trace": 22,
    "third_party_witness": 22,
    "payment_or_location_trace": 20,
}

DECEPTION_TRUTH_TYPES = {
    "concealment",
    "betrayal",
    "manipulation",
}

PRIVACY_TRUTH_TYPES = {
    "privacy_boundary",
    "private_space",
    "habit_cleanup",
}

NO_PHONE_TRACE_CONFLICTS = {
    "online_but_no_reply",
    "social_media_updated_but_no_reply",
    "message_seen_but_ignored",
    "selective_availability",
}


@dataclass(frozen=True)
class TruthLayer:
    truth_type: str = "busy"
    truth_reason: str = ""
    truth_intention: str = ""
    truth_harm_level: float = 0.0
    truth_priority_signal: float = 0.0
    truth_moral_severity: float = 0.0

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any] | None) -> "TruthLayer":
        data = data or {}
        return cls(
            truth_type=str(data.get("truth_type", "busy")),
            truth_reason=str(data.get("truth_reason", "")),
            truth_intention=str(data.get("truth_intention", "")),
            truth_harm_level=_clamp_number(data.get("truth_harm_level", 0)),
            truth_priority_signal=_clamp_number(data.get("truth_priority_signal", 0)),
            truth_moral_severity=_clamp_number(data.get("truth_moral_severity", 0)),
        )

    @property
    def has_real_problem(self) -> bool:
        return (
            self.truth_type in REAL_PROBLEM_TRUTH_TYPES
            or self.truth_harm_level >= 45
            or self.truth_priority_signal >= 60
            or self.truth_moral_severity >= 45
        )


@dataclass(frozen=True)
class ExplanationLayer:
    explanation_claim: str = ""
    explanation_specificity: float = 50.0
    explanation_consistency: float = 50.0
    explanation_plausibility: float = 50.0
    behavior_explanation_gap: float = 0.0
    excuse_repetition_count: int = 0
    supporting_evidence_strength: float = 0.0

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any] | None) -> "ExplanationLayer":
        data = data or {}
        return cls(
            explanation_claim=str(data.get("explanation_claim", "")),
            explanation_specificity=_clamp_number(data.get("explanation_specificity", 50)),
            explanation_consistency=_clamp_number(data.get("explanation_consistency", 50)),
            explanation_plausibility=_clamp_number(data.get("explanation_plausibility", 50)),
            behavior_explanation_gap=_clamp_number(data.get("behavior_explanation_gap", 0)),
            excuse_repetition_count=max(0, int(data.get("excuse_repetition_count", 0))),
            supporting_evidence_strength=_clamp_number(
                data.get("supporting_evidence_strength", data.get("supporting_evidence", 0))
            ),
        )


@dataclass(frozen=True)
class ObservableTraces:
    traces: dict[str, bool]

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any] | None) -> "ObservableTraces":
        data = data or {}
        return cls({name: bool(data.get(name, False)) for name in TRACE_WEIGHTS})

    @property
    def active(self) -> list[str]:
        return [name for name, enabled in self.traces.items() if enabled]


def interpret_relationship_event(event: Mapping[str, Any]) -> dict[str, Any]:
    """Evaluate one relationship event against truth, explanation, and evidence layers."""

    truth = TruthLayer.from_mapping(_mapping(event.get("truth")))
    explanation = ExplanationLayer.from_mapping(_mapping(event.get("explanation")))
    traces = ObservableTraces.from_mapping(_mapping(event.get("observable_traces")))
    player_judgment = _normalize_judgment(event.get("player_judgment", "trust_no_problem"))

    adjusted_gap = _adjusted_behavior_gap(explanation, traces)
    evidence_chain_strength = _evidence_chain_strength(explanation, traces, adjusted_gap)
    explanation_credibility = _explanation_credibility(explanation, adjusted_gap)
    quadrant = _quadrant(player_judgment, truth.has_real_problem)
    trust_calibration = _trust_calibration(
        quadrant["type"],
        evidence_chain_strength,
        explanation_credibility,
    )
    relationship_effects = _relationship_effects(
        truth,
        explanation,
        adjusted_gap,
        evidence_chain_strength,
        explanation_credibility,
        quadrant["type"],
    )
    report_tags = _report_tags(
        truth,
        explanation,
        traces,
        evidence_chain_strength,
        explanation_credibility,
        quadrant["type"],
    )

    return {
        "event_id": str(event.get("event_id", "")),
        "truth_layer": {
            "truth_type": truth.truth_type,
            "truth_reason": truth.truth_reason,
            "truth_intention": truth.truth_intention,
            "truth_harm_level": truth.truth_harm_level,
            "truth_priority_signal": truth.truth_priority_signal,
            "truth_moral_severity": truth.truth_moral_severity,
            "has_real_problem": truth.has_real_problem,
        },
        "explanation_layer": {
            "explanation_claim": explanation.explanation_claim,
            "explanation_specificity": explanation.explanation_specificity,
            "explanation_consistency": explanation.explanation_consistency,
            "explanation_plausibility": explanation.explanation_plausibility,
            "behavior_explanation_gap": adjusted_gap,
            "excuse_repetition_count": explanation.excuse_repetition_count,
            "explanation_credibility": explanation_credibility,
        },
        "observable_traces": traces.active,
        "evidence_chain_strength": evidence_chain_strength,
        "interpretation_accuracy": quadrant["type"],
        "trust_calibration": trust_calibration,
        "quadrant": quadrant,
        "relationship_effects": relationship_effects,
        "report_tags": report_tags,
        "npc_reaction": _npc_reaction(quadrant["type"], evidence_chain_strength, explanation_credibility),
    }


def interpretation_to_aggregator_input(
    result: dict[str, Any],
    source_id: str = "",
    target_id: str = "",
) -> dict[str, Any]:
    """Convert an interpretation result into relationship_state_aggregator input.

    The interpretation layer uses 0-100 scores, while the aggregator prototype
    expects compact 0-10 levels. This adapter keeps the old interpretation result
    intact and only emits the fields the aggregator can already consume.
    """

    truth_layer = _mapping(result.get("truth_layer"))
    explanation_layer = _mapping(result.get("explanation_layer"))
    relationship_effects = _mapping(result.get("relationship_effects"))
    report_tags = result.get("report_tags", [])
    quadrant = _mapping(result.get("quadrant"))

    truth_type = str(truth_layer.get("truth_type", ""))
    interpretation_accuracy = str(
        result.get("interpretation_accuracy", quadrant.get("type", "unknown"))
    )

    evidence_chain_strength = _scale_100_to_10(result.get("evidence_chain_strength", 0))
    truth_harm_level = _scale_100_to_10(truth_layer.get("truth_harm_level", 0))
    deception_level = _deception_level_for_aggregator(
        truth_type,
        truth_layer,
        explanation_layer,
        evidence_chain_strength,
    )

    return {
        "source_id": source_id,
        "target_id": target_id,
        "truth_type": truth_type,
        "truth_harm_level": truth_harm_level,
        "deception_level": deception_level,
        "evidence_chain_strength": evidence_chain_strength,
        "interpretation_type": _interpretation_type_for_aggregator(interpretation_accuracy),
        "interpretation_accuracy": interpretation_accuracy,
        "privacy_boundary_conflict": _privacy_boundary_conflict_for_aggregator(
            truth_type,
            truth_layer,
            report_tags,
        ),
        "projection_bias_effect": 7 if interpretation_accuracy == "over_suspicion" else 0,
        "threat_bias_effect": 7 if interpretation_accuracy == "over_suspicion" else 0,
        "selective_blindness_effect": 7 if interpretation_accuracy == "misplaced_trust" else 0,
        "conflict_escalation_risk": _scale_100_to_10(
            relationship_effects.get("conflict_escalation", 0)
        ),
        "pattern_key": str(result.get("event_id", "")),
        "occurrence_count": _occurrence_count_for_aggregator(explanation_layer),
    }


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _clamp_number(value: Any, low: float = 0.0, high: float = 100.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = low
    return max(low, min(high, number))


def _clamp_delta(value: float) -> float:
    return max(-100.0, min(100.0, value))


def _scale_100_to_10(value: Any) -> float:
    return round(_clamp_number(value) / 10, 2)


def _deception_level_for_aggregator(
    truth_type: str,
    truth_layer: Mapping[str, Any],
    explanation_layer: Mapping[str, Any],
    evidence_chain_strength: float,
) -> float:
    if truth_type not in DECEPTION_TRUTH_TYPES:
        return 0.0

    moral_severity = _scale_100_to_10(truth_layer.get("truth_moral_severity", 0))
    credibility_deficit = _scale_100_to_10(
        100 - _clamp_number(explanation_layer.get("explanation_credibility", 100))
    )
    return round(max(moral_severity, evidence_chain_strength, credibility_deficit), 2)


def _privacy_boundary_conflict_for_aggregator(
    truth_type: str,
    truth_layer: Mapping[str, Any],
    report_tags: Any,
) -> float:
    tags = report_tags if isinstance(report_tags, list) else []
    if truth_type in PRIVACY_TRUTH_TYPES or "privacy_boundary_conflict" in tags:
        return max(2.0, _scale_100_to_10(truth_layer.get("truth_harm_level", 0)))
    return 0.0


def _interpretation_type_for_aggregator(interpretation_accuracy: str) -> str:
    if interpretation_accuracy in {"accurate_alertness", "over_suspicion"}:
        return "suspicion"
    if interpretation_accuracy == "stable_trust":
        return "benign_interpretation"
    if interpretation_accuracy == "misplaced_trust":
        return "selective_blindness"
    return "unknown"


def _occurrence_count_for_aggregator(explanation_layer: Mapping[str, Any]) -> int:
    try:
        repetition = int(explanation_layer.get("excuse_repetition_count", 0))
    except (TypeError, ValueError):
        repetition = 0
    return max(0, repetition)


def _normalize_judgment(value: Any) -> str:
    if isinstance(value, bool):
        return "suspect_problem" if value else "trust_no_problem"

    normalized = str(value).strip()
    if normalized in SUSPECT_JUDGMENTS:
        return "suspect_problem"
    if normalized in TRUST_JUDGMENTS:
        return "trust_no_problem"
    return "trust_no_problem"


def _adjusted_behavior_gap(explanation: ExplanationLayer, traces: ObservableTraces) -> float:
    gap = explanation.behavior_explanation_gap
    claim = explanation.explanation_claim

    if any(token in claim for token in ("没看手机", "没看", "手机没电", "没拿手机")):
        for trace_name in NO_PHONE_TRACE_CONFLICTS:
            if traces.traces.get(trace_name, False):
                gap += 10

    if traces.traces.get("late_night_implausible_call", False) and any(
        token in claim for token in ("妈妈", "家人", "家里")
    ):
        gap += 6

    gap += min(explanation.excuse_repetition_count * 5, 20)
    return _clamp_number(gap)


def _evidence_chain_strength(
    explanation: ExplanationLayer,
    traces: ObservableTraces,
    adjusted_gap: float,
) -> float:
    trace_score = sum(weight for name, weight in TRACE_WEIGHTS.items() if traces.traces.get(name, False))
    repetition_score = min(explanation.excuse_repetition_count * 6, 24)
    score = trace_score + adjusted_gap * 0.25 + repetition_score
    return round(_clamp_number(score), 2)


def _explanation_credibility(explanation: ExplanationLayer, adjusted_gap: float) -> float:
    base = (
        explanation.explanation_specificity
        + explanation.explanation_consistency
        + explanation.explanation_plausibility
    ) / 3
    penalty = adjusted_gap * 0.45 + min(explanation.excuse_repetition_count * 5, 25)
    support = explanation.supporting_evidence_strength * 0.25
    return round(_clamp_number(base + support - penalty), 2)


def _quadrant(player_judgment: str, has_real_problem: bool) -> dict[str, str]:
    suspects_problem = player_judgment == "suspect_problem"

    if suspects_problem and has_real_problem:
        return {
            "judgment": "怀疑有问题",
            "fact": "真的有问题",
            "type": "accurate_alertness",
            "label": "准确警觉",
            "game_consequence": "可以触发证据链和事实揭露",
        }
    if suspects_problem and not has_real_problem:
        return {
            "judgment": "怀疑有问题",
            "fact": "实际没问题",
            "type": "over_suspicion",
            "label": "误会/焦虑",
            "game_consequence": "损害隐私信任和情绪安全",
        }
    if not suspects_problem and not has_real_problem:
        return {
            "judgment": "相信没问题",
            "fact": "实际没问题",
            "type": "stable_trust",
            "label": "稳定信任",
            "game_consequence": "关系稳定或轻微波动",
        }
    return {
        "judgment": "相信没问题",
        "fact": "真的有问题",
        "type": "misplaced_trust",
        "label": "被欺骗/低估风险",
        "game_consequence": "后续揭穿时伤害更大",
    }


def _trust_calibration(
    quadrant_type: str,
    evidence_chain_strength: float,
    explanation_credibility: float,
) -> float:
    if quadrant_type in {"accurate_alertness", "stable_trust"}:
        if quadrant_type == "accurate_alertness":
            score = 70 + evidence_chain_strength * 0.25
        else:
            score = 65 + explanation_credibility * 0.25
    elif quadrant_type == "misplaced_trust":
        score = 45 - evidence_chain_strength * 0.25
    else:
        score = 45 - explanation_credibility * 0.15
    return round(_clamp_number(score), 2)


def _relationship_effects(
    truth: TruthLayer,
    explanation: ExplanationLayer,
    adjusted_gap: float,
    evidence_chain_strength: float,
    explanation_credibility: float,
    quadrant_type: str,
) -> dict[str, float]:
    credibility_deficit = 100 - explanation_credibility
    repetition = explanation.excuse_repetition_count

    fact_trust = -truth.truth_harm_level * 0.18 - credibility_deficit * 0.08 - evidence_chain_strength * 0.06
    loyalty_multiplier = 1.0 if truth.truth_type in {"concealment", "betrayal", "manipulation"} else 0.45
    loyalty_trust = -truth.truth_moral_severity * 0.18 * loyalty_multiplier
    emotional_trust = -truth.truth_harm_level * 0.12 - truth.truth_priority_signal * 0.12
    priority_feeling = -truth.truth_priority_signal * 0.2 - adjusted_gap * 0.05
    old_wound_memory = truth.truth_harm_level * 0.1 + repetition * 3 + evidence_chain_strength * 0.04
    conflict_escalation = adjusted_gap * 0.1 + evidence_chain_strength * 0.08 + repetition * 2
    if quadrant_type == "over_suspicion":
        conflict_escalation += 8
    if quadrant_type == "misplaced_trust":
        old_wound_memory += 10

    repair_chance = 70 + explanation_credibility * 0.18 - truth.truth_harm_level * 0.35 - repetition * 4
    if truth.truth_type in {"busy", "neglect"} and explanation_credibility >= 60:
        repair_chance += 8
    if truth.truth_type in {"betrayal", "manipulation"}:
        repair_chance -= 15

    relationship_satisfaction = -truth.truth_harm_level * 0.16 - credibility_deficit * 0.06

    return {
        "fact_trust": round(_clamp_delta(fact_trust), 2),
        "loyalty_trust": round(_clamp_delta(loyalty_trust), 2),
        "emotional_trust": round(_clamp_delta(emotional_trust), 2),
        "priority_feeling": round(_clamp_delta(priority_feeling), 2),
        "old_wound_memory": round(_clamp_number(old_wound_memory), 2),
        "relationship_satisfaction": round(_clamp_delta(relationship_satisfaction), 2),
        "conflict_escalation": round(_clamp_number(conflict_escalation), 2),
        "repair_chance": round(_clamp_number(repair_chance), 2),
        "lie_evidence_chain": round(_clamp_number(evidence_chain_strength), 2),
    }


def _report_tags(
    truth: TruthLayer,
    explanation: ExplanationLayer,
    traces: ObservableTraces,
    evidence_chain_strength: float,
    explanation_credibility: float,
    quadrant_type: str,
) -> list[str]:
    tags = [quadrant_type]

    if evidence_chain_strength >= 45:
        tags.append("evidence_sensitive")
    if truth.truth_priority_signal >= 55 or traces.traces.get("selective_availability", False):
        tags.append("priority_neglect_sensitive")
    if explanation.excuse_repetition_count >= 2:
        tags.append("repeated_excuse_alert")
    if quadrant_type == "misplaced_trust" and evidence_chain_strength >= 45:
        tags.append("selective_blindness")
    if quadrant_type == "stable_trust" and explanation_credibility >= 65:
        tags.append("plausible_explanation_acceptor")
    if quadrant_type == "over_suspicion":
        tags.append("over_suspicion")
    if quadrant_type == "accurate_alertness":
        tags.append("accurate_alertness")

    return _unique(tags)


def _npc_reaction(quadrant_type: str, evidence_chain_strength: float, explanation_credibility: float) -> str:
    if quadrant_type == "accurate_alertness":
        return "解释和线索存在冲突，角色会更倾向要求细节、证据或后续一致行动。"
    if quadrant_type == "over_suspicion":
        return "如果继续追问，可能损害隐私信任；更适合先核对具体线索。"
    if quadrant_type == "misplaced_trust":
        return "当前相信可能低估风险；后续证据暴露时伤害会更大。"
    if evidence_chain_strength <= 20 and explanation_credibility >= 65:
        return "解释较具体且线索冲突少，关系可能保持稳定或轻微波动。"
    return "角色会继续观察解释、线索和后续行为是否一致。"


def _unique(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result

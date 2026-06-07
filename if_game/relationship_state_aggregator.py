from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping


LEVEL_SCORES = {
    "none": 0.0,
    "low": 2.0,
    "weak": 2.0,
    "minor": 2.0,
    "medium": 5.0,
    "moderate": 5.0,
    "high": 8.0,
    "strong": 8.0,
    "critical": 10.0,
    "conclusive": 10.0,
}

ACCURATE_ALERTNESS_VALUES = {"accurate_alertness", "accurate", "准确警觉"}
OVER_SUSPICION_VALUES = {"over_suspicion", "over_suspicion_pattern", "误会/焦虑"}
BENIGN_PRIVACY_TRUTH_TYPES = {"privacy_boundary", "private_space", "habit_cleanup"}
HARMFUL_TRUTH_TYPES = {"concealment", "betrayal", "boundary_blur", "identity_split"}


@dataclass(frozen=True)
class RelationshipStateDelta:
    source_id: str = ""
    target_id: str = ""
    trust_delta: int = 0
    satisfaction_delta: int = 0
    intimacy_delta: int = 0
    stability_delta: int = 0
    repair_chance_delta: int = 0
    old_wound_memory_delta: int = 0
    safety_delta: int = 0
    excitement_delta: int = 0
    fairness_delta: int = 0
    dependence_delta: int = 0
    report_tags: list[str] = field(default_factory=list)
    memory_notes: list[str] = field(default_factory=list)
    debug_reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def aggregate_relationship_event(event: Mapping[str, Any]) -> RelationshipStateDelta:
    """Aggregate one relationship event into a bounded, directional state delta.

    This prototype intentionally stays small. It centralizes high-level relationship
    effects so that truth/evidence, communication, conflict, and exchange rules do
    not all subtract trust independently for the same event.
    """

    source_id = str(event.get("source_id", event.get("actor_id", "")))
    target_id = str(event.get("target_id", ""))

    truth_type = str(event.get("truth_type", "")).strip()
    truth_harm = _score(event.get("truth_harm_level", 0))
    deception = _score(event.get("deception_level", 0))
    evidence = _score(event.get("evidence_chain_strength", 0))
    interpretation_type = str(event.get("interpretation_type", "")).strip()
    interpretation_accuracy = str(event.get("interpretation_accuracy", "unknown"))
    projection_bias = _score(event.get("projection_bias_effect", 0))
    threat_bias = _score(event.get("threat_bias_effect", 0))
    perceived_responsiveness = _score(event.get("perceived_responsiveness", 0))
    conflict_escalation = _score(event.get("conflict_escalation_risk", 0))
    active_listening = _score(event.get("active_listening_skill", 0))
    validation_skill = _score(event.get("validation_skill", 0))
    stonewalling = _score(event.get("stonewalling_level", 0))
    repair_quality = _score(event.get("repair_attempt_quality", 0))
    rewards_delta = _signed_score(event.get("relationship_rewards_delta", 0))
    costs_delta = _signed_score(event.get("relationship_costs_delta", 0))
    approach_reward = _signed_score(event.get("approach_reward_delta", 0))
    avoidance_pressure = _signed_score(event.get("avoidance_cost_pressure_delta", 0))
    direct_excitement = _signed_score(event.get("relationship_excitement_delta", 0))
    direct_safety = _signed_score(event.get("relationship_safety_delta", 0))
    boredom = _signed_score(event.get("boredom_delta", 0))
    perceived_equity = _signed_score(event.get("perceived_equity_delta", 0))
    underbenefit = _signed_score(event.get("underbenefit_feeling_delta", 0))
    overbenefit_guilt = _signed_score(event.get("overbenefit_guilt_delta", 0))
    felt_appreciation = _signed_score(event.get("felt_appreciation_delta", 0))
    taken_for_granted = _signed_score(event.get("taken_for_granted_delta", 0))
    privacy_conflict = _score(event.get("privacy_boundary_conflict", 0))
    occurrence_count = max(0, int(_score(event.get("occurrence_count", 0), high=100)))
    repair_status = str(event.get("repair_status", "")).strip()
    pattern_key = str(event.get("pattern_key", "")).strip()
    timeout_repair_success = bool(event.get("timeout_repair_success", False))

    trust = 0.0
    satisfaction = 0.0
    intimacy = 0.0
    stability = 0.0
    repair = 0.0
    old_wound = 0.0
    safety = 0.0
    excitement = 0.0
    fairness = 0.0
    dependence = 0.0
    tags: list[str] = []
    memory_notes: list[str] = []
    reasons: list[str] = []

    harmful_truth = truth_type in HARMFUL_TRUTH_TYPES
    serious_truth_damage = truth_harm >= 7 or deception >= 7 or harmful_truth
    any_truth_damage = truth_harm > 0 or deception > 0 or harmful_truth

    if any_truth_damage:
        trust_loss = truth_harm * 0.8 + deception * 1.15
        if harmful_truth:
            trust_loss += 3
        if evidence >= 7 and (deception > 0 or harmful_truth):
            trust_loss += 1.5
        trust -= trust_loss
        satisfaction -= min(8, truth_harm * 0.45 + deception * 0.35)
        stability -= min(7, truth_harm * 0.35 + deception * 0.4)
        if serious_truth_damage:
            old_wound += min(10, truth_harm * 0.5 + deception * 0.5)
            _add(tags, "trust_damage_event")
            _add(tags, "old_wound_written")
        if deception > 0 or harmful_truth:
            _add(tags, "deception_risk")
        reasons.append("truth/deception handled as the primary trust-impact rule")

    if privacy_conflict > 0 and not harmful_truth and deception <= 0 and truth_harm <= 3:
        trust -= min(2, privacy_conflict * 0.2)
        satisfaction -= min(4, privacy_conflict * 0.45)
        intimacy -= min(4, privacy_conflict * 0.35)
        _add(tags, "privacy_boundary_conflict")
        reasons.append("privacy boundary conflict treated separately from deception")

    inferred_accurate_alertness = (
        interpretation_type == "suspicion" and evidence >= 7 and truth_harm >= 7
    )
    inferred_over_suspicion = (
        interpretation_type == "suspicion"
        and evidence <= 3
        and truth_harm <= 3
        and (projection_bias >= 7 or threat_bias >= 7)
    )

    if interpretation_accuracy in ACCURATE_ALERTNESS_VALUES or inferred_accurate_alertness:
        _add(tags, "accurate_alertness")
        reasons.append("suspicion is supported by the truth/evidence layer")
    elif interpretation_accuracy in OVER_SUSPICION_VALUES or inferred_over_suspicion:
        satisfaction -= 2
        stability -= 1
        _add(tags, "over_suspicion_pattern")
        reasons.append("weakly supported suspicion adds relationship pressure without major trust loss")

    if perceived_responsiveness > 0:
        intimacy += min(5, perceived_responsiveness * 0.45)
        satisfaction += min(3, perceived_responsiveness * 0.25)
        reasons.append("perceived responsiveness supports intimacy")

    if validation_skill > 0:
        repair += min(4, validation_skill * 0.35)
        intimacy += min(3, validation_skill * 0.25)
        reasons.append("validation skill improves repair chance")

    if active_listening > 0:
        repair += min(4, active_listening * 0.35)
        intimacy += min(3, active_listening * 0.25)
        _add(tags, "active_listener")
        reasons.append("active listening improves repair chance")

    effective_timeout = timeout_repair_success or repair_status in {"repaired", "partially_repaired"}
    if stonewalling > 0 and not effective_timeout:
        trust -= min(7, stonewalling * 0.55)
        satisfaction -= min(8, stonewalling * 0.7)
        repair -= min(8, stonewalling * 0.85)
        old_wound += min(7, stonewalling * 0.55)
        _add(tags, "stonewalling_pattern")
        _add(tags, "old_wound_written")
        reasons.append("stonewalling damages repair chance and may write old wound memory")
    elif effective_timeout and stonewalling <= 2:
        repair += 3
        _add(tags, "repair_window_open")
        reasons.append("effective timeout is not treated as stonewalling")

    if conflict_escalation > 0:
        satisfaction -= min(6, conflict_escalation * 0.45)
        stability -= min(5, conflict_escalation * 0.35)
        reasons.append("conflict escalation affects satisfaction/stability rather than duplicating trust loss")

    if repair_quality > 0:
        repair += min(8, repair_quality * 0.8)
        satisfaction += min(3, repair_quality * 0.2)
        if old_wound > 0:
            old_wound -= min(old_wound, repair_quality * 0.25)
        _add(tags, "repair_capable")
        _add(tags, "repair_window_open")
        reasons.append("high-quality repair improves repair chance and softens wound intensity")

    if rewards_delta:
        satisfaction += rewards_delta * 0.6
        intimacy += max(0, rewards_delta) * 0.25
        reasons.append("relationship rewards affect satisfaction")

    if costs_delta:
        satisfaction -= costs_delta * 0.6
        stability -= max(0, costs_delta) * 0.25
        reasons.append("relationship costs affect satisfaction/stability")

    if approach_reward:
        excitement += approach_reward * 0.6
        satisfaction += max(0, approach_reward) * 0.25
        intimacy += max(0, approach_reward) * 0.2
        reasons.append("approach rewards affect excitement without implying safety")

    if direct_excitement:
        excitement += direct_excitement * 0.8
        reasons.append("direct relationship excitement field applied")

    if avoidance_pressure:
        if avoidance_pressure > 0:
            safety -= min(8, avoidance_pressure * 0.7)
            stability -= min(5, avoidance_pressure * 0.35)
            satisfaction -= min(4, avoidance_pressure * 0.25)
            reasons.append("avoidance pressure lowers safety/stability")
        else:
            safety += min(5, abs(avoidance_pressure) * 0.5)
            reasons.append("lower avoidance pressure can improve safety but not excitement")

    if direct_safety:
        safety += direct_safety * 0.8
        reasons.append("direct relationship safety field applied")

    if boredom:
        if boredom > 0:
            excitement -= min(8, boredom * 0.6)
            satisfaction -= min(4, boredom * 0.3)
            reasons.append("boredom lowers excitement/satisfaction")
        else:
            excitement += min(4, abs(boredom) * 0.3)
            reasons.append("lower boredom can restore some excitement")

    if avoidance_pressure < 0 and approach_reward <= 2 and boredom >= 5:
        _add(tags, "safe_but_bored_pattern")
        reasons.append("low threat is not treated as high excitement")

    if approach_reward >= 7 and (avoidance_pressure >= 5 or conflict_escalation >= 5):
        _add(tags, "risk_excitement_pattern")
        reasons.append("high reward with high pressure is treated as risky excitement")

    if perceived_equity:
        fairness += perceived_equity * 0.7
        reasons.append("perceived equity directly adjusts fairness")

    if felt_appreciation:
        fairness += felt_appreciation * 0.4
        satisfaction += max(0, felt_appreciation) * 0.2
        reasons.append("felt appreciation supports fairness/satisfaction")

    if underbenefit > 0:
        fairness -= min(8, underbenefit * 0.7)
        satisfaction -= min(5, underbenefit * 0.35)
        _add(tags, "underbenefit_sensitive")
        reasons.append("underbenefit lowers fairness")

    if taken_for_granted > 0:
        fairness -= min(7, taken_for_granted * 0.6)
        satisfaction -= min(5, taken_for_granted * 0.35)
        _add(tags, "taken_for_granted_sensitive")
        reasons.append("being taken for granted lowers fairness/satisfaction")

    if overbenefit_guilt > 0:
        fairness -= min(3, overbenefit_guilt * 0.2)
        reasons.append("overbenefit guilt is tracked as a light fairness cost")

    equity_ratio_delta = _equity_ratio_delta(event)
    if equity_ratio_delta is not None:
        if equity_ratio_delta < -0.2:
            fairness += max(-5, equity_ratio_delta * 4)
            _add(tags, "underbenefit_sensitive")
            reasons.append("outcome-to-contribution ratio suggests underbenefit")
        elif equity_ratio_delta > 0.2:
            fairness += min(3, equity_ratio_delta * 2)
            reasons.append("outcome-to-contribution ratio suggests overbenefit")
        else:
            fairness += 1
            reasons.append("similar outcome-to-contribution ratios are treated as equitable")

    if pattern_key and occurrence_count >= 3:
        old_wound += min(6, occurrence_count - 2)
        satisfaction -= min(5, (occurrence_count - 2) * 0.7)
        _add(tags, "pattern_memory_risk")
        memory_notes.append(f"同类事件已出现 {occurrence_count} 次：{pattern_key}")
        reasons.append("repeated events are tracked as pattern risk")

    if repair_status == "repeated_after_repair":
        trust -= 3
        old_wound += 4
        _add(tags, "old_wound_written")
        memory_notes.append("修复后再次发生同类问题，旧伤风险上升")
        reasons.append("repetition after repair weakens change-belief")

    if old_wound > 0 and not memory_notes:
        memory_notes.append("本次事件可能进入旧伤或长期记忆")

    if not tags:
        _add(tags, "short_term_fluctuation")
        reasons.append("event remains a bounded short-term fluctuation")

    major_event = serious_truth_damage or stonewalling >= 7 or repair_status == "repeated_after_repair"

    return RelationshipStateDelta(
        source_id=source_id,
        target_id=target_id,
        trust_delta=_bounded_int(trust, major_event=major_event),
        satisfaction_delta=_bounded_int(satisfaction, major_event=major_event),
        intimacy_delta=_bounded_int(intimacy, major_event=major_event),
        stability_delta=_bounded_int(stability, major_event=major_event),
        repair_chance_delta=_bounded_int(repair, major_event=major_event),
        old_wound_memory_delta=_bounded_int(old_wound, major_event=major_event),
        safety_delta=_bounded_int(safety, major_event=major_event),
        excitement_delta=_bounded_int(excitement, major_event=major_event),
        fairness_delta=_bounded_int(fairness, major_event=major_event),
        dependence_delta=_bounded_int(dependence, major_event=major_event),
        report_tags=tags,
        memory_notes=memory_notes,
        debug_reasons=reasons,
    )


def _add(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def _score(value: Any, low: float = 0.0, high: float = 10.0) -> float:
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in LEVEL_SCORES:
            return max(low, min(high, LEVEL_SCORES[normalized]))
        try:
            number = float(normalized)
        except ValueError:
            return low
    else:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return low
    return max(low, min(high, number))


def _signed_score(value: Any, low: float = -10.0, high: float = 10.0) -> float:
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in LEVEL_SCORES:
            return max(low, min(high, LEVEL_SCORES[normalized]))
        try:
            number = float(normalized)
        except ValueError:
            return 0.0
    else:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return 0.0
    return max(low, min(high, number))


def _equity_ratio_delta(event: Mapping[str, Any]) -> float | None:
    player_contribution = _score(event.get("player_contribution", 0), high=100)
    player_outcome = _score(event.get("player_outcome", 0), high=100)
    npc_contribution = _score(event.get("npc_contribution", 0), high=100)
    npc_outcome = _score(event.get("npc_outcome", 0), high=100)
    if min(player_contribution, player_outcome, npc_contribution, npc_outcome) <= 0:
        return None
    player_ratio = player_outcome / player_contribution
    npc_ratio = npc_outcome / npc_contribution
    return player_ratio - npc_ratio


def _bounded_int(value: float, major_event: bool = False) -> int:
    limit = 20 if major_event else 10
    return int(round(max(-limit, min(limit, value))))

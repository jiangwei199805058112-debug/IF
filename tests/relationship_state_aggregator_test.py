from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.conflict_event_samples import (  # noqa: E402
    late_arrival_complaint_event,
    mocking_vulnerability_event,
    timeout_request_event,
)
from if_game.exchange_event_samples import (  # noqa: E402
    equity_repair_event,
    household_underbenefit_event,
    stable_but_bored_event,
)
from if_game.relationship_state_aggregator import (  # noqa: E402
    RelationshipStateDelta,
    aggregate_relationship_event,
)


REQUIRED_FIELDS = {
    "source_id",
    "target_id",
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
    "report_tags",
    "memory_notes",
    "debug_reasons",
}


def _assert_common_shape(delta: RelationshipStateDelta) -> None:
    data = delta.to_dict()
    assert REQUIRED_FIELDS.issubset(data)
    assert isinstance(delta.report_tags, list)
    assert isinstance(delta.memory_notes, list)
    assert isinstance(delta.debug_reasons, list)
    for field_name in REQUIRED_FIELDS - {"source_id", "target_id", "report_tags", "memory_notes", "debug_reasons"}:
        assert -20 <= data[field_name] <= 20, field_name


def _assert_tag_absent(delta: RelationshipStateDelta, tag: str) -> None:
    assert tag not in delta.report_tags


def _test_common_shape_and_reserved_defaults() -> None:
    mild = aggregate_relationship_event(
        {
            "source_id": "npc_a",
            "target_id": "player",
            "truth_harm_level": 2,
            "deception_level": 0,
            "evidence_chain_strength": "weak",
        }
    )
    _assert_common_shape(mild)
    assert mild.source_id == "npc_a"
    assert mild.target_id == "player"
    assert mild.trust_delta >= -5
    assert mild.safety_delta == 0
    assert mild.excitement_delta == 0
    assert mild.fairness_delta == 0
    assert mild.dependence_delta == 0


def _test_silence_is_not_always_stonewalling() -> None:
    repaired_pause = aggregate_relationship_event(
        {
            "stonewalling_level": 0,
            "communication_response_type": "processing_silence",
            "timeout_repair_success": True,
            "repair_attempt_quality": "high",
        }
    )
    _assert_common_shape(repaired_pause)
    assert repaired_pause.repair_chance_delta > 0
    assert repaired_pause.old_wound_memory_delta <= 0
    assert "repair_window_open" in repaired_pause.report_tags
    _assert_tag_absent(repaired_pause, "stonewalling_pattern")


def _test_stonewalling_is_high_harm_communication() -> None:
    stonewalling = aggregate_relationship_event(
        {
            "source_id": "player",
            "target_id": "npc_a",
            "stonewalling_level": "high",
            "timeout_repair_success": False,
            "conflict_escalation_risk": "medium",
        }
    )
    _assert_common_shape(stonewalling)
    assert stonewalling.trust_delta < 0
    assert stonewalling.satisfaction_delta < 0
    assert stonewalling.repair_chance_delta < 0
    assert stonewalling.old_wound_memory_delta > 0
    assert "stonewalling_pattern" in stonewalling.report_tags
    assert stonewalling.memory_notes


def _test_conflict_can_be_repaired_successfully() -> None:
    repaired_conflict = aggregate_relationship_event(
        {
            "conflict_escalation_risk": "medium",
            "validation_skill": "high",
            "active_listening_skill": "high",
            "repair_attempt_quality": "high",
        }
    )
    _assert_common_shape(repaired_conflict)
    assert repaired_conflict.repair_chance_delta > 0
    assert repaired_conflict.intimacy_delta >= 0
    assert repaired_conflict.satisfaction_delta >= -3
    assert "repair_capable" in repaired_conflict.report_tags
    assert "active_listener" in repaired_conflict.report_tags


def _test_suspicion_can_be_accurate_alertness() -> None:
    accurate = aggregate_relationship_event(
        {
            "truth_type": "concealment",
            "truth_harm_level": "high",
            "deception_level": 0,
            "evidence_chain_strength": "strong",
            "interpretation_type": "suspicion",
            "interpretation_accuracy": "accurate_alertness",
        }
    )
    _assert_common_shape(accurate)
    assert accurate.trust_delta < 0
    assert "accurate_alertness" in accurate.report_tags
    _assert_tag_absent(accurate, "over_suspicion_pattern")


def _test_suspicion_can_be_misunderstanding_or_anxiety() -> None:
    over_suspicion = aggregate_relationship_event(
        {
            "truth_harm_level": "low",
            "evidence_chain_strength": "low",
            "interpretation_type": "suspicion",
            "projection_bias_effect": "high",
            "threat_bias_effect": "high",
        }
    )
    _assert_common_shape(over_suspicion)
    assert over_suspicion.trust_delta >= -3
    assert over_suspicion.satisfaction_delta < 0
    assert "over_suspicion_pattern" in over_suspicion.report_tags
    _assert_tag_absent(over_suspicion, "accurate_alertness")


def _test_privacy_is_not_deception() -> None:
    privacy = aggregate_relationship_event(
        {
            "truth_type": "privacy_boundary",
            "truth_harm_level": 1,
            "deception_level": 0,
            "privacy_boundary_conflict": 8,
        }
    )
    _assert_common_shape(privacy)
    assert privacy.trust_delta >= -3
    assert privacy.satisfaction_delta < 0
    assert privacy.intimacy_delta < 0
    assert "privacy_boundary_conflict" in privacy.report_tags
    _assert_tag_absent(privacy, "deception_risk")


def _test_low_pain_is_not_high_pleasure() -> None:
    safe_but_bored = aggregate_relationship_event(
        {
            "avoidance_cost_pressure_delta": -8,
            "approach_reward_delta": 0,
            "boredom_delta": "high",
        }
    )
    _assert_common_shape(safe_but_bored)
    assert safe_but_bored.safety_delta > 0
    assert safe_but_bored.excitement_delta <= 0
    assert safe_but_bored.intimacy_delta == 0
    assert "safe_but_bored_pattern" in safe_but_bored.report_tags
    _assert_tag_absent(safe_but_bored, "risk_excitement_pattern")


def _test_high_pleasure_is_not_safety() -> None:
    risky_excitement = aggregate_relationship_event(
        {
            "approach_reward_delta": "high",
            "avoidance_cost_pressure_delta": "high",
            "conflict_escalation_risk": "high",
        }
    )
    _assert_common_shape(risky_excitement)
    assert risky_excitement.excitement_delta > 0
    assert risky_excitement.safety_delta < 0
    assert risky_excitement.stability_delta < 0
    assert "risk_excitement_pattern" in risky_excitement.report_tags


def _test_fairness_is_not_fifty_fifty() -> None:
    proportional_equity = aggregate_relationship_event(
        {
            "player_contribution": 70,
            "player_outcome": 90,
            "npc_contribution": 40,
            "npc_outcome": 50,
        }
    )
    _assert_common_shape(proportional_equity)
    assert proportional_equity.fairness_delta >= 0
    _assert_tag_absent(proportional_equity, "underbenefit_sensitive")


def _test_same_event_does_not_duplicate_trust_loss() -> None:
    deception = aggregate_relationship_event(
        {
            "truth_type": "concealment",
            "truth_harm_level": 7,
            "deception_level": 7,
            "evidence_chain_strength": "strong",
        }
    )
    _assert_common_shape(deception)
    assert -20 <= deception.trust_delta <= -10
    assert deception.old_wound_memory_delta > 0
    assert "trust_damage_event" in deception.report_tags
    assert "deception_risk" in deception.report_tags

    combined_pressure = aggregate_relationship_event(
        {
            "truth_type": "concealment",
            "truth_harm_level": 7,
            "deception_level": 7,
            "evidence_chain_strength": "strong",
            "interpretation_type": "suspicion",
            "interpretation_accuracy": "accurate_alertness",
            "conflict_escalation_risk": "high",
        }
    )
    _assert_common_shape(combined_pressure)
    assert combined_pressure.trust_delta >= deception.trust_delta
    assert combined_pressure.trust_delta < 0
    assert "trust_damage_event" in combined_pressure.report_tags
    assert "accurate_alertness" in combined_pressure.report_tags


def _test_repeated_events_write_pattern_memory() -> None:
    pattern = aggregate_relationship_event(
        {
            "pattern_key": "late_reply_inconsistency",
            "occurrence_count": 3,
            "repair_status": "repeated_after_repair",
        }
    )
    _assert_common_shape(pattern)
    assert pattern.old_wound_memory_delta > 0
    assert pattern.memory_notes
    assert "pattern_memory_risk" in pattern.report_tags


def _test_conflict_repair_sample_improves_repair_chance() -> None:
    repaired = aggregate_relationship_event(late_arrival_complaint_event("repair"))
    _assert_common_shape(repaired)
    assert repaired.source_id == "player"
    assert repaired.target_id == "npc_a"
    assert repaired.repair_chance_delta > 0
    assert repaired.satisfaction_delta >= -3
    assert "repair_capable" in repaired.report_tags


def _test_defensive_or_cross_complaining_sample_lowers_repair() -> None:
    defensive = aggregate_relationship_event(late_arrival_complaint_event("defensive"))
    cross_complaining = aggregate_relationship_event(
        late_arrival_complaint_event("cross_complaining")
    )
    _assert_common_shape(defensive)
    _assert_common_shape(cross_complaining)
    assert defensive.repair_chance_delta < 0 or defensive.satisfaction_delta < 0
    assert cross_complaining.repair_chance_delta < 0 or cross_complaining.satisfaction_delta < 0
    assert cross_complaining.stability_delta < 0


def _test_timeout_sample_is_not_stonewalling() -> None:
    timeout = aggregate_relationship_event(timeout_request_event())
    _assert_common_shape(timeout)
    assert timeout.repair_chance_delta > 0
    assert timeout.old_wound_memory_delta <= 0
    assert "repair_window_open" in timeout.report_tags
    _assert_tag_absent(timeout, "stonewalling_pattern")


def _test_mocking_vulnerability_sample_writes_old_wound() -> None:
    mocking = aggregate_relationship_event(mocking_vulnerability_event())
    _assert_common_shape(mocking)
    assert mocking.old_wound_memory_delta > 0
    assert mocking.intimacy_delta < 0
    assert "contempt_risk" in mocking.report_tags
    assert "old_wound_written" in mocking.report_tags
    assert mocking.memory_notes


def _test_conflict_samples_can_all_be_aggregated() -> None:
    samples = [
        late_arrival_complaint_event("repair"),
        late_arrival_complaint_event("defensive"),
        late_arrival_complaint_event("cross_complaining"),
        timeout_request_event(),
        mocking_vulnerability_event(),
    ]
    for sample in samples:
        delta = aggregate_relationship_event(sample)
        _assert_common_shape(delta)
        assert sample["event_id"].startswith("E-CON-")


def _test_stable_but_bored_sample_uses_exchange_fields() -> None:
    bored = aggregate_relationship_event(stable_but_bored_event())
    _assert_common_shape(bored)
    assert bored.safety_delta > 0
    assert bored.excitement_delta <= 0
    assert bored.trust_delta == 0
    assert bored.dependence_delta > 0
    assert "safe_but_bored_pattern" in bored.report_tags


def _test_long_term_underbenefit_lowers_satisfaction() -> None:
    underbenefit = aggregate_relationship_event(household_underbenefit_event())
    _assert_common_shape(underbenefit)
    assert underbenefit.satisfaction_delta < 0
    assert underbenefit.fairness_delta < 0
    assert underbenefit.trust_delta == 0
    assert "underbenefit_sensitive" in underbenefit.report_tags
    assert "taken_for_granted_sensitive" in underbenefit.report_tags
    assert "pattern_memory_risk" in underbenefit.report_tags
    assert underbenefit.memory_notes


def _test_taken_for_granted_lowers_satisfaction_or_fairness() -> None:
    taken_for_granted = aggregate_relationship_event(
        {
            "event_id": "E-EQU-TFG",
            "event_type": "equity_conflict",
            "taken_for_granted_delta": "high",
            "relationship_rewards_delta": 0,
            "relationship_costs_delta": 2,
        }
    )
    _assert_common_shape(taken_for_granted)
    assert taken_for_granted.satisfaction_delta < 0 or taken_for_granted.fairness_delta < 0
    assert "taken_for_granted_sensitive" in taken_for_granted.report_tags


def _test_equity_repair_sample_restores_fairness() -> None:
    repair = aggregate_relationship_event(equity_repair_event())
    _assert_common_shape(repair)
    assert repair.satisfaction_delta >= 0
    assert repair.fairness_delta > 0
    assert repair.repair_chance_delta > 0
    assert repair.trust_delta == 0
    assert "repair_capable" in repair.report_tags


def _test_exchange_fields_do_not_duplicate_trust_loss() -> None:
    exchange_only = aggregate_relationship_event(
        {
            "relationship_rewards_delta": -3,
            "relationship_costs_delta": 6,
            "approach_reward_delta": -2,
            "avoidance_cost_pressure_delta": 5,
            "boredom_delta": 6,
            "perceived_equity_delta": -4,
            "underbenefit_feeling_delta": 6,
            "taken_for_granted_delta": 5,
            "dependence_delta": -2,
        }
    )
    _assert_common_shape(exchange_only)
    assert exchange_only.trust_delta == 0
    assert exchange_only.satisfaction_delta < 0
    assert exchange_only.fairness_delta < 0
    assert "trust_damage_event" not in exchange_only.report_tags
    assert "deception_risk" not in exchange_only.report_tags


def _test_dependence_is_not_intimacy() -> None:
    dependence_only = aggregate_relationship_event({"dependence_delta": "high"})
    _assert_common_shape(dependence_only)
    assert dependence_only.dependence_delta > 0
    assert dependence_only.intimacy_delta == 0
    assert dependence_only.trust_delta == 0


def main() -> None:
    _test_common_shape_and_reserved_defaults()
    _test_silence_is_not_always_stonewalling()
    _test_stonewalling_is_high_harm_communication()
    _test_conflict_can_be_repaired_successfully()
    _test_suspicion_can_be_accurate_alertness()
    _test_suspicion_can_be_misunderstanding_or_anxiety()
    _test_privacy_is_not_deception()
    _test_low_pain_is_not_high_pleasure()
    _test_high_pleasure_is_not_safety()
    _test_fairness_is_not_fifty_fifty()
    _test_same_event_does_not_duplicate_trust_loss()
    _test_repeated_events_write_pattern_memory()
    _test_conflict_repair_sample_improves_repair_chance()
    _test_defensive_or_cross_complaining_sample_lowers_repair()
    _test_timeout_sample_is_not_stonewalling()
    _test_mocking_vulnerability_sample_writes_old_wound()
    _test_conflict_samples_can_all_be_aggregated()
    _test_stable_but_bored_sample_uses_exchange_fields()
    _test_long_term_underbenefit_lowers_satisfaction()
    _test_taken_for_granted_lowers_satisfaction_or_fairness()
    _test_equity_repair_sample_restores_fairness()
    _test_exchange_fields_do_not_duplicate_trust_loss()
    _test_dependence_is_not_intimacy()

    print("relationship state aggregator test passed")


if __name__ == "__main__":
    main()

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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


def main() -> None:
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
    assert "privacy_boundary_conflict" in privacy.report_tags

    deception = aggregate_relationship_event(
        {
            "truth_type": "concealment",
            "truth_harm_level": 9,
            "deception_level": 9,
            "evidence_chain_strength": "strong",
        }
    )
    _assert_common_shape(deception)
    assert -20 <= deception.trust_delta <= -10
    assert deception.old_wound_memory_delta > 0
    assert "trust_damage_event" in deception.report_tags
    assert "deception_risk" in deception.report_tags

    stonewalling = aggregate_relationship_event(
        {
            "source_id": "player",
            "target_id": "npc_a",
            "stonewalling_level": 8,
            "conflict_escalation_risk": 6,
        }
    )
    _assert_common_shape(stonewalling)
    assert stonewalling.repair_chance_delta < 0
    assert stonewalling.old_wound_memory_delta > 0
    assert "stonewalling_pattern" in stonewalling.report_tags
    assert stonewalling.memory_notes

    repaired = aggregate_relationship_event(
        {
            "stonewalling_level": 0,
            "timeout_repair_success": True,
            "repair_attempt_quality": 8,
            "validation_skill": 7,
        }
    )
    _assert_common_shape(repaired)
    assert repaired.repair_chance_delta > 0
    assert repaired.old_wound_memory_delta <= 0
    assert "repair_capable" in repaired.report_tags
    assert "stonewalling_pattern" not in repaired.report_tags

    duplicated_pressure = aggregate_relationship_event(
        {
            "truth_type": "betrayal",
            "truth_harm_level": 10,
            "deception_level": 10,
            "evidence_chain_strength": "conclusive",
            "conflict_escalation_risk": 10,
            "stonewalling_level": 10,
        }
    )
    _assert_common_shape(duplicated_pressure)
    assert duplicated_pressure.trust_delta >= -20
    assert duplicated_pressure.trust_delta < 0
    assert "trust_damage_event" in duplicated_pressure.report_tags

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

    print("relationship state aggregator test passed")


if __name__ == "__main__":
    main()

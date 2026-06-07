from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.relationship_memory import (  # noqa: E402
    RelationshipMemory,
    decay_relationship_memories,
    format_memory_summary,
    update_memories_from_aggregated_event,
    update_relationship_memories,
)
from if_game.relationship_state_aggregator import aggregate_relationship_event  # noqa: E402


def _old_wound_memories(memories: list[RelationshipMemory]) -> list[RelationshipMemory]:
    return [memory for memory in memories if memory.memory_type == "old_wound_memory"]


def _pattern_memories(memories: list[RelationshipMemory]) -> list[RelationshipMemory]:
    return [memory for memory in memories if memory.memory_type == "pattern_memory"]


def _repair_memories(memories: list[RelationshipMemory]) -> list[RelationshipMemory]:
    return [memory for memory in memories if memory.memory_type == "repair_memory"]


def _test_high_harm_delta_writes_old_wound_memory() -> None:
    event = {
        "event_id": "E-MEM-HARM",
        "source_id": "npc_a",
        "target_id": "player",
        "truth_type": "concealment",
        "truth_harm_level": "high",
        "deception_level": "high",
        "evidence_chain_strength": "strong",
        "pattern_key": "hidden_contact_or_ex",
    }
    delta = aggregate_relationship_event(event)

    memories = update_relationship_memories([], event, delta, day=2)
    old_wounds = _old_wound_memories(memories)

    assert old_wounds
    assert old_wounds[0].wound_type == "betrayal_discovered"
    assert old_wounds[0].intensity > 0
    assert old_wounds[0].source_event_id == "E-MEM-HARM"


def _test_mild_event_does_not_write_old_wound_memory() -> None:
    event = {
        "event_id": "E-MEM-MILD",
        "source_id": "npc_a",
        "target_id": "player",
        "truth_harm_level": 1,
        "deception_level": 0,
        "evidence_chain_strength": "weak",
    }
    delta = aggregate_relationship_event(event)

    memories = update_relationship_memories([], event, delta, day=3)

    assert not _old_wound_memories(memories)


def _test_pattern_key_with_three_occurrences_writes_pattern_memory() -> None:
    event = {
        "event_id": "E-MEM-PATTERN-3",
        "source_id": "npc_a",
        "target_id": "player",
        "pattern_key": "late_reply_inconsistency",
        "occurrence_count": 3,
    }
    delta = aggregate_relationship_event(event)

    memories = update_relationship_memories([], event, delta, day=4)
    patterns = _pattern_memories(memories)

    assert patterns
    assert patterns[0].pattern_key == "late_reply_inconsistency"
    assert patterns[0].occurrence_count >= 3
    assert patterns[0].decay_policy == "pattern_reinforced"


def _test_same_pattern_updates_existing_memory_without_duplicate() -> None:
    first_event = {
        "event_id": "E-MEM-PATTERN-A",
        "source_id": "npc_a",
        "target_id": "player",
        "pattern_key": "stonewalling_after_conflict",
        "occurrence_count": 3,
    }
    second_event = {
        "event_id": "E-MEM-PATTERN-B",
        "source_id": "npc_a",
        "target_id": "player",
        "pattern_key": "stonewalling_after_conflict",
        "occurrence_count": 4,
    }

    memories = update_relationship_memories(
        [],
        first_event,
        aggregate_relationship_event(first_event),
        day=5,
    )
    first_pattern = _pattern_memories(memories)[0]
    memories = update_relationship_memories(
        memories,
        second_event,
        aggregate_relationship_event(second_event),
        day=8,
    )
    patterns = _pattern_memories(memories)

    assert len(patterns) == 1
    assert patterns[0].occurrence_count >= 4
    assert patterns[0].last_triggered_day == 8
    assert patterns[0].intensity >= first_pattern.intensity


def _test_repair_capable_or_high_repair_quality_writes_repair_memory() -> None:
    event = {
        "event_id": "E-MEM-REPAIR",
        "source_id": "player",
        "target_id": "npc_a",
        "conflict_response_type": "repair_attempt",
        "repair_attempt_quality": "high",
        "repair_status": "partially_repaired",
        "pattern_key": "conflict_repair_success",
    }
    delta = aggregate_relationship_event(event)

    memories = update_relationship_memories([], event, delta, day=6)
    repairs = _repair_memories(memories)

    assert repairs
    assert repairs[0].repair_status in {"partially_repaired", "repaired"}
    assert repairs[0].intensity > 0


def _test_repaired_status_lowers_old_wound_or_marks_repaired() -> None:
    wound_event = {
        "event_id": "E-MEM-WOUND",
        "source_id": "npc_a",
        "target_id": "player",
        "truth_type": "concealment",
        "truth_harm_level": "high",
        "deception_level": "high",
        "pattern_key": "hidden_contact_or_ex",
    }
    memories = update_relationship_memories(
        [],
        wound_event,
        aggregate_relationship_event(wound_event),
        day=7,
    )
    old_before = _old_wound_memories(memories)[0]

    repair_event = {
        "event_id": "E-MEM-WOUND-REPAIR",
        "source_id": "npc_a",
        "target_id": "player",
        "conflict_response_type": "repair_attempt",
        "repair_attempt_quality": 9,
        "repair_status": "repaired",
        "pattern_key": "hidden_contact_or_ex",
    }
    memories = update_relationship_memories(
        memories,
        repair_event,
        aggregate_relationship_event(repair_event),
        day=10,
    )
    old_after = [
        memory
        for memory in _old_wound_memories(memories)
        if memory.pattern_key == "hidden_contact_or_ex"
    ][0]

    assert old_after.intensity < old_before.intensity or old_after.repair_status == "repaired"
    assert old_after.repair_status == "repaired"


def _test_normal_decay_lowers_intensity_by_periods() -> None:
    memory = RelationshipMemory(
        memory_id="mem:test:normal",
        source_event_id="E-DECAY",
        source_id="npc_a",
        target_id="player",
        memory_type="old_wound_memory",
        wound_type="relationship_wound",
        pattern_key=None,
        severity="medium",
        intensity=50,
        created_day=1,
        last_triggered_day=1,
        occurrence_count=1,
        decay_policy="normal_decay",
        repair_status="unrepaired",
        visibility="player_visible",
        player_facing_note="这段经历仍可能影响之后的信任和安全感。",
        debug_note="truth_type=concealment deception_level=8",
    )

    decayed = decay_relationship_memories([memory], current_day=15)

    assert decayed[0].intensity == 40


def _test_no_decay_until_repair_does_not_decay_when_unrepaired() -> None:
    memory = RelationshipMemory(
        memory_id="mem:test:no-decay",
        source_event_id="E-NO-DECAY",
        source_id="npc_a",
        target_id="player",
        memory_type="old_wound_memory",
        wound_type="betrayal_discovered",
        pattern_key="hidden_contact_or_ex",
        severity="high",
        intensity=70,
        created_day=1,
        last_triggered_day=1,
        occurrence_count=1,
        decay_policy="no_decay_until_repair",
        repair_status="unrepaired",
        visibility="player_visible",
        player_facing_note="这段经历仍可能影响之后的信任和安全感。",
        debug_note="truth_type=concealment deception_level=8",
    )

    decayed = decay_relationship_memories([memory], current_day=22)

    assert decayed[0].intensity == 70


def _test_empty_inputs_and_legacy_memory_dict_are_safe() -> None:
    legacy_memory = {
        "memory_id": "legacy-memory",
        "source_event_id": "OLD-EVENT",
        "source_id": "npc_a",
        "target_id": "player",
        "memory_type": "old_wound_memory",
        "intensity": 35,
    }

    memories = update_relationship_memories([legacy_memory], {}, {}, day=20)
    decayed = decay_relationship_memories(memories, current_day=27)
    summary = format_memory_summary(decayed)

    assert len(memories) == 1
    assert memories[0].memory_id == "legacy-memory"
    assert memories[0].repair_status == "unrepaired"
    assert memories[0].decay_policy == "normal_decay"
    assert 0 <= decayed[0].intensity <= 35
    assert summary


def _test_player_visible_summary_does_not_leak_debug_truth() -> None:
    memory = RelationshipMemory(
        memory_id="mem:test:summary",
        source_event_id="E-SUMMARY",
        source_id="npc_a",
        target_id="player",
        memory_type="old_wound_memory",
        wound_type="betrayal_discovered",
        pattern_key="hidden_contact_or_ex",
        severity="high",
        intensity=80,
        created_day=1,
        last_triggered_day=1,
        occurrence_count=1,
        decay_policy="no_decay_until_repair",
        repair_status="unrepaired",
        visibility="player_visible",
        player_facing_note="这段经历会让之后的信任恢复更慢。",
        debug_note="truth_type=concealment deception_level=9 hidden_truth_notes=true",
    )

    summary = "\n".join(format_memory_summary([memory], player_visible_only=True))

    assert "truth_type" not in summary
    assert "deception_level" not in summary
    assert "concealment" not in summary
    assert "hidden_truth" not in summary


def _test_aggregator_output_can_be_consumed_by_memory_system() -> None:
    event = {
        "event_id": "E-MEM-BRIDGE",
        "source_id": "npc_a",
        "target_id": "player",
        "conflict_response_type": "contempt",
        "communication_response_type": "mocking_response",
        "truth_harm_level": "medium",
        "pattern_key": "contempt_or_mockery",
    }
    delta = aggregate_relationship_event(event)

    memories = update_memories_from_aggregated_event([], event, delta, day=12)
    data = [memory.to_dict() for memory in memories]
    summary = "\n".join(format_memory_summary(memories))

    assert memories
    assert any(item["memory_type"] == "old_wound_memory" for item in data)
    assert any(item["source_event_id"] == "E-MEM-BRIDGE" for item in data)
    assert "truth_type" not in summary
    assert "deception_level" not in summary


def main() -> None:
    _test_high_harm_delta_writes_old_wound_memory()
    _test_mild_event_does_not_write_old_wound_memory()
    _test_pattern_key_with_three_occurrences_writes_pattern_memory()
    _test_same_pattern_updates_existing_memory_without_duplicate()
    _test_repair_capable_or_high_repair_quality_writes_repair_memory()
    _test_repaired_status_lowers_old_wound_or_marks_repaired()
    _test_normal_decay_lowers_intensity_by_periods()
    _test_no_decay_until_repair_does_not_decay_when_unrepaired()
    _test_empty_inputs_and_legacy_memory_dict_are_safe()
    _test_player_visible_summary_does_not_leak_debug_truth()
    _test_aggregator_output_can_be_consumed_by_memory_system()

    print("relationship memory test passed")


if __name__ == "__main__":
    main()

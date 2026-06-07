from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.relationship_event_samples import (  # noqa: E402
    accountability_repair_event,
    dinner_disclosure_event,
    event_to_aggregator_input,
    event_to_interpretation_input,
    forgotten_small_promise_event,
    phone_boundary_event,
    relationship_event_samples,
    supportive_listening_event,
)
from if_game.relationship_flow_integration import (  # noqa: E402
    apply_relationship_delta_to_state,
    format_relationship_delta_summary,
)
from if_game.relationship_interpretation import (  # noqa: E402
    interpret_relationship_event,
    interpretation_to_aggregator_input,
)
from if_game.relationship_memory import (  # noqa: E402
    format_memory_summary,
    update_relationship_memories,
)
from if_game.relationship_state_aggregator import aggregate_relationship_event  # noqa: E402


REQUIRED_SAMPLE_FIELDS = {
    "event_id",
    "title",
    "short_description",
    "trigger",
    "context",
    "relationship_delta",
    "memory_candidate",
    "visibility",
}


def _aggregate_sample(event: dict):
    aggregator_input = event_to_aggregator_input(event)
    return aggregator_input, aggregate_relationship_event(aggregator_input)


def _summary_text(delta, memories) -> str:
    return "\n".join(
        [
            *format_relationship_delta_summary(delta),
            *format_memory_summary(memories),
        ]
    )


def _assert_no_debug_truth(text: str) -> None:
    for token in ["truth_type", "deception_level", "hidden_truth", "debug_note"]:
        assert token not in text


def _test_sample_events_have_minimum_shape() -> None:
    samples = relationship_event_samples()
    assert len(samples) == 5
    for sample in samples:
        assert REQUIRED_SAMPLE_FIELDS.issubset(sample.keys()), sample["event_id"]
        assert sample["event_id"].startswith("E-REL-")
        assert sample["visibility"] in {"public", "private", "hidden", "discovered"}
        assert isinstance(sample["relationship_delta"], dict)
        assert isinstance(sample["memory_candidate"], dict)


def _test_positive_event_improves_trust_and_logs_repair_memory() -> None:
    event = supportive_listening_event()
    aggregator_input, delta = _aggregate_sample(event)
    memories = update_relationship_memories([], aggregator_input, delta, day=4)
    state: dict = {}
    apply_relationship_delta_to_state(state, delta)

    assert delta.trust_delta > 0
    assert delta.safety_delta > 0
    assert delta.repair_chance_delta > 0
    assert any(memory.memory_type == "repair_memory" for memory in memories)
    assert state["relationship_aggregator_log"]
    assert state["relationship_delta_summaries"]
    _assert_no_debug_truth(_summary_text(delta, memories))


def _test_minor_negative_event_is_not_major_betrayal_or_old_wound() -> None:
    event = forgotten_small_promise_event()
    aggregator_input, delta = _aggregate_sample(event)
    memories = update_relationship_memories([], aggregator_input, delta, day=5)

    assert -5 <= delta.trust_delta < 0
    assert delta.old_wound_memory_delta <= 0
    assert "trust_damage_event" not in delta.report_tags
    assert "deception_risk" not in delta.report_tags
    assert not any(memory.memory_type == "old_wound_memory" for memory in memories)


def _test_hidden_privacy_event_stays_hidden_until_discovered() -> None:
    hidden_event = phone_boundary_event("hidden")
    discovered_event = phone_boundary_event("discovered")

    hidden_input, hidden_delta = _aggregate_sample(hidden_event)
    discovered_input, discovered_delta = _aggregate_sample(discovered_event)
    hidden_memories = update_relationship_memories([], hidden_input, hidden_delta, day=6)
    discovered_memories = update_relationship_memories([], discovered_input, discovered_delta, day=7)

    assert hidden_event["hidden_relationship_delta"]["privacy_risk_delta"] > 0
    assert hidden_delta.trust_delta == 0
    assert hidden_delta.satisfaction_delta == 0
    assert hidden_delta.old_wound_memory_delta == 0
    assert not hidden_memories

    assert discovered_delta.trust_delta < hidden_delta.trust_delta
    assert discovered_delta.satisfaction_delta < 0
    assert "privacy_boundary_conflict" in discovered_delta.report_tags
    assert not any(memory.memory_type == "old_wound_memory" for memory in discovered_memories)


def _test_accountable_repair_beats_blame_shift() -> None:
    accountable_input, accountable_delta = _aggregate_sample(
        accountability_repair_event("accountable")
    )
    blame_input, blame_delta = _aggregate_sample(accountability_repair_event("blame_shift"))
    accountable_memories = update_relationship_memories([], accountable_input, accountable_delta, day=8)
    blame_memories = update_relationship_memories([], blame_input, blame_delta, day=8)

    assert accountable_delta.repair_chance_delta > 0
    assert accountable_delta.trust_delta >= 0
    assert any(memory.memory_type == "repair_memory" for memory in accountable_memories)

    assert blame_delta.repair_chance_delta < 0
    assert blame_delta.satisfaction_delta < 0
    assert not any(memory.memory_type == "old_wound_memory" for memory in blame_memories)


def _test_disclosure_styles_have_different_risk_profiles() -> None:
    truthful_input, truthful_delta = _aggregate_sample(dinner_disclosure_event("truthful"))
    half_input, half_delta = _aggregate_sample(dinner_disclosure_event("half_truth"))
    hidden_input, hidden_delta = _aggregate_sample(dinner_disclosure_event("hidden"))
    half_memories = update_relationship_memories([], half_input, half_delta, day=9)

    assert truthful_delta.trust_delta >= 0
    assert truthful_delta.repair_chance_delta > 0
    assert half_delta.trust_delta < truthful_delta.trust_delta
    assert "deception_risk" in half_delta.report_tags
    assert half_delta.old_wound_memory_delta <= 0
    assert hidden_delta.trust_delta == 0
    assert not any(memory.memory_type == "old_wound_memory" for memory in half_memories)


def _test_half_truth_sample_can_flow_through_interpretation_and_memory() -> None:
    event = dinner_disclosure_event("half_truth")
    interpretation = interpret_relationship_event(event_to_interpretation_input(event))
    aggregator_input = interpretation_to_aggregator_input(
        interpretation,
        source_id=event["source_id"],
        target_id=event["target_id"],
    )
    delta = aggregate_relationship_event(aggregator_input)
    memories = update_relationship_memories([], aggregator_input, delta, day=10)
    summary = _summary_text(delta, memories)

    assert interpretation["quadrant"]["type"] == "accurate_alertness"
    assert "accurate_alertness" in delta.report_tags
    assert delta.trust_delta < 0
    assert not any(memory.memory_type == "old_wound_memory" for memory in memories)
    assert summary
    _assert_no_debug_truth(summary)


def main() -> None:
    _test_sample_events_have_minimum_shape()
    _test_positive_event_improves_trust_and_logs_repair_memory()
    _test_minor_negative_event_is_not_major_betrayal_or_old_wound()
    _test_hidden_privacy_event_stays_hidden_until_discovered()
    _test_accountable_repair_beats_blame_shift()
    _test_disclosure_styles_have_different_risk_profiles()
    _test_half_truth_sample_can_flow_through_interpretation_and_memory()

    print("relationship event samples test passed")


if __name__ == "__main__":
    main()

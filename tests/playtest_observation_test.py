from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.playtest_observation import (  # noqa: E402
    PlaytestObservation,
    build_playtest_observation,
    format_playtest_observation,
)
from if_game.relationship_event_samples import (  # noqa: E402
    dinner_disclosure_event,
    forgotten_small_promise_event,
    supportive_listening_event,
)


REQUIRED_OBSERVATION_FIELDS = {
    "observation_id",
    "event_id",
    "event_type",
    "event_title",
    "event_visibility",
    "event_discovered",
    "npc_personality_snapshot",
    "relationship_state_before",
    "memory_snapshot",
    "npc_reaction_type",
    "npc_reaction_intensity",
    "npc_public_conflict",
    "npc_followup_risk",
    "npc_reaction_explanation",
    "relationship_delta",
    "memory_candidate",
    "interpretation_summary",
    "tags",
}


def _deception_event(discovered: bool = True) -> dict:
    return {
        "event_id": "E-OBS-DECEPTION",
        "event_type": "deception",
        "title": "玩家隐瞒异性约饭",
        "severity": 70,
        "visibility": "private",
        "discovered": discovered,
        "relationship_delta": {
            "truth_harm_level": 6,
            "deception_level": 7,
            "privacy_boundary_conflict": 4,
        },
        "memory_tags": ["boundary_violation"],
        "context": "玩家隐瞒了异性约饭，后来被对方发现。",
    }


def _assert_complete_observation(observation: PlaytestObservation) -> None:
    data = observation.to_dict()
    assert REQUIRED_OBSERVATION_FIELDS.issubset(data)
    assert observation.observation_id.startswith("obs:")
    assert isinstance(observation.npc_personality_snapshot, dict)
    assert isinstance(observation.relationship_state_before, dict)
    assert isinstance(observation.memory_snapshot, list)
    assert isinstance(observation.relationship_delta, dict)
    assert isinstance(observation.memory_candidate, dict)
    assert isinstance(observation.tags, list)


def _test_build_playtest_observation_generates_complete_fields() -> None:
    observation = build_playtest_observation(
        supportive_listening_event(),
        {"communication_drive": 80, "forgiveness": 70},
        {"trust": 62, "safety": 55, "satisfaction": 58, "repair_chance": 60},
        [{"memory_id": "mem:old", "memory_type": "old_wound_memory", "tags": ["unresolved_betrayal"]}],
    )

    _assert_complete_observation(observation)
    assert observation.event_id == "E-REL-TRU-01"
    assert observation.npc_reaction_type in {"appreciate", "soften"}
    assert observation.npc_reaction_explanation
    assert observation.interpretation_summary


def _test_format_playtest_observation_contains_key_sections() -> None:
    observation = build_playtest_observation(
        forgotten_small_promise_event(),
        {"communication_drive": 60, "forgiveness": 60},
        {"trust": 60, "safety": 58},
        [],
    )
    text = format_playtest_observation(observation)

    for token in ["event:", "personality:", "reaction:", "reason:", "public_conflict:"]:
        assert token in text
    assert observation.event_id in text
    assert observation.npc_reaction_type in text


def _test_hidden_undiscovered_event_never_records_public_conflict() -> None:
    observation = build_playtest_observation(
        dinner_disclosure_event("hidden"),
        {"jealousy": 95, "attachment_anxiety": 90, "revenge_tendency": 95},
        {"suspicion": 70, "hidden_tension": 50},
        ["repeated_deception"],
    )
    text = format_playtest_observation(observation)

    assert observation.event_visibility == "hidden"
    assert observation.event_discovered is False
    assert observation.npc_public_conflict is False
    assert observation.relationship_delta.get("hidden_tension_delta", 0) > 0
    assert observation.npc_followup_risk > 0
    assert "public_conflict: false" in text
    assert "hidden" in text


def _test_positive_support_never_logs_revenge_or_breakup() -> None:
    observation = build_playtest_observation(
        supportive_listening_event(),
        {"revenge_tendency": 95, "forgiveness": 10},
        {"repair_chance": 65},
        ["unresolved_betrayal"],
    )

    assert observation.npc_reaction_type in {"appreciate", "soften"}
    assert observation.npc_reaction_type not in {"retaliate", "breakup_warning"}
    assert observation.npc_public_conflict is False


def _test_same_deception_event_shows_different_personality_reactions() -> None:
    event = _deception_event(discovered=True)
    state = {"trust": 48, "safety": 50, "satisfaction": 55, "repair_chance": 55}

    communicative = build_playtest_observation(
        event,
        {"communication_drive": 90, "forgiveness": 85, "revenge_tendency": 10},
        state,
        [],
    )
    jealous = build_playtest_observation(
        event,
        {"jealousy": 95, "attachment_anxiety": 90, "communication_drive": 40},
        state,
        [],
    )

    assert communicative.event_id == jealous.event_id
    assert communicative.npc_reaction_type != jealous.npc_reaction_type
    assert communicative.npc_reaction_type in {"communicate", "repair_attempt", "forgive"}
    assert jealous.npc_reaction_type in {"confront", "test_player"}
    assert "high_communication_drive" in format_playtest_observation(communicative)
    assert "high_jealousy" in format_playtest_observation(jealous)


def _test_empty_inputs_are_safe_defaults() -> None:
    observation = build_playtest_observation({}, {}, {}, [])
    text = format_playtest_observation(observation)

    _assert_complete_observation(observation)
    assert observation.event_id == "unknown_event"
    assert observation.relationship_state_before["trust"] == 50
    assert observation.npc_personality_snapshot["forgiveness"] == 50
    assert text


def _test_memory_candidate_and_relationship_delta_enter_log() -> None:
    observation = build_playtest_observation(
        _deception_event(discovered=True),
        {"self_respect": 90, "forgiveness": 30},
        {"trust": 25, "safety": 35, "satisfaction": 20},
        ["repeated_deception", "unresolved_betrayal"],
    )
    text = format_playtest_observation(observation)

    assert observation.memory_candidate
    assert observation.relationship_delta
    assert "memory_candidate:" in text
    assert "relationship_delta:" in text
    assert observation.memory_candidate["memory_type"] in text


def main() -> None:
    _test_build_playtest_observation_generates_complete_fields()
    _test_format_playtest_observation_contains_key_sections()
    _test_hidden_undiscovered_event_never_records_public_conflict()
    _test_positive_support_never_logs_revenge_or_breakup()
    _test_same_deception_event_shows_different_personality_reactions()
    _test_empty_inputs_are_safe_defaults()
    _test_memory_candidate_and_relationship_delta_enter_log()

    print("playtest observation test passed")


if __name__ == "__main__":
    main()

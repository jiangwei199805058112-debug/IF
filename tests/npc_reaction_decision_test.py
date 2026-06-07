from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.npc_reaction_decision import (  # noqa: E402
    REACTION_TYPES,
    decide_npc_reaction,
)
from if_game.relationship_event_samples import supportive_listening_event  # noqa: E402


def _dinner_deception(discovered: bool = True) -> dict:
    return {
        "event_id": "E-REACT-DINNER-HIDDEN",
        "event_type": "deception",
        "severity": 70,
        "visibility": "private",
        "discovered": discovered,
        "relationship_delta": {
            "truth_harm_level": 6,
            "deception_level": 7,
            "privacy_boundary_conflict": 4,
        },
        "memory_tags": ["boundary_violation"],
        "context": "Player hid an opposite-gender dinner and the missing context has now surfaced.",
    }


def _repair_event(blame_shift: bool = False) -> dict:
    return {
        "event_id": "E-REACT-REPAIR",
        "event_type": "repair_attempt",
        "severity": 45,
        "visibility": "public",
        "discovered": True,
        "repair_attempt_quality": 8 if not blame_shift else 2,
        "relationship_delta": {
            "repair_attempt_quality": 8 if not blame_shift else 2,
            "validation_skill": 7 if not blame_shift else 1,
            "defensive_response": 0 if not blame_shift else 8,
        },
        "context": "accountable repair" if not blame_shift else "blame_shift defensive repair",
    }


def _test_same_deception_event_varies_by_personality() -> None:
    event = _dinner_deception(discovered=True)
    relationship_state = {"trust": 45, "safety": 45, "satisfaction": 55, "repair_chance": 55}

    communicative = decide_npc_reaction(
        event,
        {
            "communication_drive": 90,
            "forgiveness": 85,
            "revenge_tendency": 10,
            "emotional_stability": 80,
        },
        relationship_state,
        [],
    )
    anxious = decide_npc_reaction(
        event,
        {"jealousy": 92, "attachment_anxiety": 90, "communication_drive": 45},
        relationship_state,
        [],
    )
    avoidant = decide_npc_reaction(
        event,
        {"conflict_avoidance": 95, "communication_drive": 20},
        relationship_state,
        [],
    )
    revenge = decide_npc_reaction(
        event,
        {"revenge_tendency": 95, "forgiveness": 10, "communication_drive": 30},
        {"trust": 25, "safety": 25, "satisfaction": 45, "repair_chance": 25},
        ["repeated_deception"],
    )
    self_respect = decide_npc_reaction(
        event,
        {"self_respect": 95, "forgiveness": 35, "communication_drive": 45},
        {"trust": 25, "safety": 35, "satisfaction": 20, "repair_chance": 20},
        ["repeated_deception", "unresolved_betrayal"],
    )

    assert communicative.reaction_type in {"communicate", "repair_attempt", "forgive"}
    assert anxious.reaction_type in {"confront", "test_player"}
    assert avoidant.reaction_type in {"withdraw", "cold_war", "become_sad"}
    assert revenge.reaction_type == "retaliate"
    assert self_respect.reaction_type == "breakup_warning"
    assert len(
        {
            communicative.reaction_type,
            anxious.reaction_type,
            avoidant.reaction_type,
            revenge.reaction_type,
            self_respect.reaction_type,
        }
    ) >= 4


def _test_high_communication_and_forgiveness_prefers_repair_path() -> None:
    decision = decide_npc_reaction(
        _repair_event(blame_shift=False),
        {"communication_drive": 90, "forgiveness": 90, "revenge_tendency": 5},
        {"repair_chance": 70, "satisfaction": 60},
        [],
    )

    assert decision.reaction_type in {"communicate", "repair_attempt", "forgive", "soften"}
    assert decision.relationship_delta["repair_chance_delta"] > 0
    assert decision.followup_risk < 50


def _test_jealous_anxious_npc_prefers_confront_or_test() -> None:
    decision = decide_npc_reaction(
        _dinner_deception(discovered=True),
        {"jealousy": 95, "attachment_anxiety": 90},
        {"suspicion": 60, "satisfaction": 55},
        [],
    )

    assert decision.reaction_type in {"confront", "test_player"}
    assert decision.public_conflict is True


def _test_avoidant_npc_prefers_withdrawal_or_cold_war() -> None:
    decision = decide_npc_reaction(
        _dinner_deception(discovered=True),
        {"conflict_avoidance": 95, "communication_drive": 15, "emotional_stability": 35},
        {"satisfaction": 50},
        [],
    )

    assert decision.reaction_type in {"withdraw", "cold_war", "become_sad"}


def _test_revenge_only_appears_after_discovered_deception_or_betrayal() -> None:
    personality = {"revenge_tendency": 95, "forgiveness": 10}
    state = {"safety": 20, "satisfaction": 40}
    memories = ["repeated_deception"]

    discovered = decide_npc_reaction(_dinner_deception(discovered=True), personality, state, memories)
    hidden = decide_npc_reaction(_dinner_deception(discovered=False), personality, state, memories)

    assert discovered.reaction_type == "retaliate"
    assert discovered.public_conflict is True
    assert hidden.reaction_type != "retaliate"
    assert hidden.public_conflict is False


def _test_hidden_undiscovered_event_has_no_public_conflict() -> None:
    decision = decide_npc_reaction(
        _dinner_deception(discovered=False),
        {"jealousy": 95, "attachment_anxiety": 90, "revenge_tendency": 95},
        {"suspicion": 70, "hidden_tension": 50},
        ["repeated_deception"],
    )

    assert decision.public_conflict is False
    assert decision.reaction_type in {"record_grievance", "become_sad"}
    assert decision.relationship_delta["hidden_tension_delta"] > 0
    assert decision.relationship_delta["suspicion_delta"] > 0
    assert "internalized_suspicion" in decision.tags


def _test_positive_support_never_generates_revenge_or_breakup() -> None:
    decision = decide_npc_reaction(
        supportive_listening_event(),
        {"revenge_tendency": 95, "forgiveness": 10},
        {"repair_chance": 60},
        ["unresolved_betrayal"],
    )

    assert decision.reaction_type in {"appreciate", "soften"}
    assert decision.reaction_type not in {"retaliate", "breakup_warning"}
    assert decision.relationship_delta["repair_chance_delta"] > 0
    assert decision.public_conflict is False


def _test_repeated_deception_memory_raises_intensity_or_followup_risk() -> None:
    event = _dinner_deception(discovered=True)
    personality = {"communication_drive": 70, "forgiveness": 55}
    state = {"satisfaction": 50, "safety": 50}

    without_memory = decide_npc_reaction(event, personality, state, [])
    with_memory = decide_npc_reaction(event, personality, state, ["repeated_deception"])

    assert (
        with_memory.intensity > without_memory.intensity
        or with_memory.followup_risk > without_memory.followup_risk
    )
    assert "repeated_deception_memory" in with_memory.tags


def _test_missing_inputs_use_safe_defaults() -> None:
    decision = decide_npc_reaction({}, {}, {}, [])
    data = decision.to_dict()

    assert decision.reaction_type in REACTION_TYPES
    assert 0 <= decision.intensity <= 100
    assert isinstance(decision.public_conflict, bool)
    assert isinstance(data["relationship_delta"], dict)
    assert isinstance(data["memory_candidate"], dict)
    assert isinstance(data["tags"], list)


def _test_blame_shift_repair_is_not_treated_as_true_repair() -> None:
    decision = decide_npc_reaction(
        _repair_event(blame_shift=True),
        {"communication_drive": 85, "forgiveness": 90, "self_respect": 80},
        {"repair_chance": 70},
        [],
    )

    assert decision.reaction_type not in {"forgive", "soften"}
    assert decision.relationship_delta["repair_chance_delta"] < 0
    assert "low_quality_repair" in decision.tags


def main() -> None:
    _test_same_deception_event_varies_by_personality()
    _test_high_communication_and_forgiveness_prefers_repair_path()
    _test_jealous_anxious_npc_prefers_confront_or_test()
    _test_avoidant_npc_prefers_withdrawal_or_cold_war()
    _test_revenge_only_appears_after_discovered_deception_or_betrayal()
    _test_hidden_undiscovered_event_has_no_public_conflict()
    _test_positive_support_never_generates_revenge_or_breakup()
    _test_repeated_deception_memory_raises_intensity_or_followup_risk()
    _test_missing_inputs_use_safe_defaults()
    _test_blame_shift_repair_is_not_treated_as_true_repair()

    print("npc reaction decision test passed")


if __name__ == "__main__":
    main()

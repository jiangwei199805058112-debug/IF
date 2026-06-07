from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.playtest_observation_samples import (  # noqa: E402
    SAMPLE_CASES,
    SAMPLE_PERSONALITIES,
    generate_sample_observations,
    observations_for,
    reaction_type_distribution,
    summarize_sample_observations,
)


def _all_observations():
    return generate_sample_observations()


def _first(observations, case_id: str, npc_id: str):
    matches = observations_for(observations, case_id=case_id, npc_id=npc_id)
    assert matches, f"missing {case_id} x {npc_id}"
    return matches[0]


def _test_sample_count_matches_cases_and_personalities() -> None:
    observations = _all_observations()

    assert len(SAMPLE_CASES) >= 6
    assert len(SAMPLE_PERSONALITIES) == 5
    assert len(observations) == len(SAMPLE_CASES) * len(SAMPLE_PERSONALITIES)
    assert len(observations) >= 15


def _test_support_case_never_retaliates_or_warns_breakup() -> None:
    observations = observations_for(_all_observations(), case_id="CASE_SUPPORT")
    reaction_types = {observation.npc_reaction_type for observation in observations}

    assert "retaliate" not in reaction_types
    assert "breakup_warning" not in reaction_types
    assert reaction_types <= {"appreciate", "soften"}


def _test_hidden_privacy_case_has_no_public_conflict() -> None:
    observations = observations_for(_all_observations(), case_id="CASE_PRIVACY_HIDDEN")

    assert observations
    assert all(not observation.npc_public_conflict for observation in observations)
    assert all(observation.event_discovered is False for observation in observations)
    assert all(observation.event_visibility == "hidden" for observation in observations)


def _test_discovered_deception_varies_by_personality() -> None:
    observations = observations_for(_all_observations(), case_id="CASE_DECEPTION_DISCOVERED")
    reaction_types = {observation.npc_reaction_type for observation in observations}

    assert len(reaction_types) >= 2
    assert _first(observations, "CASE_DECEPTION_DISCOVERED", "NPC_A_COMMUNICATOR").npc_reaction_type in {
        "communicate",
        "repair_attempt",
        "forgive",
    }
    assert _first(observations, "CASE_DECEPTION_DISCOVERED", "NPC_B_JEALOUS").npc_reaction_type in {
        "confront",
        "test_player",
    }
    assert _first(observations, "CASE_DECEPTION_DISCOVERED", "NPC_C_AVOIDANT").npc_reaction_type in {
        "withdraw",
        "cold_war",
        "become_sad",
    }


def _test_communicator_and_avoidant_reactions_differ() -> None:
    observations = _all_observations()
    communicator = _first(observations, "CASE_DECEPTION_DISCOVERED", "NPC_A_COMMUNICATOR")
    avoidant = _first(observations, "CASE_DECEPTION_DISCOVERED", "NPC_C_AVOIDANT")

    assert communicator.npc_reaction_type != avoidant.npc_reaction_type
    assert communicator.npc_reaction_type in {"communicate", "repair_attempt", "forgive"}
    assert avoidant.npc_reaction_type in {"withdraw", "cold_war", "become_sad"}


def _test_revengeful_npc_does_not_retaliate_on_support() -> None:
    observations = _all_observations()
    support = _first(observations, "CASE_SUPPORT", "NPC_D_REVENGEFUL")

    assert support.npc_reaction_type != "retaliate"
    assert support.npc_public_conflict is False


def _test_revengeful_npc_retaliates_only_after_discovered_deception() -> None:
    observations = observations_for(_all_observations(), npc_id="NPC_D_REVENGEFUL")
    retaliation_cases = {
        next(tag.removeprefix("case:") for tag in observation.tags if tag.startswith("case:"))
        for observation in observations
        if observation.npc_reaction_type == "retaliate"
    }

    assert retaliation_cases
    assert retaliation_cases <= {"CASE_DECEPTION_DISCOVERED", "CASE_REPEAT_DECEPTION"}


def _test_high_self_respect_sets_boundary_or_warns_under_repeated_deception() -> None:
    observation = _first(
        _all_observations(),
        "CASE_REPEAT_DECEPTION",
        "NPC_E_HIGH_SELF_RESPECT",
    )

    assert observation.npc_reaction_type in {"set_boundary", "breakup_warning"}


def _test_summary_outputs_distribution_and_observations() -> None:
    observations = _all_observations()
    distribution = reaction_type_distribution(observations)
    summary = summarize_sample_observations(observations)

    assert distribution
    assert "reaction_type distribution:" in summary
    assert "key observations:" in summary
    assert "hidden privacy cases have public_conflict=false." in summary
    assert "discovered deception reactions vary:" in summary


def main() -> None:
    _test_sample_count_matches_cases_and_personalities()
    _test_support_case_never_retaliates_or_warns_breakup()
    _test_hidden_privacy_case_has_no_public_conflict()
    _test_discovered_deception_varies_by_personality()
    _test_communicator_and_avoidant_reactions_differ()
    _test_revengeful_npc_does_not_retaliate_on_support()
    _test_revengeful_npc_retaliates_only_after_discovered_deception()
    _test_high_self_respect_sets_boundary_or_warns_under_repeated_deception()
    _test_summary_outputs_distribution_and_observations()

    print("playtest observation samples test passed")


if __name__ == "__main__":
    main()

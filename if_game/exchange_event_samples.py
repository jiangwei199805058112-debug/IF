from __future__ import annotations


def stable_but_bored_event(
    source_id: str = "relationship",
    target_id: str = "player",
) -> dict:
    """E-EXC-01: stable and low-conflict, but lacking novelty."""

    return {
        "event_id": "E-EXC-01",
        "event_type": "relationship_boredom",
        "source_id": source_id,
        "target_id": target_id,
        "relationship_rewards_delta": 1,
        "relationship_costs_delta": -3,
        "approach_reward_delta": 1,
        "avoidance_cost_pressure_delta": -7,
        "boredom_delta": 8,
        "dependence_delta": 1,
        "pattern_key": "boredom_without_repair",
    }


def household_underbenefit_event(
    source_id: str = "relationship",
    target_id: str = "player",
) -> dict:
    """E-EQU-01: one side carries household or emotional labor for too long."""

    return {
        "event_id": "E-EQU-01",
        "event_type": "equity_conflict",
        "source_id": source_id,
        "target_id": target_id,
        "relationship_rewards_delta": -2,
        "relationship_costs_delta": 6,
        "perceived_equity_delta": -6,
        "underbenefit_feeling_delta": 8,
        "taken_for_granted_delta": 7,
        "dependence_delta": -1,
        "pattern_key": "household_underbenefit",
        "occurrence_count": 4,
    }


def equity_repair_event(
    source_id: str = "npc_a",
    target_id: str = "player",
) -> dict:
    """E-EQU-02: partner notices unequal effort and compensates."""

    return {
        "event_id": "E-EQU-02",
        "event_type": "equity_repair",
        "source_id": source_id,
        "target_id": target_id,
        "relationship_rewards_delta": 4,
        "relationship_costs_delta": -2,
        "perceived_equity_delta": 5,
        "felt_appreciation_delta": 8,
        "taken_for_granted_delta": -4,
        "repair_attempt_quality": 5,
        "dependence_delta": 1,
        "pattern_key": "household_underbenefit",
    }

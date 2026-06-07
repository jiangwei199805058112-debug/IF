from __future__ import annotations

from typing import Literal


LateArrivalResponse = Literal["repair", "defensive", "cross_complaining"]


def late_arrival_complaint_event(
    response: LateArrivalResponse = "repair",
    source_id: str = "player",
    target_id: str = "npc_a",
) -> dict:
    """E-CON-01: a lightweight conflict sample for a late-arrival complaint."""

    base = {
        "event_id": "E-CON-01",
        "event_type": "conflict_repair",
        "source_id": source_id,
        "target_id": target_id,
        "truth_harm_level": 2,
    }

    if response == "repair":
        return {
            **base,
            "conflict_response_type": "repair_attempt",
            "conflict_escalation_risk": 2,
            "validation_skill": 8,
            "active_listening_skill": 7,
            "repair_attempt_quality": 8,
            "perceived_responsiveness": 7,
            "pattern_key": "late_arrival_repair",
        }
    if response == "defensive":
        return {
            **base,
            "conflict_response_type": "defensive_explanation",
            "conflict_escalation_risk": 5,
            "defensive_response": 7,
            "validation_skill": 1,
            "repair_attempt_quality": 1,
            "perceived_responsiveness": 2,
            "pattern_key": "conflict_defensiveness",
        }
    if response == "cross_complaining":
        return {
            **base,
            "conflict_response_type": "cross_complaining",
            "conflict_escalation_risk": 7,
            "defensive_response": 5,
            "validation_skill": 0,
            "repair_attempt_quality": 0,
            "perceived_responsiveness": 1,
            "pattern_key": "cross_complaining_loop",
        }

    raise ValueError(f"unsupported late arrival response: {response}")


def timeout_request_event(
    source_id: str = "player",
    target_id: str = "npc_a",
) -> dict:
    """E-CON-02: effective timeout that returns to the conflict."""

    return {
        "event_id": "E-CON-02",
        "event_type": "conflict_timeout",
        "source_id": source_id,
        "target_id": target_id,
        "conflict_response_type": "effective_timeout",
        "conflict_escalation_risk": 2,
        "stonewalling_level": 0,
        "timeout_repair_success": True,
        "repair_attempt_quality": 7,
        "validation_skill": 5,
        "pattern_key": "stonewalling_after_conflict",
    }


def mocking_vulnerability_event(
    source_id: str = "npc_a",
    target_id: str = "player",
) -> dict:
    """E-CON-03: contempt/mockery toward a vulnerable disclosure."""

    return {
        "event_id": "E-CON-03",
        "event_type": "contempt_or_mockery",
        "source_id": source_id,
        "target_id": target_id,
        "conflict_response_type": "contempt",
        "communication_response_type": "mocking_response",
        "conflict_escalation_risk": 6,
        "contempt_signal": 9,
        "truth_harm_level": 6,
        "perceived_responsiveness": 0,
        "repair_attempt_quality": 0,
        "pattern_key": "contempt_or_mockery",
    }

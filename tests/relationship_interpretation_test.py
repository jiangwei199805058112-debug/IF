from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.relationship_interpretation import (
    interpret_relationship_event,
    interpretation_to_aggregator_input,
)
from if_game.relationship_state_aggregator import aggregate_relationship_event


def _credible_busy_event(player_judgment: str = "trust_no_problem") -> dict:
    return {
        "event_id": "late_reply_busy",
        "player_judgment": player_judgment,
        "truth": {
            "truth_type": "busy",
            "truth_reason": "工作会议延长",
            "truth_intention": "无意延迟",
            "truth_harm_level": 10,
            "truth_priority_signal": 8,
            "truth_moral_severity": 0,
        },
        "explanation": {
            "explanation_claim": "刚才一直在开会，手机静音，会议结束才看到。",
            "explanation_specificity": 86,
            "explanation_consistency": 88,
            "explanation_plausibility": 82,
            "behavior_explanation_gap": 4,
            "excuse_repetition_count": 0,
            "supporting_evidence_strength": 20,
        },
        "observable_traces": {},
    }


def _concealment_event(player_judgment: str = "suspect_problem") -> dict:
    return {
        "event_id": "social_media_no_reply",
        "player_judgment": player_judgment,
        "truth": {
            "truth_type": "concealment",
            "truth_reason": "正在和暧昧对象聊天但不想说明",
            "truth_intention": "保留秘密",
            "truth_harm_level": 65,
            "truth_priority_signal": 76,
            "truth_moral_severity": 55,
        },
        "explanation": {
            "explanation_claim": "没看手机",
            "explanation_specificity": 28,
            "explanation_consistency": 42,
            "explanation_plausibility": 45,
            "behavior_explanation_gap": 8,
            "excuse_repetition_count": 2,
        },
        "observable_traces": {
            "online_but_no_reply": True,
            "social_media_updated_but_no_reply": True,
            "message_seen_but_ignored": True,
            "selective_availability": True,
        },
    }


def _assert_score_range(result: dict) -> None:
    assert 0 <= result["evidence_chain_strength"] <= 100
    assert 0 <= result["explanation_layer"]["explanation_credibility"] <= 100
    assert 0 <= result["trust_calibration"] <= 100
    for value in result["relationship_effects"].values():
        assert -100 <= value <= 100


def _aggregate_interpretation(result: dict):
    aggregator_input = interpretation_to_aggregator_input(
        result,
        source_id="npc_a",
        target_id="player",
    )
    return aggregator_input, aggregate_relationship_event(aggregator_input)


def main() -> None:
    accurate = interpret_relationship_event(_concealment_event("suspect_problem"))
    assert accurate["quadrant"]["type"] == "accurate_alertness"
    assert accurate["truth_layer"]["has_real_problem"] is True
    assert accurate["evidence_chain_strength"] >= 50
    assert accurate["explanation_layer"]["explanation_credibility"] < 40
    assert accurate["relationship_effects"]["fact_trust"] < 0
    assert "accurate_alertness" in accurate["report_tags"]
    assert "repeated_excuse_alert" in accurate["report_tags"]
    _assert_score_range(accurate)

    accurate_input, accurate_delta = _aggregate_interpretation(accurate)
    assert accurate_input["source_id"] == "npc_a"
    assert accurate_input["target_id"] == "player"
    assert accurate_input["truth_type"] == "concealment"
    assert accurate_input["truth_harm_level"] > 0
    assert accurate_input["evidence_chain_strength"] > 0
    assert "accurate_alertness" in accurate_delta.report_tags
    assert accurate_delta.trust_delta < 0

    over_suspicion = interpret_relationship_event(_credible_busy_event("suspect_problem"))
    assert over_suspicion["quadrant"]["type"] == "over_suspicion"
    assert over_suspicion["truth_layer"]["has_real_problem"] is False
    assert "over_suspicion" in over_suspicion["report_tags"]
    _assert_score_range(over_suspicion)

    over_suspicion_input, over_suspicion_delta = _aggregate_interpretation(over_suspicion)
    assert over_suspicion_input["truth_harm_level"] <= 3
    assert over_suspicion_input["evidence_chain_strength"] <= 3
    assert over_suspicion_delta.trust_delta >= -3
    assert "over_suspicion_pattern" in over_suspicion_delta.report_tags

    stable = interpret_relationship_event(_credible_busy_event("trust_no_problem"))
    assert stable["quadrant"]["type"] == "stable_trust"
    assert "plausible_explanation_acceptor" in stable["report_tags"]
    assert stable["trust_calibration"] > over_suspicion["trust_calibration"]
    _assert_score_range(stable)

    misplaced = interpret_relationship_event(_concealment_event("trust_no_problem"))
    assert misplaced["quadrant"]["type"] == "misplaced_trust"
    assert "selective_blindness" in misplaced["report_tags"]
    assert misplaced["trust_calibration"] < accurate["trust_calibration"]
    _assert_score_range(misplaced)

    deception_input, deception_delta = _aggregate_interpretation(misplaced)
    assert deception_input["truth_harm_level"] >= 5
    assert deception_input["deception_level"] >= 5
    assert deception_delta.trust_delta < 0
    assert (
        "deception_risk" in deception_delta.report_tags
        or "trust_damage_event" in deception_delta.report_tags
    )

    no_trace = _concealment_event("suspect_problem")
    no_trace["observable_traces"] = {}
    no_trace["explanation"]["excuse_repetition_count"] = 0
    no_trace_result = interpret_relationship_event(no_trace)
    assert accurate["explanation_layer"]["explanation_credibility"] < no_trace_result[
        "explanation_layer"
    ]["explanation_credibility"]

    print("relationship interpretation test passed")


if __name__ == "__main__":
    main()

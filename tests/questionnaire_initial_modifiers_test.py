from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.questionnaire.initial_modifiers import (  # noqa: E402
    MODIFIER_DELTA_FIELDS,
    apply_initial_modifiers,
    build_initial_relationship_modifiers,
    format_initial_modifier_summary,
)
from if_game.questionnaire.loader import load_mvp_questionnaire  # noqa: E402
from if_game.questionnaire.reporting import render_questionnaire_report  # noqa: E402


def _score_result(
    dimension_scores: dict[str, float] | None = None,
    completion_rate: float = 1.0,
) -> dict:
    scores = dimension_scores or {}
    return {
        "dimension_scores": scores,
        "evidence_count": {dimension: 1 for dimension in scores},
        "answered_questions": 1 if scores else 0,
        "total_questions": 29,
        "completion_rate": completion_rate,
    }


def _assert_deltas_bounded(modifiers: dict) -> None:
    for field in MODIFIER_DELTA_FIELDS:
        assert -10 <= modifiers[field] <= 10, field


def _assert_no_diagnostic_language(lines: list[str]) -> None:
    text = "\n".join(lines)
    forbidden_phrases = ["你有病", "你一定会", "你就是", "人格障碍", "病态"]
    for phrase in forbidden_phrases:
        assert phrase not in text


def _test_empty_or_low_completion_result_does_not_crash() -> None:
    empty = build_initial_relationship_modifiers({})
    _assert_deltas_bounded(empty)
    assert all(empty[field] == 0 for field in MODIFIER_DELTA_FIELDS)
    assert format_initial_modifier_summary(empty)

    low_completion = build_initial_relationship_modifiers(
        _score_result({"trust_suspicion_sensitivity": 100}, completion_rate=0.1)
    )
    _assert_deltas_bounded(low_completion)
    assert low_completion["suspicion_sensitivity_delta"] <= 2


def _test_high_suspicion_sensitivity_increases_modifier() -> None:
    modifiers = build_initial_relationship_modifiers(
        _score_result({"trust_suspicion_sensitivity": 90})
    )
    assert modifiers["suspicion_sensitivity_delta"] > 0


def _test_high_reassurance_need_increases_modifier() -> None:
    modifiers = build_initial_relationship_modifiers(
        _score_result({"emotion_reassurance_need": 90})
    )
    assert modifiers["reassurance_need_delta"] > 0


def _test_high_repair_initiative_increases_modifier() -> None:
    modifiers = build_initial_relationship_modifiers(
        _score_result({"communication_repair_initiative": 90})
    )
    assert modifiers["conflict_repair_tendency_delta"] > 0


def _test_privacy_and_independence_affect_boundary_sensitivity() -> None:
    privacy = build_initial_relationship_modifiers(
        _score_result({"digital_phone_privacy_need": 90})
    )
    independence = build_initial_relationship_modifiers(
        _score_result({"attachment_independence_need": 90})
    )
    assert privacy["privacy_boundary_sensitivity_delta"] > 0
    assert independence["privacy_boundary_sensitivity_delta"] > 0


def _test_apply_initial_modifiers_returns_state_copy() -> None:
    modifiers = build_initial_relationship_modifiers(
        _score_result(
            {
                "trust_baseline": 80,
                "emotion_reassurance_need": 90,
                "trust_suspicion_sensitivity": 90,
            }
        )
    )
    base_state = {"trust_baseline": 8, "initial_report_tags": ["existing_tag"]}
    applied = apply_initial_modifiers(base_state, modifiers)
    assert applied is not base_state
    assert applied["trust_baseline"] <= 10
    assert "existing_tag" in applied["initial_report_tags"]
    assert applied["questionnaire_initial_modifiers"]["reassurance_need_delta"] > 0


def _test_summary_has_no_diagnostic_language() -> None:
    modifiers = build_initial_relationship_modifiers(
        _score_result(
            {
                "trust_suspicion_sensitivity": 90,
                "emotion_reassurance_need": 90,
                "communication_repair_initiative": 90,
                "digital_phone_privacy_need": 90,
            }
        )
    )
    summaries = format_initial_modifier_summary(modifiers)
    assert summaries
    _assert_no_diagnostic_language(summaries)


def _test_reporting_includes_initial_modifier_summary() -> None:
    config = load_mvp_questionnaire()
    score_result = _score_result(
        {
            "trust_suspicion_sensitivity": 90,
            "emotion_reassurance_need": 90,
            "digital_phone_privacy_need": 90,
        }
    )
    report = render_questionnaire_report(config, [], score_result)
    assert "游戏初始倾向修正摘要" in report
    assert "这些只是开局倾向" in report
    _assert_no_diagnostic_language(report.splitlines())


def main() -> None:
    _test_empty_or_low_completion_result_does_not_crash()
    _test_high_suspicion_sensitivity_increases_modifier()
    _test_high_reassurance_need_increases_modifier()
    _test_high_repair_initiative_increases_modifier()
    _test_privacy_and_independence_affect_boundary_sensitivity()
    _test_apply_initial_modifiers_returns_state_copy()
    _test_summary_has_no_diagnostic_language()
    _test_reporting_includes_initial_modifier_summary()

    print("questionnaire initial modifiers test passed")


if __name__ == "__main__":
    main()

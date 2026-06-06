from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.questionnaire.loader import load_mvp_questionnaire
from if_game.questionnaire.reporting import render_questionnaire_report
from if_game.questionnaire.scoring import score_questionnaire


HIGH_NEED_ANSWERS = [
    {"question_id": "Q001", "primary_choice": "strong_ambiguous", "confidence": 80},
    {"question_id": "Q004", "primary_choice": "daily_messages", "confidence": 80},
    {
        "question_id": "Q017",
        "primary_choice": "ask_why",
        "secondary_choices": ["check_clues"],
        "confidence": 80,
    },
    {"question_id": "Q018", "axis_x": 75, "axis_y": 65, "confidence": 75},
    {"question_id": "Q019", "slider_value": 85, "confidence": 75},
    {"question_id": "Q020", "slider_value": 30, "confidence": 75},
    {
        "question_id": "Q021",
        "primary_choice": "pretend_ok",
        "secondary_choices": ["tell_directly"],
        "confidence": 70,
    },
    {"question_id": "Q023", "primary_choice": "careful_reliance", "confidence": 70},
    {"question_id": "Q026", "slider_value": 80, "confidence": 80},
    {
        "question_id": "Q030",
        "primary_choice": "needs_stable_response",
        "selected_choices": ["needs_stable_response", "needs_space", "hides_needs"],
        "confidence": 70,
    },
]

LOW_NEED_ANSWERS = [
    {"question_id": "Q001", "primary_choice": "plain_chat", "confidence": 80},
    {"question_id": "Q004", "primary_choice": "irregular_contact", "confidence": 80},
    {"question_id": "Q017", "primary_choice": "assume_busy", "secondary_choices": [], "confidence": 80},
    {"question_id": "Q018", "axis_x": 25, "axis_y": 30, "confidence": 75},
    {"question_id": "Q019", "slider_value": 20, "confidence": 75},
    {"question_id": "Q020", "slider_value": 85, "confidence": 75},
    {"question_id": "Q021", "primary_choice": "tell_directly", "secondary_choices": [], "confidence": 70},
    {"question_id": "Q023", "primary_choice": "natural_reliance", "confidence": 70},
    {"question_id": "Q026", "slider_value": 40, "confidence": 80},
    {
        "question_id": "Q030",
        "primary_choice": "usually_stable",
        "selected_choices": ["usually_stable"],
        "confidence": 70,
    },
]


def _render(config: dict, answers: list[dict]) -> str:
    score_result = score_questionnaire(config, answers)
    return render_questionnaire_report(config, answers, score_result)


def _key_dimension_section(report: str) -> str:
    start = report.index("## 关键维度摘要")
    end = report.index("## 亲密依恋摘要")
    return report[start:end]


def main() -> None:
    config = load_mvp_questionnaire()
    report = _render(config, HIGH_NEED_ANSWERS)

    assert isinstance(report, str)
    assert report.strip()
    assert "IF 问卷 MVP 报告" in report
    assert "完成度" in report
    assert "关键维度" in report
    assert "后续游戏行为" in report

    forbidden_phrases = ["你有病", "你一定会", "你就是某种人格"]
    for phrase in forbidden_phrases:
        assert phrase not in report

    alternate_report = _render(config, LOW_NEED_ANSWERS)
    assert _key_dimension_section(report) != _key_dimension_section(alternate_report)

    print("questionnaire reporting test passed")


if __name__ == "__main__":
    main()

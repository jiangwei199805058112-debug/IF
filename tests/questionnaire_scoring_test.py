from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.questionnaire.loader import load_mvp_questionnaire
from if_game.questionnaire.scoring import score_questionnaire


CORE_DIMENSIONS = [
    "attachment_abandonment_anxiety",
    "attachment_intimacy_avoidance",
    "attachment_closeness_need",
    "attachment_independence_need",
    "attachment_vulnerability_fear",
]


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


def main() -> None:
    config = load_mvp_questionnaire()
    result = score_questionnaire(config, HIGH_NEED_ANSWERS)

    assert result["answered_questions"] == len(HIGH_NEED_ANSWERS)
    assert result["completion_rate"] == 1.0

    dimension_scores = result["dimension_scores"]
    evidence_count = result["evidence_count"]

    for dimension in CORE_DIMENSIONS:
        assert dimension in dimension_scores
        assert dimension in evidence_count
        assert 0 <= dimension_scores[dimension] <= 100

    alternate_result = score_questionnaire(config, LOW_NEED_ANSWERS)
    assert (
        result["dimension_scores"]["attachment_abandonment_anxiety"]
        != alternate_result["dimension_scores"]["attachment_abandonment_anxiety"]
    )

    print("questionnaire scoring test passed")


if __name__ == "__main__":
    main()

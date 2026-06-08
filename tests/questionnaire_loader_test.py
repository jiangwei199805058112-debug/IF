from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.questionnaire.loader import load_mvp_questionnaire


def main() -> None:
    questionnaire = load_mvp_questionnaire()
    questions = questionnaire["questions"]

    assert len(questions) == 29

    question_ids = [question["id"] for question in questions]
    assert len(question_ids) == len(set(question_ids))
    assert {"Q-COM-01", "Q-COM-05", "Q-COM-06", "Q-COM-10"}.issubset(question_ids)
    question_by_id = {question["id"]: question for question in questions}
    assert question_by_id["Q024"]["selection_mode"] == "primary_with_secondary"
    assert question_by_id["Q024"]["question_type"] == "primary_with_secondary"

    for question in questions:
        assert question.get("selection_mode"), f"{question['id']} missing selection_mode"
        assert question.get("dimensions"), f"{question['id']} missing dimensions"

    print("questionnaire loader test passed")


if __name__ == "__main__":
    main()

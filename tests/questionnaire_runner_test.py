from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.questionnaire.loader import load_mvp_questionnaire
from if_game.questionnaire.runner import (
    QuestionnaireRunnerInputError,
    build_answer_from_input,
    run_questionnaire,
)
from if_game.questionnaire.scoring import score_questionnaire
from if_game.questionnaire.reporting import render_questionnaire_report


RAW_ANSWERS = {
    "Q001": "3",
    "Q002": "4",
    "Q003": "3",
    "Q004": "2",
    "Q005": "5",
    "Q007": "5",
    "Q008": "1,3,4",
    "Q009": "5",
    "Q010": "3,1",
    "Q012": "25",
    "Q013": "1,2,4",
    "Q014": "1,2,5",
    "Q015": "1,5,2",
    "Q016": "3,4",
    "Q017": "3,5",
    "Q018": "75,65",
    "Q019": "85",
    "Q020": "30",
    "Q021": "3,1",
    "Q022": "85",
    "Q023": "2",
    "Q024": "2",
    "Q025": "2,1,4",
    "Q026": "80",
    "Q030": "1,3,4",
    "Q-COM-01": "1",
    "Q-COM-05": "2,1",
    "Q-COM-06": "10,1,7",
    "Q-COM-10": "30,90",
}


def _question_by_id(config: dict, question_id: str) -> dict:
    for question in config["questions"]:
        if question["id"] == question_id:
            return question
    raise AssertionError(f"missing question {question_id}")


def _assert_invalid(question: dict, raw_input: str) -> None:
    try:
        build_answer_from_input(question, raw_input)
    except QuestionnaireRunnerInputError:
        return
    raise AssertionError(f"expected invalid input for {question['id']}: {raw_input}")


def main() -> None:
    config = load_mvp_questionnaire()
    assert len(config["questions"]) == 29
    assert set(RAW_ANSWERS) == {question["id"] for question in config["questions"]}

    forced_single = build_answer_from_input(_question_by_id(config, "Q001"), "1")
    assert forced_single["primary_choice"] == "plain_chat"
    forced_single_value = build_answer_from_input(_question_by_id(config, "Q001"), "a")
    assert forced_single_value["primary_choice"] == "plain_chat"

    primary_with_secondary = build_answer_from_input(_question_by_id(config, "Q017"), "3,5")
    assert primary_with_secondary["primary_choice"] == "ask_why"
    assert primary_with_secondary["secondary_choices"] == ["check_clues"]

    slider = build_answer_from_input(_question_by_id(config, "Q019"), "85")
    assert slider["slider_value"] == 85

    axis = build_answer_from_input(_question_by_id(config, "Q018"), "75 65")
    assert axis["axis_x"] == 75
    assert axis["axis_y"] == 65

    multi_with_primary = build_answer_from_input(_question_by_id(config, "Q030"), "1,3,4")
    assert multi_with_primary["primary_choice"] == "needs_stable_response"
    assert multi_with_primary["selected_choices"] == [
        "needs_stable_response",
        "needs_space",
        "hides_needs",
    ]

    communication_multi = build_answer_from_input(_question_by_id(config, "Q-COM-06"), "10,1,7")
    assert communication_multi["primary_choice"] == "full_transparency"
    assert communication_multi["selected_choices"] == [
        "full_transparency",
        "ex_contact",
        "opposite_sex_friends",
    ]

    communication_axis = build_answer_from_input(_question_by_id(config, "Q-COM-10"), "30,90")
    assert communication_axis["axis_x"] == 30
    assert communication_axis["axis_y"] == 90

    _assert_invalid(_question_by_id(config, "Q001"), "1,2")
    _assert_invalid(_question_by_id(config, "Q019"), "101")
    _assert_invalid(_question_by_id(config, "Q018"), "50")
    _assert_invalid(_question_by_id(config, "Q030"), "99")
    _assert_invalid(_question_by_id(config, "Q-COM-06"), "11")

    parsed_answers = [
        build_answer_from_input(question, RAW_ANSWERS[question["id"]])
        for question in config["questions"]
    ]
    score_result = score_questionnaire(config, parsed_answers)
    report = render_questionnaire_report(config, parsed_answers, score_result)
    assert "IF 问卷 MVP 报告" in report
    assert "游戏初始倾向修正摘要" in report
    assert score_result["answered_questions"] == len(config["questions"])

    raw_inputs = iter(RAW_ANSWERS[question["id"]] for question in config["questions"])
    printed_lines: list[str] = []
    runner_report = run_questionnaire(
        config=config,
        input_func=lambda _prompt: next(raw_inputs),
        output_func=printed_lines.append,
    )
    assert "IF 问卷 MVP 报告" in runner_report
    assert "游戏初始倾向修正摘要" in runner_report
    assert any("IF 问卷 MVP 控制台" in line for line in printed_lines)

    print("questionnaire runner test passed")


if __name__ == "__main__":
    main()

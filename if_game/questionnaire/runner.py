from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from typing import Any

from if_game.questionnaire.loader import load_mvp_questionnaire
from if_game.questionnaire.reporting import render_questionnaire_report
from if_game.questionnaire.scoring import score_questionnaire


InputFunc = Callable[[str], str]
OutputFunc = Callable[[str], None]

TOKEN_SPLIT_PATTERN = re.compile(r"[\s,，、;；|/：:]+")


class QuestionnaireRunnerInputError(ValueError):
    """Raised when console input cannot be converted into an answer record."""


def build_answer_from_input(question: dict[str, Any], raw_input: str) -> dict[str, Any]:
    selection_mode = question.get("selection_mode")

    if selection_mode == "forced_single":
        return _parse_forced_single(question, raw_input)
    if selection_mode == "primary_with_secondary":
        return _parse_primary_with_secondary(question, raw_input)
    if selection_mode == "multi_with_primary":
        return _parse_multi_with_primary(question, raw_input)
    if selection_mode == "slider":
        return _parse_slider(question, raw_input)
    if selection_mode == "axis_2d":
        return _parse_axis_2d(question, raw_input)

    raise QuestionnaireRunnerInputError(f"当前 MVP runner 不支持题型：{selection_mode}")


def run_questionnaire(
    config: dict[str, Any] | None = None,
    input_func: InputFunc = input,
    output_func: OutputFunc = print,
) -> str:
    return collect_questionnaire_result(config, input_func, output_func)["report"]


def collect_questionnaire_result(
    config: dict[str, Any] | None = None,
    input_func: InputFunc = input,
    output_func: OutputFunc = print,
) -> dict[str, Any]:
    questionnaire = config if config is not None else load_mvp_questionnaire()
    questions = questionnaire.get("questions", [])

    output_func("IF 问卷 MVP 控制台")
    output_func("请按题目提示输入选项序号或 0-100 数值。")

    answers: list[dict[str, Any]] = []
    for index, question in enumerate(questions, start=1):
        answer = _read_answer(question, index, len(questions), input_func, output_func)
        answers.append(answer)

    score_result = score_questionnaire(questionnaire, answers)
    report = render_questionnaire_report(questionnaire, answers, score_result)

    output_func("")
    output_func(report)
    return {
        "questionnaire": questionnaire,
        "answers": answers,
        "score_result": score_result,
        "report": report,
    }


def main() -> None:
    run_questionnaire()


def _read_answer(
    question: dict[str, Any],
    index: int,
    total: int,
    input_func: InputFunc,
    output_func: OutputFunc,
) -> dict[str, Any]:
    _print_question(question, index, total, output_func)
    while True:
        raw_input = input_func("请输入：")
        try:
            return build_answer_from_input(question, raw_input)
        except QuestionnaireRunnerInputError as error:
            output_func(f"输入有误：{error} 请重新输入。")


def _print_question(
    question: dict[str, Any],
    index: int,
    total: int,
    output_func: OutputFunc,
) -> None:
    output_func("")
    output_func(f"第 {index}/{total} 题 {question.get('id')}：{question.get('title')}")
    output_func(str(question.get("prompt", "")))

    selection_mode = question.get("selection_mode")
    if selection_mode in {"forced_single", "primary_with_secondary", "multi_with_primary"}:
        _print_options(question, output_func)
    elif selection_mode == "slider":
        _print_scale(question, output_func)
    elif selection_mode == "axis_2d":
        _print_axis(question, output_func)

    output_func(_input_hint(selection_mode))


def _print_options(question: dict[str, Any], output_func: OutputFunc) -> None:
    for index, option in enumerate(question.get("options", []), start=1):
        value = option.get("value", "")
        label = option.get("label", "")
        output_func(f"{index}. {value} {label}".rstrip())


def _print_scale(question: dict[str, Any], output_func: OutputFunc) -> None:
    scale = question.get("scale", {})
    minimum = scale.get("min", 0)
    maximum = scale.get("max", 100)
    min_label = scale.get("min_label", scale.get("left_label", "低"))
    max_label = scale.get("max_label", scale.get("right_label", "高"))
    output_func(f"范围：{minimum}-{maximum}")
    output_func(f"{minimum}：{min_label}")
    output_func(f"{maximum}：{max_label}")


def _print_axis(question: dict[str, Any], output_func: OutputFunc) -> None:
    axis = question.get("axis", {})
    axis_x = axis.get("x", {})
    axis_y = axis.get("y", {})
    output_func(
        f"X 轴 {axis_x.get('min', 0)}-{axis_x.get('max', 100)}："
        f"{axis_x.get('left_label', '左')} -> {axis_x.get('right_label', '右')}"
    )
    output_func(
        f"Y 轴 {axis_y.get('min', 0)}-{axis_y.get('max', 100)}："
        f"{axis_y.get('left_label', '左')} -> {axis_y.get('right_label', '右')}"
    )


def _input_hint(selection_mode: Any) -> str:
    if selection_mode == "forced_single":
        return "输入一个选项序号，例如：1"
    if selection_mode == "primary_with_secondary":
        return "输入主选项序号，可追加次选项，例如：3 或 3,5"
    if selection_mode == "multi_with_primary":
        return "输入多个选项序号，第一个视为主因，例如：1,3,4"
    if selection_mode == "slider":
        return "输入 0-100 的数值，例如：75"
    if selection_mode == "axis_2d":
        return "输入 X 和 Y 两个 0-100 数值，例如：70,40"
    return "输入答案"


def _parse_forced_single(question: dict[str, Any], raw_input: str) -> dict[str, Any]:
    tokens = _split_tokens(raw_input)
    if len(tokens) != 1:
        raise QuestionnaireRunnerInputError("该题只能选择一个选项")

    return _base_answer(question) | {"primary_choice": _option_id_from_token(question, tokens[0])}


def _parse_primary_with_secondary(question: dict[str, Any], raw_input: str) -> dict[str, Any]:
    tokens = _split_tokens(raw_input)
    primary_choice = _option_id_from_token(question, tokens[0])
    secondary_choices = _unique_choices(
        _option_id_from_token(question, token) for token in tokens[1:]
    )
    secondary_choices = [choice for choice in secondary_choices if choice != primary_choice]

    return _base_answer(question) | {
        "primary_choice": primary_choice,
        "secondary_choices": secondary_choices,
    }


def _parse_multi_with_primary(question: dict[str, Any], raw_input: str) -> dict[str, Any]:
    tokens = _split_tokens(raw_input)
    primary_choice = _option_id_from_token(question, tokens[0])
    selected_choices = _unique_choices(_option_id_from_token(question, token) for token in tokens)
    if primary_choice not in selected_choices:
        selected_choices.insert(0, primary_choice)

    return _base_answer(question) | {
        "primary_choice": primary_choice,
        "selected_choices": selected_choices,
    }


def _parse_slider(question: dict[str, Any], raw_input: str) -> dict[str, Any]:
    value = _parse_single_number(raw_input, "滑条题需要输入一个数值")
    scale = question.get("scale", {})
    _validate_range(value, scale, "slider_value")
    return _base_answer(question) | {"slider_value": value}


def _parse_axis_2d(question: dict[str, Any], raw_input: str) -> dict[str, Any]:
    tokens = _split_tokens(raw_input)
    if len(tokens) != 2:
        raise QuestionnaireRunnerInputError("二维坐标题需要输入 X 和 Y 两个数值")

    axis_x = _parse_number(tokens[0])
    axis_y = _parse_number(tokens[1])
    axis = question.get("axis", {})
    _validate_range(axis_x, axis.get("x", {}), "axis_x")
    _validate_range(axis_y, axis.get("y", {}), "axis_y")

    return _base_answer(question) | {"axis_x": axis_x, "axis_y": axis_y}


def _base_answer(question: dict[str, Any]) -> dict[str, Any]:
    question_id = question.get("id")
    selection_mode = question.get("selection_mode")
    if not isinstance(question_id, str) or not question_id:
        raise QuestionnaireRunnerInputError("题目缺少有效 id")
    if not isinstance(selection_mode, str) or not selection_mode:
        raise QuestionnaireRunnerInputError("题目缺少有效 selection_mode")
    return {"question_id": question_id, "selection_mode": selection_mode}


def _split_tokens(raw_input: str) -> list[str]:
    if not isinstance(raw_input, str):
        raise QuestionnaireRunnerInputError("输入必须是文本")
    tokens = [token for token in TOKEN_SPLIT_PATTERN.split(raw_input.strip()) if token]
    if not tokens:
        raise QuestionnaireRunnerInputError("输入不能为空")
    return tokens


def _option_id_from_token(question: dict[str, Any], token: str) -> str:
    options = question.get("options", [])
    if not isinstance(options, list) or not options:
        raise QuestionnaireRunnerInputError("该题没有可选项")

    normalized = token.strip()
    normalized_lower = normalized.lower()
    if normalized.isdigit():
        option_index = int(normalized) - 1
        if 0 <= option_index < len(options):
            option_id = options[option_index].get("id")
            if isinstance(option_id, str) and option_id:
                return option_id

    for option in options:
        if not isinstance(option, dict):
            continue
        candidates = {str(option.get("id", "")), str(option.get("value", ""))}
        lower_candidates = {candidate.lower() for candidate in candidates}
        if normalized in candidates or normalized_lower in lower_candidates:
            option_id = option.get("id")
            if isinstance(option_id, str) and option_id:
                return option_id

    raise QuestionnaireRunnerInputError(f"未找到选项：{token}")


def _unique_choices(choices: Iterable[str]) -> list[str]:
    unique: list[str] = []
    for choice in choices:
        if choice not in unique:
            unique.append(choice)
    return unique


def _parse_single_number(raw_input: str, error_message: str) -> float:
    tokens = _split_tokens(raw_input)
    if len(tokens) != 1:
        raise QuestionnaireRunnerInputError(error_message)
    return _parse_number(tokens[0])


def _parse_number(token: str) -> float:
    try:
        return float(token)
    except ValueError as exc:
        raise QuestionnaireRunnerInputError(f"不是有效数值：{token}") from exc


def _validate_range(value: float, range_config: Any, field: str) -> None:
    minimum = 0.0
    maximum = 100.0
    if isinstance(range_config, dict):
        minimum = float(range_config.get("min", minimum))
        maximum = float(range_config.get("max", maximum))

    if not minimum <= value <= maximum:
        raise QuestionnaireRunnerInputError(f"{field} 必须在 {minimum:g}-{maximum:g} 之间")


if __name__ == "__main__":
    main()

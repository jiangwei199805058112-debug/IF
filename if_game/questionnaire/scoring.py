from __future__ import annotations

from collections.abc import Iterable
from typing import Any


DEFAULT_DIMENSION_SCORE = 50.0
MIN_DIMENSION_SCORE = 0.0
MAX_DIMENSION_SCORE = 100.0
PRIMARY_CHOICE_WEIGHT = 1.0
SECONDARY_CHOICE_WEIGHT = 0.3
MULTI_OTHER_CHOICE_WEIGHT = 0.45


class QuestionnaireScoringError(ValueError):
    """Raised when answers cannot be scored against a questionnaire config."""


def score_questionnaire(config: dict[str, Any], answers: Iterable[dict[str, Any]]) -> dict[str, Any]:
    questions = config.get("questions", [])
    if not isinstance(questions, list):
        raise QuestionnaireScoringError("questionnaire config must contain questions list")

    question_by_id = _index_questions(questions)
    dimension_scores = _initial_dimension_scores(config, questions)
    evidence_count = {dimension: 0 for dimension in dimension_scores}
    answered_question_ids: set[str] = set()

    for answer in answers:
        if not isinstance(answer, dict):
            raise QuestionnaireScoringError("answer record must be an object")

        question_id = answer.get("question_id")
        if question_id not in question_by_id:
            raise QuestionnaireScoringError(f"unknown question_id: {question_id}")
        if question_id in answered_question_ids:
            raise QuestionnaireScoringError(f"duplicate answer for question_id: {question_id}")

        question = question_by_id[question_id]
        touched_dimensions = _score_answer(config, question, answer, dimension_scores)
        for dimension in touched_dimensions:
            evidence_count[dimension] += 1
        answered_question_ids.add(question_id)

    total_questions = len(questions)
    answered_questions = len(answered_question_ids)
    completion_rate = answered_questions / total_questions if total_questions else 0.0

    return {
        "dimension_scores": {
            dimension: round(score, 2) for dimension, score in sorted(dimension_scores.items())
        },
        "evidence_count": dict(sorted(evidence_count.items())),
        "answered_questions": answered_questions,
        "total_questions": total_questions,
        "completion_rate": round(completion_rate, 4),
    }


def _index_questions(questions: list[Any]) -> dict[str, dict[str, Any]]:
    question_by_id: dict[str, dict[str, Any]] = {}
    for question in questions:
        if not isinstance(question, dict):
            raise QuestionnaireScoringError("question must be an object")
        question_id = question.get("id")
        if not isinstance(question_id, str) or not question_id:
            raise QuestionnaireScoringError("question missing id")
        if question_id in question_by_id:
            raise QuestionnaireScoringError(f"duplicate question id: {question_id}")
        question_by_id[question_id] = question
    return question_by_id


def _initial_dimension_scores(config: dict[str, Any], questions: list[dict[str, Any]]) -> dict[str, float]:
    meta = config.get("questionnaire_meta", {})
    default_score = float(meta.get("default_dimension_score", DEFAULT_DIMENSION_SCORE))

    dimensions: set[str] = set()
    for question in questions:
        for dimension in question.get("dimensions", []):
            if isinstance(dimension, str) and dimension:
                dimensions.add(dimension)
        for effects in _question_dimension_effects(question).values():
            if isinstance(effects, dict):
                dimensions.update(dimension for dimension in effects if isinstance(dimension, str))

    return {dimension: default_score for dimension in sorted(dimensions)}


def _score_answer(
    config: dict[str, Any],
    question: dict[str, Any],
    answer: dict[str, Any],
    dimension_scores: dict[str, float],
) -> set[str]:
    selection_mode = question.get("selection_mode")
    base_weight = _base_weight(config, question)
    confidence_factor = _confidence_factor(question, answer)

    if selection_mode == "forced_single":
        return _score_single_choice(question, answer, dimension_scores, base_weight, confidence_factor)
    if selection_mode == "primary_with_secondary":
        return _score_primary_with_secondary(
            question, answer, dimension_scores, base_weight, confidence_factor
        )
    if selection_mode == "multi_with_primary":
        return _score_multi_with_primary(question, answer, dimension_scores, base_weight, confidence_factor)
    if selection_mode == "slider":
        return _score_slider(question, answer, dimension_scores, base_weight, confidence_factor)
    if selection_mode == "axis_2d":
        return _score_axis_2d(question, answer, dimension_scores, base_weight, confidence_factor)

    raise QuestionnaireScoringError(f"unsupported selection_mode for MVP scoring: {selection_mode}")


def _score_single_choice(
    question: dict[str, Any],
    answer: dict[str, Any],
    dimension_scores: dict[str, float],
    base_weight: float,
    confidence_factor: float,
) -> set[str]:
    choice_id = _required_choice(answer, "primary_choice", question["id"])
    return _apply_choice_effects(
        question, choice_id, PRIMARY_CHOICE_WEIGHT * base_weight * confidence_factor, dimension_scores
    )


def _score_primary_with_secondary(
    question: dict[str, Any],
    answer: dict[str, Any],
    dimension_scores: dict[str, float],
    base_weight: float,
    confidence_factor: float,
) -> set[str]:
    touched = _score_single_choice(question, answer, dimension_scores, base_weight, confidence_factor)

    for choice_id in _optional_choice_list(answer, "secondary_choices"):
        touched.update(
            _apply_choice_effects(
                question, choice_id, SECONDARY_CHOICE_WEIGHT * base_weight * confidence_factor, dimension_scores
            )
        )

    return touched


def _score_multi_with_primary(
    question: dict[str, Any],
    answer: dict[str, Any],
    dimension_scores: dict[str, float],
    base_weight: float,
    confidence_factor: float,
) -> set[str]:
    primary_choice = _required_choice(answer, "primary_choice", question["id"])
    selected_choices = _optional_choice_list(answer, "selected_choices")
    if primary_choice not in selected_choices:
        selected_choices.insert(0, primary_choice)

    touched: set[str] = set()
    for choice_id in selected_choices:
        choice_weight = PRIMARY_CHOICE_WEIGHT if choice_id == primary_choice else MULTI_OTHER_CHOICE_WEIGHT
        touched.update(
            _apply_choice_effects(
                question, choice_id, choice_weight * base_weight * confidence_factor, dimension_scores
            )
        )

    return touched


def _score_slider(
    question: dict[str, Any],
    answer: dict[str, Any],
    dimension_scores: dict[str, float],
    base_weight: float,
    confidence_factor: float,
) -> set[str]:
    value = _required_number(answer, "slider_value", question["id"])
    centered = _centered_value(value, question.get("scale", {}))
    effects = _question_dimension_effects(question).get("slider", {})
    if not effects:
        raise QuestionnaireScoringError(f"question {question['id']} missing slider effects")
    return _apply_effects(effects, centered * base_weight * confidence_factor, dimension_scores)


def _score_axis_2d(
    question: dict[str, Any],
    answer: dict[str, Any],
    dimension_scores: dict[str, float],
    base_weight: float,
    confidence_factor: float,
) -> set[str]:
    axis = question.get("axis", {})
    axis_x = _required_number(answer, "axis_x", question["id"])
    axis_y = _required_number(answer, "axis_y", question["id"])
    x_centered = _centered_value(axis_x, axis.get("x", {}))
    y_centered = _centered_value(axis_y, axis.get("y", {}))

    dimension_effects = _question_dimension_effects(question)
    touched = _apply_effects(
        dimension_effects.get("axis_x", {}),
        x_centered * base_weight * confidence_factor,
        dimension_scores,
    )
    touched.update(
        _apply_effects(
            dimension_effects.get("axis_y", {}),
            y_centered * base_weight * confidence_factor,
            dimension_scores,
        )
    )
    if not touched:
        raise QuestionnaireScoringError(f"question {question['id']} missing axis effects")
    return touched


def _base_weight(config: dict[str, Any], question: dict[str, Any]) -> float:
    scoring = question.get("scoring", {})
    if "base_weight" in scoring:
        return float(scoring["base_weight"])

    global_scoring = config.get("scoring", {})
    selection_weights = global_scoring.get("selection_mode_weights", {})
    return float(selection_weights.get(question.get("selection_mode"), 1.0))


def _confidence_factor(question: dict[str, Any], answer: dict[str, Any]) -> float:
    confidence_config = question.get("confidence", {})
    if confidence_config.get("enabled") is False or confidence_config.get("affects_weight") is False:
        return 1.0

    raw_confidence = answer.get("confidence", confidence_config.get("default", 100))
    confidence = max(0.0, min(100.0, float(raw_confidence)))
    if confidence <= 30:
        return 0.45
    if confidence <= 60:
        return 0.7
    if confidence <= 85:
        return 1.0
    return 1.05


def _question_dimension_effects(question: dict[str, Any]) -> dict[str, Any]:
    scoring = question.get("scoring", {})
    effects = scoring.get("dimension_effects", {})
    return effects if isinstance(effects, dict) else {}


def _choice_effects(question: dict[str, Any], choice_id: str) -> dict[str, float]:
    effects = _question_dimension_effects(question).get(choice_id)
    if isinstance(effects, dict):
        return effects

    for option in question.get("options", []):
        if not isinstance(option, dict) or option.get("id") != choice_id:
            continue
        option_effects = option.get("dimension_effects")
        if isinstance(option_effects, dict):
            return option_effects
        option_scoring = option.get("scoring", {})
        nested_effects = option_scoring.get("dimension_effects")
        if isinstance(nested_effects, dict):
            return nested_effects

    raise QuestionnaireScoringError(f"question {question['id']} has unknown choice: {choice_id}")


def _apply_choice_effects(
    question: dict[str, Any],
    choice_id: str,
    multiplier: float,
    dimension_scores: dict[str, float],
) -> set[str]:
    return _apply_effects(_choice_effects(question, choice_id), multiplier, dimension_scores)


def _apply_effects(
    effects: dict[str, Any],
    multiplier: float,
    dimension_scores: dict[str, float],
) -> set[str]:
    touched: set[str] = set()
    for dimension, raw_effect in effects.items():
        effect = float(raw_effect)
        if effect == 0:
            continue
        dimension_scores.setdefault(dimension, DEFAULT_DIMENSION_SCORE)
        dimension_scores[dimension] = _clamp_score(dimension_scores[dimension] + effect * multiplier)
        touched.add(dimension)
    return touched


def _centered_value(value: float, scale: Any) -> float:
    minimum = float(scale.get("min", 0)) if isinstance(scale, dict) else 0.0
    maximum = float(scale.get("max", 100)) if isinstance(scale, dict) else 100.0
    if maximum <= minimum:
        raise QuestionnaireScoringError("scale max must be greater than min")

    clamped = max(minimum, min(maximum, value))
    midpoint = (minimum + maximum) / 2
    half_range = (maximum - minimum) / 2
    return (clamped - midpoint) / half_range


def _clamp_score(score: float) -> float:
    return max(MIN_DIMENSION_SCORE, min(MAX_DIMENSION_SCORE, score))


def _required_choice(answer: dict[str, Any], field: str, question_id: str) -> str:
    choice = answer.get(field)
    if not isinstance(choice, str) or not choice:
        raise QuestionnaireScoringError(f"answer for {question_id} missing {field}")
    return choice


def _optional_choice_list(answer: dict[str, Any], field: str) -> list[str]:
    raw_choices = answer.get(field, [])
    if raw_choices is None:
        return []
    if not isinstance(raw_choices, list):
        raise QuestionnaireScoringError(f"{field} must be a list")
    choices: list[str] = []
    for choice in raw_choices:
        if not isinstance(choice, str) or not choice:
            raise QuestionnaireScoringError(f"{field} contains invalid choice")
        if choice not in choices:
            choices.append(choice)
    return choices


def _required_number(answer: dict[str, Any], field: str, question_id: str) -> float:
    value = answer.get(field)
    if not isinstance(value, int | float):
        raise QuestionnaireScoringError(f"answer for {question_id} missing numeric {field}")
    return float(value)

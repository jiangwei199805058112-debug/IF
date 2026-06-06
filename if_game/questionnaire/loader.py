from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DEFAULT_QUESTIONNAIRE_PATH = DATA_DIR / "questionnaire_mvp.json"

VALID_SELECTION_MODES = {
    "forced_single",
    "multi_select",
    "primary_with_secondary",
    "multi_with_primary",
    "ranked_multi",
    "weighted_multi",
    "slider",
    "axis_2d",
    "scenario_choice",
    "npc_perspective",
    "reverse_check",
    "open_text",
}

REQUIRED_QUESTION_FIELDS = {
    "id",
    "module",
    "title",
    "prompt",
    "selection_mode",
    "required",
    "dimensions",
    "scoring",
}


class QuestionnaireConfigError(ValueError):
    """Raised when a questionnaire config is structurally invalid."""


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise QuestionnaireConfigError("questionnaire config must be a JSON object")
    return data


def _require_question_payload(question: Any, index: int) -> dict[str, Any]:
    if not isinstance(question, dict):
        raise QuestionnaireConfigError(f"question at index {index} must be an object")

    missing = sorted(field for field in REQUIRED_QUESTION_FIELDS if field not in question)
    if missing:
        qid = question.get("id", f"index {index}")
        raise QuestionnaireConfigError(f"question {qid} missing fields: {', '.join(missing)}")

    return question


def _validate_question(question: dict[str, Any], seen_ids: set[str], index: int) -> None:
    question_id = question["id"]
    if not isinstance(question_id, str) or not question_id:
        raise QuestionnaireConfigError(f"question at index {index} has invalid id")
    if question_id in seen_ids:
        raise QuestionnaireConfigError(f"duplicate question id: {question_id}")
    seen_ids.add(question_id)

    selection_mode = question["selection_mode"]
    if selection_mode not in VALID_SELECTION_MODES:
        raise QuestionnaireConfigError(
            f"question {question_id} has invalid selection_mode: {selection_mode}"
        )

    dimensions = question["dimensions"]
    if not isinstance(dimensions, list) or not dimensions:
        raise QuestionnaireConfigError(f"question {question_id} must define dimensions")
    for dimension in dimensions:
        if not isinstance(dimension, str) or not dimension:
            raise QuestionnaireConfigError(f"question {question_id} has invalid dimension entry")

    scoring = question["scoring"]
    if not isinstance(scoring, dict):
        raise QuestionnaireConfigError(f"question {question_id} scoring must be an object")
    if "dimension_effects" not in scoring:
        raise QuestionnaireConfigError(f"question {question_id} missing scoring.dimension_effects")


def validate_questionnaire_config(config: dict[str, Any]) -> None:
    questions = config.get("questions")
    if not isinstance(questions, list):
        raise QuestionnaireConfigError("questionnaire config must contain questions list")

    seen_ids: set[str] = set()
    for index, raw_question in enumerate(questions):
        question = _require_question_payload(raw_question, index)
        _validate_question(question, seen_ids, index)


def load_questionnaire_config(path: str | Path = DEFAULT_QUESTIONNAIRE_PATH) -> dict[str, Any]:
    resolved_path = Path(path)
    config = _load_json(resolved_path)
    validate_questionnaire_config(config)
    return config


def load_mvp_questionnaire() -> dict[str, Any]:
    return load_questionnaire_config(DEFAULT_QUESTIONNAIRE_PATH)

from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
import sys
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.engine import run_14_day_simulation
from if_game.event_loader import load_day_flow, load_sample_characters, load_seed_events
from if_game.main import _run_interactive_menu
from if_game.questionnaire.loader import load_mvp_questionnaire
from if_game.questionnaire.runner import run_questionnaire


def _default_questionnaire_answer(question: dict) -> str:
    selection_mode = question["selection_mode"]
    if selection_mode in {"forced_single", "primary_with_secondary", "multi_with_primary"}:
        return "1"
    if selection_mode == "slider":
        return "50"
    if selection_mode == "axis_2d":
        return "50,50"
    raise AssertionError(f"unsupported questionnaire smoke mode: {selection_mode}")


def main() -> None:
    characters = load_sample_characters()
    events = load_seed_events()
    day_flow = load_day_flow()

    assert "pairs" in characters and len(characters["pairs"]) >= 5
    assert "events" in events and len(events["events"]) >= 3
    assert len(day_flow) == 14

    scripted_choices = {
        "MSG_001": {"branch_id": "MSG_001_B", "choice_tag": "ask_softly"},
        "SOC_001": {"branch_id": "SOC_001_B", "choice_tag": "set_boundary"},
        "CONFLICT_001": {"branch_id": "CONFLICT_001_C", "choice_tag": "private_talk"},
    }
    result = run_14_day_simulation("ambiguous", "A", scripted_choices=scripted_choices)

    assert result["final_stage"]
    assert result["transcript"]
    assert "memory_summaries" in result
    assert "feedback_level" in result
    assert "review" in result
    assert isinstance(result["memory_summaries"], list)
    assert result["feedback_level"]
    assert result["review"]["main_stage"] == result["final_stage"]
    triggered = set(result["triggered_events"])
    assert {"MSG_001", "SOC_001", "CONFLICT_001"}.issubset(triggered)
    assert result["memory_count"] >= 1

    transcript_text = "\n".join(result["transcript"])
    forbidden_tokens = ["真实信任", "真实好感", "trust="]
    for token in forbidden_tokens:
        assert token not in transcript_text

    questionnaire = load_mvp_questionnaire()
    menu_inputs = iter(
        ["3"]
        + [_default_questionnaire_answer(question) for question in questionnaire["questions"]]
    )
    output = StringIO()
    run_questionnaire_with_inputs = lambda: run_questionnaire(
        input_func=lambda _prompt="": next(menu_inputs)
    )
    with patch("builtins.input", lambda _prompt="": next(menu_inputs)):
        with patch("if_game.main.run_questionnaire", run_questionnaire_with_inputs):
            with redirect_stdout(output):
                _run_interactive_menu()

    menu_output = output.getvalue()
    assert "IF 问卷 MVP 控制台" in menu_output
    assert "IF 问卷 MVP 报告" in menu_output

    print("smoke test passed")


if __name__ == "__main__":
    main()

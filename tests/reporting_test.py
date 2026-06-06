from __future__ import annotations

import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.engine import run_playtest_scenario
from if_game.event_loader import load_playtest_scenarios
from if_game.reporting import format_summary_report, format_transcript, write_report


FORBIDDEN_TOKENS = ["真实信任", "真实好感", "trust=", "security=", "conflict="]


def _load_scenario(scenario_id: str) -> dict:
    for scenario in load_playtest_scenarios().get("scenarios", []):
        if scenario["id"] == scenario_id:
            return scenario
    raise AssertionError(f"missing scenario {scenario_id}")


def _assert_no_internal_values(text: str) -> None:
    for token in FORBIDDEN_TOKENS:
        assert token not in text


def main() -> None:
    result = run_playtest_scenario(_load_scenario("scenario_repair"))

    transcript_report = format_transcript(result)
    summary_report = format_summary_report(result)
    assert "scenario_repair" in transcript_report
    assert "final_stage" in summary_report
    _assert_no_internal_values(transcript_report)
    _assert_no_internal_values(summary_report)

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = Path(temp_dir) / "test_report.txt"
        written_path = write_report(result, output_path)
        assert written_path.exists()
        saved_text = written_path.read_text(encoding="utf-8")
        assert "IF 试玩记录" in saved_text
        _assert_no_internal_values(saved_text)

    print("reporting test passed")


if __name__ == "__main__":
    main()

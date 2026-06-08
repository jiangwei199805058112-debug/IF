from __future__ import annotations

import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.engine import run_14_day_simulation, run_playtest_scenario
from if_game.event_loader import load_playtest_scenarios
from if_game.reporting import format_summary_report, format_transcript, write_report


REQUIRED_REPORT_TOKENS = ["关系复盘报告", "结局", "副标签", "关键转折点", "主要原因", "后续隐患"]
FORBIDDEN_TOKENS = [
    "scenario_id:",
    "feedback_level:",
    "active_hooks:",
    "triggered_events:",
    "truth_type",
    "deception_level",
    "trust=",
    "security=",
    "conflict=",
    "真实信任",
    "真实好感",
]


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
    for token in REQUIRED_REPORT_TOKENS:
        assert token in transcript_report
    assert "关系状态变化" in transcript_report
    assert "scenario_repair" not in transcript_report
    assert "final_stage:" not in summary_report
    assert "有效修复路径" in summary_report
    _assert_no_internal_values(transcript_report)
    _assert_no_internal_values(summary_report)

    initial_result = run_14_day_simulation(
        "ambiguous",
        "A",
        initial_modifiers={
            "reassurance_need_delta": 3,
            "privacy_boundary_sensitivity_delta": 3,
            "suspicion_sensitivity_delta": 3,
        },
    )
    initial_report = format_transcript(initial_result)
    assert "本局开局倾向" in initial_report
    assert "这些只是开局倾向" in initial_report
    for phrase in ["你有病", "你一定会", "你就是", "人格障碍", "病态"]:
        assert phrase not in initial_report
    _assert_no_internal_values(initial_report)

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = Path(temp_dir) / "test_report.txt"
        written_path = write_report(result, output_path)
        assert written_path.exists()
        saved_text = written_path.read_text(encoding="utf-8")
        assert "IF 关系复盘报告" in saved_text
        _assert_no_internal_values(saved_text)

    print("reporting test passed")


if __name__ == "__main__":
    main()

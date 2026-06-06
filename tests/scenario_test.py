from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.engine import run_14_day_simulation
from if_game.event_loader import load_playtest_scenarios


def _assert_scenario_expectations(scenario: dict[str, Any], result: dict[str, Any]) -> None:
    expected = scenario["expected"]

    allowed_stages = set(expected["allowed_final_stages"])
    assert result["final_stage"] in allowed_stages, (
        f"{scenario['id']} final_stage={result['final_stage']} allowed={sorted(allowed_stages)}"
    )

    assert result["memory_count"] >= int(expected["min_memory_count"]), (
        f"{scenario['id']} memory_count={result['memory_count']}"
    )

    triggered_events = set(result["triggered_events"])
    for event_id in expected["required_events"]:
        assert event_id in triggered_events, f"{scenario['id']} missing event {event_id}"

    transcript_text = "\n".join(result["transcript"])
    for token in expected["forbidden_transcript_tokens"]:
        assert token not in transcript_text, f"{scenario['id']} leaked token {token}"


def main() -> None:
    scenario_data = load_playtest_scenarios()
    scenarios = scenario_data.get("scenarios", [])
    assert len(scenarios) >= 5

    for scenario in scenarios:
        result = run_14_day_simulation(
            scenario["entry_mode"],
            scenario["profile_pair_id"],
            scripted_choices=scenario["scripted_choices"],
        )
        _assert_scenario_expectations(scenario, result)
        print(
            f"{scenario['id']}: {result['final_stage']} | "
            f"memories={result['memory_count']} | feedback={result['feedback_level']}"
        )

    print("scenario test passed")


if __name__ == "__main__":
    main()

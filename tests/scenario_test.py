from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.engine import run_all_playtest_scenarios
from if_game.event_loader import load_playtest_scenarios


def _assert_scenario_expectations(scenario: dict[str, Any], result: dict[str, Any]) -> None:
    expected = scenario["expected"]

    allowed_stages = set(expected["allowed_final_stages"])
    assert result["final_stage"] in allowed_stages, (
        f"{scenario['id']} final_stage={result['final_stage']} allowed={sorted(allowed_stages)}"
    )
    review = result["review"]
    assert review["main_stage"] == result["final_stage"]

    sub_tags = set(review["sub_tags"])
    for tag in expected.get("expected_sub_tags", []):
        assert tag in sub_tags, f"{scenario['id']} missing sub tag {tag}"

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
    scenario_by_id = {scenario["id"]: scenario for scenario in scenarios}

    results = run_all_playtest_scenarios()
    assert len(results) == len(scenarios)

    for result in results:
        scenario = scenario_by_id[result["scenario_id"]]
        assert result["scenario_title"]
        assert "scenario_description" in result
        assert isinstance(result["memory_summaries"], list)
        assert result["feedback_level"]
        assert isinstance(result["active_hooks"], list)
        assert isinstance(result["relationship_aggregator_log"], list)
        assert isinstance(result["relationship_delta_summaries"], list)
        assert len(result["relationship_aggregator_log"]) >= len(result["triggered_events"])
        assert result["relationship_delta_summaries"]
        assert isinstance(result["review"], dict)
        assert result["review"]["summary"]
        assert result["review"]["main_reasons"]
        assert result["review"]["turning_points"]
        assert result["review"]["risks"]
        assert result["review"]["repair_chances"]
        _assert_scenario_expectations(scenario, result)
        print(
            f"{scenario['id']}: {result['final_stage']} | "
            f"tags={','.join(result['review']['sub_tags'])}"
        )

    print("scenario test passed")


if __name__ == "__main__":
    main()

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.engine import run_14_day_simulation
from if_game.event_loader import load_day_flow, load_sample_characters, load_seed_events


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
    triggered = set(result["triggered_events"])
    assert {"MSG_001", "SOC_001", "CONFLICT_001"}.issubset(triggered)
    assert result["memory_count"] >= 1

    transcript_text = "\n".join(result["transcript"])
    forbidden_tokens = ["真实信任", "真实好感", "trust="]
    for token in forbidden_tokens:
        assert token not in transcript_text

    print("smoke test passed")


if __name__ == "__main__":
    main()

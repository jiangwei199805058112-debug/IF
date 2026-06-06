from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).parent / "data"


def _load_json(filename: str) -> Any:
    path = DATA_DIR / filename
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_sample_characters() -> dict[str, Any]:
    return _load_json("sample_characters.json")


def load_seed_events() -> dict[str, Any]:
    return _load_json("seed_events.json")


def load_day_flow() -> list[dict[str, Any]]:
    return _load_json("day_flow.json")


def load_playtest_scenarios() -> dict[str, Any]:
    return _load_json("playtest_scenarios.json")

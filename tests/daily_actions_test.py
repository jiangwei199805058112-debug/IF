from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.daily_actions import (
    format_daily_action_result,
    format_daily_status_header,
    get_daily_actions,
    resolve_daily_action,
)
from if_game.engine import run_14_day_simulation


def _state() -> SimpleNamespace:
    return SimpleNamespace(active_hooks=[], daily_action_history=[])


def _append_history(state: SimpleNamespace, day: int, action_key: str, result: dict) -> None:
    state.daily_action_history.append(
        {
            "day": day,
            "action_key": action_key,
            "context_tags": list(result.get("context_tags", [])),
            "atmosphere_tag": result.get("atmosphere_tag", ""),
        }
    )


def _atmosphere_line(lines: list[str]) -> str:
    for line in lines:
        if line.startswith("氛围："):
            return line
    raise AssertionError("missing atmosphere line")


def main() -> None:
    header = format_daily_status_header(1, "ambiguous", "stable")
    header_text = "\n".join(header)
    assert "氛围：" in header_text
    assert "对方主动性：" in header_text
    assert "你的不安：" in header_text
    assert "修复窗口：" in header_text

    chatting_actions = get_daily_actions(1, "chatting", "A", "stable")
    assert len(chatting_actions) >= 5
    assert any(action["action_key"] == "ask_busy" for action in chatting_actions)

    result_a = resolve_daily_action("ask_busy", 2, "chatting", "A", "stable", _state())
    result_b = resolve_daily_action("ask_busy", 2, "chatting", "B", "stable", _state())
    for result in (result_a, result_b):
        assert set(["npc_response", "atmosphere_tag", "relationship_delta", "player_feedback"]).issubset(result)
        assert isinstance(result["relationship_delta"], dict)
        assert all(abs(value) <= 1 for value in result["relationship_delta"].values())
        assert "crisis" not in result["relationship_delta"]
        formatted = "\n".join(format_daily_action_result(result))
        assert "每日行动：" in formatted
        assert "对方回应：" in formatted
        assert "氛围变化：" in formatted
    assert result_a["npc_response"] != result_b["npc_response"]
    assert "周然" in result_a["npc_response"]
    assert "许知遥" in result_b["npc_response"]

    cold_state = _state()
    first_header = format_daily_status_header(1, "chatting", "stable")
    atmosphere = "stable"
    for day in (1, 2, 3):
        result = resolve_daily_action("wait_contact", day, "chatting", "A", atmosphere, cold_state)
        _append_history(cold_state, day, "wait_contact", result)
        atmosphere = result["atmosphere_tag"]
    fourth_header = format_daily_status_header(4, "chatting", atmosphere)
    assert _atmosphere_line(first_header) != _atmosphere_line(fourth_header)
    assert "氛围：降温" in "\n".join(fourth_header)

    repair_result = resolve_daily_action("ask_busy", 5, "chatting", "A", "cooling_down", _state())
    assert "repair_action" in repair_result["context_tags"]
    assert "cold_action" not in repair_result["context_tags"]
    assert repair_result["atmosphere_tag"] == "repair_window_open"

    high_reassurance = resolve_daily_action(
        "wait_contact",
        6,
        "chatting",
        "A",
        "stable",
        _state(),
        initial_modifiers={"reassurance_need_delta": 3},
    )
    low_reassurance = resolve_daily_action(
        "wait_contact",
        6,
        "chatting",
        "A",
        "stable",
        _state(),
        initial_modifiers={"reassurance_need_delta": -3},
    )
    assert high_reassurance["player_feedback"] != low_reassurance["player_feedback"]
    assert "反复确认聊天框" in high_reassurance["player_feedback"]
    assert "注意力放回自己的事" in low_reassurance["player_feedback"]

    scripted_choices = {
        "daily_actions": {1: "observe", 2: "observe", 4: "observe"},
        "MSG_001": {"branch_id": "MSG_001_B", "choice_tag": "ask_softly"},
        "SOC_001": {"branch_id": "SOC_001_B", "choice_tag": "set_boundary"},
        "CONFLICT_001": {"branch_id": "CONFLICT_001_C", "choice_tag": "private_talk"},
    }
    result = run_14_day_simulation("ambiguous", "A", scripted_choices=scripted_choices)
    transcript_text = "\n".join(result["transcript"])
    assert "每日行动：" in transcript_text
    assert "对方回应：" in transcript_text
    assert "氛围：" in transcript_text
    assert "余波日：" in transcript_text
    assert "第 7 天中期反馈：" in transcript_text
    assert "当前氛围趋势：" in transcript_text
    assert "玩家行为模式：" in transcript_text
    assert "第 8 天前的轻微铺垫：" in transcript_text
    assert "事件：对方很久没回消息" in transcript_text
    assert "事件：异性饭局/神秘电话" in transcript_text
    assert "事件：吵架后是否解决" in transcript_text
    assert "第 14 天阶段结算" in transcript_text
    assert transcript_text.count("氛围：") >= 14
    assert transcript_text.count("每日行动：") == 10
    assert transcript_text.count("对方回应：") == 10
    assert len(result["daily_action_history"]) == 10
    assert result["relationship_delta_summaries"]
    assert "trust=" not in transcript_text

    print("daily actions test passed")


if __name__ == "__main__":
    main()

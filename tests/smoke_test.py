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
from if_game.main import _build_parser, _print_startup, _run_interactive_menu
from if_game.questionnaire.loader import load_mvp_questionnaire


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
    startup_output = StringIO()
    with redirect_stdout(startup_output):
        _print_startup()
    startup_text = startup_output.getvalue()
    assert "v0.1.60" in startup_text
    assert "v0.1.6 控制台测试原型" not in startup_text
    assert "v0.1.60" in _build_parser().description

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
    assert isinstance(result["relationship_aggregator_log"], list)
    assert isinstance(result["relationship_delta_summaries"], list)
    assert result["relationship_aggregator_log"]
    assert result["relationship_delta_summaries"]
    assert result["feedback_level"]
    assert result["review"]["main_stage"] == result["final_stage"]
    triggered = set(result["triggered_events"])
    assert {"MSG_001", "SOC_001", "CONFLICT_001"}.issubset(triggered)
    assert result["memory_count"] >= 1

    transcript_text = "\n".join(result["transcript"])
    forbidden_tokens = ["真实信任", "真实好感", "trust="]
    for token in forbidden_tokens:
        assert token not in transcript_text
    assert "关系状态变化" in transcript_text
    assert "本轮目标：" in transcript_text
    assert "每日行动：" in transcript_text
    assert "对方回应：" in transcript_text
    assert "氛围：" in transcript_text
    assert "余波日：" in transcript_text
    assert "第 7 天中期反馈：" in transcript_text
    assert "当前氛围趋势：" in transcript_text
    assert "原因说明：" in transcript_text
    assert "冲突后约定私下复盘" in transcript_text
    assert "修复窗口" in transcript_text
    assert "沉默没有回到问题本身，容易变成冷处理模式。" not in transcript_text
    assert transcript_text.count("事件：对方很久没回消息") == 1
    assert transcript_text.count("事件：异性饭局/神秘电话") == 1
    assert transcript_text.count("事件：吵架后是否解决") == 1
    assert "本局开局倾向" not in transcript_text

    initial_modifiers = {
        "reassurance_need_delta": 3,
        "privacy_boundary_sensitivity_delta": 3,
        "suspicion_sensitivity_delta": 3,
    }
    result_with_initial_modifiers = run_14_day_simulation(
        "ambiguous",
        "A",
        scripted_choices=scripted_choices,
        initial_modifiers=initial_modifiers,
    )
    modifier_transcript = "\n".join(result_with_initial_modifiers["transcript"])
    assert "本局开局倾向" in modifier_transcript
    assert "这些只是开局倾向" in modifier_transcript
    assert "氛围：" in modifier_transcript
    for phrase in ["你有病", "你一定会", "你就是", "人格障碍", "病态"]:
        assert phrase not in modifier_transcript
    assert result_with_initial_modifiers["final_stage"] == result["final_stage"]
    assert result_with_initial_modifiers["triggered_events"] == result["triggered_events"]
    assert result_with_initial_modifiers["memory_summaries"] == result["memory_summaries"]

    immediate_inputs = iter([""] * 40)
    immediate_prompts: list[str] = []

    def immediate_input(prompt: str = "") -> str:
        immediate_prompts.append(prompt)
        return next(immediate_inputs)

    immediate_output = StringIO()
    with redirect_stdout(immediate_output):
        interactive_result = run_14_day_simulation(
            "ambiguous",
            "A",
            interactive=True,
            input_func=immediate_input,
        )
    immediate_text = immediate_output.getvalue()
    assert "每日行动：" in immediate_text
    assert "对方回应：" in immediate_text
    assert "氛围变化：" in immediate_text
    assert "你的感受：" in immediate_text
    assert "你的选择：" in immediate_text
    assert "记忆账本：" in immediate_text
    assert "关系状态变化：" in immediate_text
    assert "感知反馈：" in immediate_text
    assert "按回车继续。" in immediate_text
    assert "按回车进入下一天。" not in immediate_text
    assert "第 14 天阶段结算" in immediate_text
    assert immediate_text.index("每日行动：") < immediate_text.index("第 2 天：")
    assert "按回车继续。" not in "\n".join(interactive_result["transcript"])
    assert not any(prompt.startswith("事件：") for prompt in immediate_prompts)

    questionnaire = load_mvp_questionnaire()
    captured_run_kwargs: dict = {}

    def fake_collect_questionnaire_result(input_func=input):
        return {
            "score_result": {
                "dimension_scores": {
                    "emotion_reassurance_need": 90,
                    "digital_phone_privacy_need": 90,
                },
                "evidence_count": {
                    "emotion_reassurance_need": 2,
                    "digital_phone_privacy_need": 2,
                },
                "answered_questions": 2,
                "total_questions": len(questionnaire["questions"]),
                "completion_rate": 1.0,
            }
        }

    def fake_run_14_day_simulation(*_args, **kwargs):
        captured_run_kwargs.update(kwargs)
        result = {"transcript": ["本局开局倾向：", "- 遇到不确定回应时，开局更需要明确安抚和说明。"]}
        for line in result["transcript"]:
            print(line)
        return result

    menu_yes_inputs = iter(["1", "1", "2", "1"])
    output = StringIO()
    with patch("builtins.input", lambda _prompt="": next(menu_yes_inputs)):
        with patch("if_game.main.collect_questionnaire_result", fake_collect_questionnaire_result):
            with patch("if_game.main.run_14_day_simulation", fake_run_14_day_simulation):
                with redirect_stdout(output):
                    _run_interactive_menu()

    menu_yes_output = output.getvalue()
    assert "是否先回答问卷，生成本局初始倾向？" in menu_yes_output
    assert "快速预设组合会同时决定玩家倾向、NPC 倾向和主要矛盾主题。" in menu_yes_output
    assert "选择快速预设组合：" in menu_yes_output
    assert "选择样例角色组合：" not in menu_yes_output
    assert "本局开局倾向" in menu_yes_output
    assert captured_run_kwargs["initial_modifiers"]["reassurance_need_delta"] > 0
    assert captured_run_kwargs["initial_modifiers"]["privacy_boundary_sensitivity_delta"] > 0
    assert captured_run_kwargs["initial_modifiers"]["initial_modifier_summary"]

    interactive_inputs = iter(["1", "", "2", "1"] + [""] * 40)
    output = StringIO()
    with patch("builtins.input", lambda _prompt="": next(interactive_inputs)):
        with redirect_stdout(output):
            _run_interactive_menu()

    interactive_output = output.getvalue()
    assert "是否先回答问卷，生成本局初始倾向？" in interactive_output
    assert "IF 问卷 MVP 控制台" not in interactive_output
    assert "本局开局倾向" not in interactive_output
    assert "每日行动：" in interactive_output
    assert "对方回应：" in interactive_output
    assert "按回车继续。" in interactive_output
    assert "按回车进入下一天。" not in interactive_output

    menu_inputs = iter(
        ["3"]
        + [_default_questionnaire_answer(question) for question in questionnaire["questions"]]
    )
    output = StringIO()
    with patch("builtins.input", lambda _prompt="": next(menu_inputs)):
        with redirect_stdout(output):
            _run_interactive_menu()

    menu_output = output.getvalue()
    assert "IF 问卷 MVP 控制台" in menu_output
    assert "IF 问卷 MVP 报告" in menu_output

    print("smoke test passed")


if __name__ == "__main__":
    main()

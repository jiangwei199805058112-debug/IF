from __future__ import annotations

import argparse
from typing import Any

from .engine import run_14_day_simulation, run_all_playtest_scenarios, run_playtest_scenario
from .event_loader import load_playtest_scenarios, load_sample_characters
from .questionnaire.initial_modifiers import (
    build_initial_relationship_modifiers,
    format_initial_modifier_summary,
)
from .questionnaire.runner import collect_questionnaire_result, run_questionnaire
from .reporting import format_transcript, write_report, write_scenario_summary


APP_VERSION = "v0.1.61"

MODE_OPTIONS = [
    ("interactive", "互动运行 14 天"),
    ("scenarios", "运行内置场景测试摘要"),
    ("questionnaire", "回答问卷 MVP 快速版"),
]

ENTRY_OPTIONS = [
    ("chatting", "正在聊天"),
    ("ambiguous", "暧昧中"),
    ("new_relationship", "刚恋爱"),
]

QUESTIONNAIRE_START_OPTIONS = [
    ("yes", "是"),
    ("no", "否"),
]

RELATIONSHIP_SETUP_OPTIONS = [
    ("quick_preset", "快速预设组合"),
    ("questionnaire", "根据问卷生成"),
    ("manual", "手动自定义"),
]

PLAYER_TENDENCY_OPTIONS = [
    ("high_reassurance", "安全感需求较高"),
    ("social_open", "社交比较开放"),
    ("material_expectation", "现实 / 物质期待较高"),
    ("high_attraction_low_stability", "生理吸引强但稳定性较低"),
    ("mature_communication", "成熟沟通型"),
]

NPC_TENDENCY_OPTIONS = [
    ("busy_avoidant", "忙碌回避型"),
    ("jealous_double_standard", "高吃醋 / 容易双标"),
    ("practical_low_income", "低收入务实型"),
    ("low_emotional_stability", "低心理稳定"),
    ("emotional_testing", "情绪试探型"),
]

CONFLICT_THEME_OPTIONS = [
    ("message_security", "消息回复和安全感"),
    ("social_boundary", "异性边界和社交自由"),
    ("money_pressure", "消费观和现实压力"),
    ("attraction_stability", "生理吸引与心理稳定"),
    ("repair_testing", "沟通修复与情绪试探"),
]

THEME_TO_PROFILE_PAIR = {
    "message_security": "A",
    "social_boundary": "B",
    "money_pressure": "C",
    "attraction_stability": "D",
    "repair_testing": "E",
}

NPC_TENDENCY_TO_PROFILE_PAIR = {
    "busy_avoidant": "A",
    "jealous_double_standard": "B",
    "practical_low_income": "C",
    "low_emotional_stability": "D",
    "emotional_testing": "E",
}


def _choose(prompt: str, options: list[tuple[str, str]], default_index: int = 0) -> str:
    print(prompt)
    for index, (_, label) in enumerate(options, start=1):
        print(f"{index}. {label}")
    raw = input(f"直接回车使用第 {default_index + 1} 项：").strip()
    if not raw:
        return options[default_index][0]
    try:
        selected = int(raw) - 1
    except ValueError:
        selected = default_index
    if 0 <= selected < len(options):
        return options[selected][0]
    return options[default_index][0]


def _join_cli_list(values: list[str]) -> str:
    return "、".join(values) if values else "无"


def _label_for(options: list[tuple[str, str]], key: str) -> str:
    return next((label for option_key, label in options if option_key == key), key)


def _nearest_profile_pair_id(npc_tendency: str, conflict_theme: str) -> str:
    return THEME_TO_PROFILE_PAIR.get(
        conflict_theme,
        NPC_TENDENCY_TO_PROFILE_PAIR.get(npc_tendency, "A"),
    )


def _quick_preset_config(profile_pair_id: str, pair_title: str) -> dict[str, Any]:
    return {
        "setup_method": "快速预设组合",
        "quick_preset_title": pair_title,
        "player_tendency": "由快速预设决定",
        "npc_tendency": "由快速预设决定",
        "conflict_theme": "由快速预设决定",
    }


def _choose_quick_preset(profiles: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    pair_options = [(pair_id, pair["title"]) for pair_id, pair in profiles["pairs"].items()]
    print("快速预设组合会同时决定玩家倾向、NPC 倾向和主要矛盾主题，仅用于快速试玩。")
    profile_pair_id = _choose("选择快速预设组合：", pair_options, default_index=0)
    pair_title = str(profiles["pairs"][profile_pair_id]["title"])
    return profile_pair_id, _quick_preset_config(profile_pair_id, pair_title)


def _derive_player_tendency_from_questionnaire(initial_modifiers: dict[str, Any]) -> str:
    labels: list[str] = []
    if int(initial_modifiers.get("reassurance_need_delta", 0) or 0) > 0:
        labels.append("稳定回应需求较高")
    if int(initial_modifiers.get("privacy_boundary_sensitivity_delta", 0) or 0) > 0:
        labels.append("透明期待较高")
    if int(initial_modifiers.get("suspicion_sensitivity_delta", 0) or 0) > 0:
        labels.append("信任线索敏感")
    if not labels:
        labels.append("稳定观察型")
    return " / ".join(labels[:2])


def _questionnaire_defaults(initial_modifiers: dict[str, Any]) -> tuple[int, int]:
    if int(initial_modifiers.get("privacy_boundary_sensitivity_delta", 0) or 0) > 0:
        return 1, 1
    if int(initial_modifiers.get("reassurance_need_delta", 0) or 0) > 0:
        return 0, 0
    return 4, 4


def _choose_questionnaire_config(
    initial_modifiers: dict[str, Any] | None,
    profiles: dict[str, Any],
) -> tuple[str, dict[str, Any]]:
    if not initial_modifiers:
        print("当前没有问卷结果，无法根据问卷生成关系配置。")
        print("请先回答问卷，或使用快速预设组合。")
        return _choose_quick_preset(profiles)

    player_tendency = _derive_player_tendency_from_questionnaire(initial_modifiers)
    npc_default, theme_default = _questionnaire_defaults(initial_modifiers)
    print(f"根据问卷结果，本局玩家倾向更接近：{player_tendency}。")
    npc_tendency = _choose("选择 NPC 倾向：", NPC_TENDENCY_OPTIONS, default_index=npc_default)
    conflict_theme = _choose("选择主要矛盾主题：", CONFLICT_THEME_OPTIONS, default_index=theme_default)
    profile_pair_id = _nearest_profile_pair_id(npc_tendency, conflict_theme)
    return profile_pair_id, {
        "setup_method": "根据问卷生成",
        "player_tendency": player_tendency,
        "npc_tendency": _label_for(NPC_TENDENCY_OPTIONS, npc_tendency),
        "conflict_theme": _label_for(CONFLICT_THEME_OPTIONS, conflict_theme),
    }


def _choose_manual_config() -> tuple[str, dict[str, Any]]:
    player_tendency = _choose("选择玩家倾向：", PLAYER_TENDENCY_OPTIONS, default_index=0)
    npc_tendency = _choose("选择 NPC 倾向：", NPC_TENDENCY_OPTIONS, default_index=0)
    conflict_theme = _choose("选择主要矛盾主题：", CONFLICT_THEME_OPTIONS, default_index=0)
    profile_pair_id = _nearest_profile_pair_id(npc_tendency, conflict_theme)
    return profile_pair_id, {
        "setup_method": "手动自定义",
        "player_tendency": _label_for(PLAYER_TENDENCY_OPTIONS, player_tendency),
        "npc_tendency": _label_for(NPC_TENDENCY_OPTIONS, npc_tendency),
        "conflict_theme": _label_for(CONFLICT_THEME_OPTIONS, conflict_theme),
    }


def _choose_relationship_setup(
    profiles: dict[str, Any],
    initial_modifiers: dict[str, Any] | None,
) -> tuple[str, dict[str, Any]]:
    setup_method = _choose("选择本局关系设置方式：", RELATIONSHIP_SETUP_OPTIONS, default_index=0)
    if setup_method == "questionnaire":
        return _choose_questionnaire_config(initial_modifiers, profiles)
    if setup_method == "manual":
        return _choose_manual_config()
    return _choose_quick_preset(profiles)


def _load_scenarios() -> list[dict[str, Any]]:
    return load_playtest_scenarios().get("scenarios", [])


def _find_scenario(scenario_id: str) -> dict[str, Any]:
    for scenario in _load_scenarios():
        if scenario.get("id") == scenario_id:
            return scenario
    raise KeyError(f"Unknown scenario: {scenario_id}")


def _print_startup() -> None:
    print(f"IF {APP_VERSION} 控制台测试原型")
    print("真实内部数值不会显示。")
    print()


def _run_interactive_menu() -> None:
    mode = _choose("选择运行模式：", MODE_OPTIONS, default_index=0)
    if mode == "scenarios":
        print()
        print("----- 内置场景摘要 -----")
        for result in run_all_playtest_scenarios():
            print(
                f"{result['scenario_id']}：{result['final_stage']}；"
                f"记忆 {result['memory_count']} 条；反馈 {result['feedback_level']}"
            )
        print("----- 结束 -----")
        return

    if mode == "questionnaire":
        print()
        run_questionnaire(input_func=input)
        return

    initial_modifiers: dict[str, Any] | None = None
    questionnaire_start = _choose(
        "是否先回答问卷，生成本局初始倾向？",
        QUESTIONNAIRE_START_OPTIONS,
        default_index=1,
    )
    if questionnaire_start == "yes":
        print()
        questionnaire_result = collect_questionnaire_result(input_func=input)
        initial_modifiers = build_initial_relationship_modifiers(questionnaire_result["score_result"])
        initial_modifiers["initial_modifier_summary"] = format_initial_modifier_summary(initial_modifiers)

    entry_mode = _choose("选择开局模式：", ENTRY_OPTIONS, default_index=1)

    profiles = load_sample_characters()
    profile_pair_id, relationship_config = _choose_relationship_setup(profiles, initial_modifiers)

    print()
    print("开始 14 天模拟。普通日可选择每日行动，关键事件日会提供处理方式。")
    run_14_day_simulation(
        entry_mode,
        profile_pair_id,
        interactive=True,
        input_func=input,
        initial_modifiers=initial_modifiers,
        relationship_config=relationship_config,
    )

    print()
    print("----- 结束 -----")
    print("提醒：这是规则测试原型，不做 UI、存档、AI、完整经济系统、完整亲密系统或完整一年模拟。")


def _list_scenarios() -> None:
    for scenario in _load_scenarios():
        print(f"{scenario['id']}：{scenario['title']}")
        print(f"  {scenario.get('description', '')}")


def _run_single_scenario(scenario_id: str, export_path: str | None = None) -> None:
    result = run_playtest_scenario(_find_scenario(scenario_id))
    print(format_transcript(result))
    if export_path:
        path = write_report(result, export_path)
        print(f"已导出 UTF-8 报告：{path}")


def _run_all_scenarios(export_path: str | None = None) -> None:
    results = run_all_playtest_scenarios()
    print("----- 多场景关系复盘摘要 -----")
    for result in results:
        review = result["review"]
        print(
            f"{result['scenario_title']}：{review['main_stage']}；"
            f"副标签 {_join_cli_list(review['sub_tags'])}"
        )
    if export_path:
        path = write_scenario_summary(results, export_path)
        print(f"已导出 UTF-8 汇总：{path}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=f"IF {APP_VERSION} 控制台测试原型")
    parser.add_argument("--list-scenarios", action="store_true", help="列出所有内置试玩场景")
    parser.add_argument("--scenario", help="运行指定脚本场景 ID")
    parser.add_argument("--run-all-scenarios", action="store_true", help="运行全部内置脚本场景")
    parser.add_argument("--export", help="把运行结果导出为 UTF-8 文本报告")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    has_command = bool(args.list_scenarios or args.scenario or args.run_all_scenarios)
    if args.export and not (args.scenario or args.run_all_scenarios):
        parser.error("--export 需要配合 --scenario 或 --run-all-scenarios 使用")
    if args.scenario and args.run_all_scenarios:
        parser.error("--scenario 与 --run-all-scenarios 不能同时使用")

    _print_startup()
    if not has_command:
        _run_interactive_menu()
        return
    if args.list_scenarios:
        _list_scenarios()
    if args.scenario:
        _run_single_scenario(args.scenario, args.export)
    if args.run_all_scenarios:
        _run_all_scenarios(args.export)


if __name__ == "__main__":
    main()

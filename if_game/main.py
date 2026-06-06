from __future__ import annotations

import argparse
from typing import Any

from .engine import run_14_day_simulation, run_all_playtest_scenarios, run_playtest_scenario
from .event_loader import load_playtest_scenarios, load_sample_characters
from .questionnaire.runner import run_questionnaire
from .reporting import format_transcript, write_report, write_scenario_summary


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


def _load_scenarios() -> list[dict[str, Any]]:
    return load_playtest_scenarios().get("scenarios", [])


def _find_scenario(scenario_id: str) -> dict[str, Any]:
    for scenario in _load_scenarios():
        if scenario.get("id") == scenario_id:
            return scenario
    raise KeyError(f"Unknown scenario: {scenario_id}")


def _print_startup() -> None:
    print("IF v0.1.6 控制台测试原型")
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
        run_questionnaire()
        return

    entry_mode = _choose("选择开局模式：", ENTRY_OPTIONS, default_index=1)

    profiles = load_sample_characters()
    pair_options = [(pair_id, pair["title"]) for pair_id, pair in profiles["pairs"].items()]
    profile_pair_id = _choose("选择样例角色组合：", pair_options, default_index=0)

    print()
    print("开始 14 天模拟。事件日会提供测试分支和处理方式。")
    result = run_14_day_simulation(entry_mode, profile_pair_id, interactive=True)

    print()
    print("----- 模拟记录 -----")
    for line in result["transcript"]:
        print(line)
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
    parser = argparse.ArgumentParser(description="IF v0.1.6 控制台测试原型")
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

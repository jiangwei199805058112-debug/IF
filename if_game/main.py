from __future__ import annotations

from .engine import run_14_day_simulation, run_all_playtest_scenarios
from .event_loader import load_sample_characters


MODE_OPTIONS = [
    ("interactive", "互动运行 14 天"),
    ("scenarios", "运行内置场景测试摘要"),
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


def main() -> None:
    print("IF v0.1.5 控制台测试原型")
    print("这是 14 天关系规则测试原型，不是完整游戏，真实数值不会显示。")
    print()

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


if __name__ == "__main__":
    main()

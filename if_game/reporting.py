from __future__ import annotations

from pathlib import Path
from typing import Any


def _join_list(values: list[Any] | tuple[Any, ...] | None) -> str:
    if not values:
        return "无"
    return "、".join(str(value) for value in values)


def format_transcript(result: dict[str, Any]) -> str:
    title = result.get("scenario_title") or result.get("pair_title") or "未指定场景"
    lines = [
        "# IF 试玩记录",
        "",
        f"场景/组合：{title}",
    ]
    if result.get("scenario_id"):
        lines.append(f"场景 ID：{result['scenario_id']}")
    if result.get("scenario_description"):
        lines.append(f"说明：{result['scenario_description']}")
    lines.extend(
        [
            f"最终阶段：{result.get('final_stage', '')}",
            f"反馈等级：{result.get('feedback_level', '')}",
            f"记忆数量：{result.get('memory_count', 0)}",
            f"触发事件：{_join_list(result.get('triggered_events'))}",
            "",
            "## 14 天记录",
            "",
        ]
    )
    lines.extend(str(line) for line in result.get("transcript", []))
    return "\n".join(lines) + "\n"


def format_summary_report(result: dict[str, Any]) -> str:
    lines = ["# IF 试玩摘要", ""]
    if result.get("scenario_id"):
        lines.append(f"scenario_id: {result['scenario_id']}")
    if result.get("scenario_title"):
        lines.append(f"scenario_title: {result['scenario_title']}")
    lines.extend(
        [
            f"final_stage: {result.get('final_stage', '')}",
            f"feedback_level: {result.get('feedback_level', '')}",
            f"memory_count: {result.get('memory_count', 0)}",
            f"memory_summaries: {_join_list(result.get('memory_summaries'))}",
            f"triggered_events: {_join_list(result.get('triggered_events'))}",
            f"active_hooks: {_join_list(result.get('active_hooks'))}",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(result: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(format_transcript(result), encoding="utf-8")
    return path


def write_scenario_summary(results: list[dict[str, Any]], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    sections = ["# IF 多场景试玩汇总", ""]
    for result in results:
        sections.append(format_summary_report(result).strip())
        sections.append("")
    path.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    return path

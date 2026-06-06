from __future__ import annotations

from pathlib import Path
from typing import Any


EVENT_LABELS = {
    "MSG_001": "消息延迟",
    "SOC_001": "异性饭局/神秘电话",
    "CONFLICT_001": "冲突处理",
}


def _join_list(values: list[Any] | tuple[Any, ...] | None) -> str:
    if not values:
        return "无"
    return "、".join(str(value) for value in values)


def _event_labels(event_ids: list[str] | None) -> str:
    return _join_list([EVENT_LABELS.get(event_id, event_id) for event_id in event_ids or []])


def _review(result: dict[str, Any]) -> dict[str, Any]:
    review = result.get("review") or {}
    return {
        "main_stage": review.get("main_stage", result.get("final_stage", "")),
        "sub_tags": review.get("sub_tags", []),
        "main_reasons": review.get("main_reasons", result.get("memory_summaries", [])),
        "turning_points": review.get("turning_points", []),
        "risks": review.get("risks", []),
        "repair_chances": review.get("repair_chances", []),
        "summary": review.get("summary", result.get("visible_summary", "")),
    }


def _add_numbered(lines: list[str], values: list[str]) -> None:
    for index, value in enumerate(values or ["暂无明显转折点。"], start=1):
        lines.append(f"{index}. {value}")


def _add_bullets(lines: list[str], values: list[str]) -> None:
    for value in values or ["暂无。"]:
        lines.append(f"- {value}")


def format_transcript(result: dict[str, Any]) -> str:
    review = _review(result)
    title = result.get("scenario_title") or result.get("pair_title") or "未指定场景"
    lines = [
        "# IF 关系复盘报告",
        "",
        f"场景：{title}",
        f"结局：{review['main_stage']}",
        f"副标签：{_join_list(review['sub_tags'])}",
        "",
        "关系概述：",
        str(review["summary"]),
        "",
        "关键转折点：",
    ]
    _add_numbered(lines, review["turning_points"])
    lines.extend(["", "主要原因："])
    _add_bullets(lines, review["main_reasons"])
    lines.extend(["", "后续隐患："])
    _add_bullets(lines, review["risks"])
    lines.extend(["", "修复机会："])
    _add_bullets(lines, review["repair_chances"])
    lines.extend(
        [
            "",
            f"涉及事件：{_event_labels(result.get('triggered_events'))}",
            "",
            "14 天记录：",
            "",
        ]
    )
    lines.extend(str(line) for line in result.get("transcript", []))
    return "\n".join(lines) + "\n"


def format_summary_report(result: dict[str, Any]) -> str:
    review = _review(result)
    title = result.get("scenario_title") or result.get("pair_title") or "未指定场景"
    lines = [
        "# IF 关系复盘摘要",
        "",
        f"场景：{title}",
        f"结局：{review['main_stage']}",
        f"副标签：{_join_list(review['sub_tags'])}",
        f"概述：{review['summary']}",
        f"记忆：{_join_list(result.get('memory_summaries'))}",
        "",
        "关键转折点：",
    ]
    _add_bullets(lines, review["turning_points"])
    lines.extend(["", "主要原因："])
    _add_bullets(lines, review["main_reasons"])
    lines.extend(["", "后续隐患："])
    _add_bullets(lines, review["risks"])
    lines.extend(["", "修复机会："])
    _add_bullets(lines, review["repair_chances"])
    return "\n".join(lines) + "\n"


def write_report(result: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(format_transcript(result), encoding="utf-8")
    return path


def write_scenario_summary(results: list[dict[str, Any]], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    sections = ["# IF 多场景关系复盘汇总", ""]
    for result in results:
        review = _review(result)
        title = result.get("scenario_title") or result.get("pair_title") or "未指定场景"
        sections.extend(
            [
                f"## {title}",
                f"结局：{review['main_stage']}",
                f"副标签：{_join_list(review['sub_tags'])}",
                f"概述：{review['summary']}",
                "",
                "关键转折点：",
            ]
        )
        _add_bullets(sections, review["turning_points"])
        sections.extend(["", "后续隐患："])
        _add_bullets(sections, review["risks"])
        sections.append("")
    path.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    return path

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from if_game.questionnaire.initial_modifiers import (
    build_initial_relationship_modifiers,
    format_initial_modifier_summary,
)


CORE_DIMENSIONS = [
    "attachment_abandonment_anxiety",
    "attachment_intimacy_avoidance",
    "attachment_closeness_need",
    "attachment_independence_need",
    "attachment_vulnerability_fear",
]

DIMENSION_LABELS = {
    "attachment_abandonment_anxiety": "稳定回应需求",
    "attachment_intimacy_avoidance": "亲密推进压力",
    "attachment_closeness_need": "亲密联系需求",
    "attachment_independence_need": "个人空间需求",
    "attachment_vulnerability_fear": "脆弱表达难度",
}

DIMENSION_BEHAVIOR_TEXT = {
    "attachment_abandonment_anxiety": {
        "high": "你在亲密关系中可能更需要稳定回应，消息延迟或态度变化容易影响安全感。",
        "low": "你面对回复延迟或短暂冷淡时通常较能先稳住判断。",
        "mid": "你对稳定回应有一定需要，但会根据具体关系阶段和压力情境变化。",
    },
    "attachment_intimacy_avoidance": {
        "high": "关系推进过快时，你可能需要更多时间确认节奏和边界。",
        "low": "你通常较能接受关系靠近，也更容易把亲密表达视为安全来源。",
        "mid": "你既能靠近，也会在部分场景中需要留出缓冲空间。",
    },
    "attachment_closeness_need": {
        "high": "你可能更重视日常分享、陪伴和持续联系。",
        "low": "你对联系频率的要求相对宽松，较能接受低频但稳定的互动。",
        "mid": "你需要一定联系和陪伴，但不一定要求全天候回应。",
    },
    "attachment_independence_need": {
        "high": "你在关系中会明显需要个人空间和自主安排。",
        "low": "你更容易接受生活融合，也较少把亲密视为束缚。",
        "mid": "你会在亲密和独立之间寻找平衡，具体取决于对方是否尊重边界。",
    },
    "attachment_vulnerability_fear": {
        "high": "你不安或难过时可能不太会直接表达脆弱，容易先隐藏真实需求。",
        "low": "你较能把需要和脆弱说出来，修复时更容易让对方理解发生了什么。",
        "mid": "你有表达真实需要的能力，但在压力较高时仍可能先保护自己。",
    },
}


def render_questionnaire_report(
    config: dict[str, Any],
    answers: Iterable[dict[str, Any]],
    score_result: dict[str, Any],
) -> str:
    dimension_scores = score_result.get("dimension_scores", {})
    evidence_count = score_result.get("evidence_count", {})
    answered_questions = int(score_result.get("answered_questions", 0))
    total_questions = int(score_result.get("total_questions", len(config.get("questions", []))))
    completion_rate = float(score_result.get("completion_rate", 0.0))
    answer_count = sum(1 for _ in answers)
    initial_modifiers = build_initial_relationship_modifiers(score_result)
    initial_modifier_summary = format_initial_modifier_summary(initial_modifiers)

    lines = [
        "IF 问卷 MVP 报告",
        "",
        "## 完成度",
        f"完成度：{_format_percent(completion_rate)}",
        f"已回答题数 / 总题数：{answered_questions} / {total_questions}",
        f"本次收到的答案记录数：{answer_count}",
        _completion_note(completion_rate),
        "",
        "## 关键维度摘要",
    ]

    for dimension in CORE_DIMENSIONS:
        score = _score_for_dimension(dimension_scores, dimension)
        evidence = int(evidence_count.get(dimension, 0))
        lines.append(
            f"- {DIMENSION_LABELS[dimension]}：{score_to_level(score)}。"
            f"{_behavior_text(dimension, score)}"
            f"（证据：{_evidence_text(evidence)}）"
        )

    lines.extend(
        [
            "",
            "## 亲密依恋摘要",
            _render_attachment_summary(dimension_scores),
            "",
            "## 沟通表露摘要",
            _render_communication_disclosure_summary(dimension_scores),
            "",
            "## 游戏初始倾向修正摘要",
            *_format_bullets(initial_modifier_summary),
            "",
            "## 风险提示",
            _render_risk_hint(dimension_scores),
            "",
            "## 后续游戏行为修正提示",
            "当前报告基于自述答案生成，不代表固定结论。后续游戏行为会继续修正画像，尤其是消息延迟、冲突修复、边界协商和脆弱表达相关选择。",
        ]
    )

    return "\n".join(lines)


def score_to_level(score: float) -> str:
    if score <= 20:
        return "很低"
    if score <= 40:
        return "较低"
    if score <= 60:
        return "中等"
    if score <= 80:
        return "较高"
    return "很高"


def _format_percent(completion_rate: float) -> str:
    return f"{round(completion_rate * 100)}%"


def _completion_note(completion_rate: float) -> str:
    if completion_rate >= 0.9:
        return "你完成了大部分 MVP 题目，报告可作为较完整的自述画像。"
    if completion_rate >= 0.7:
        return "报告可以反映主要倾向，但部分题目仍需要后续行为补充。"
    if completion_rate >= 0.5:
        return "报告只能作为粗略画像，后续游戏行为会更明显地修正。"
    if completion_rate >= 0.25:
        return "当前报告可信度有限，适合快速开始而非稳定画像。"
    return "当前答案不足以形成稳定画像，系统会更多依赖后续游戏行为。"


def _score_for_dimension(dimension_scores: dict[str, Any], dimension: str) -> float:
    value = dimension_scores.get(dimension, 50)
    return float(value)


def _behavior_text(dimension: str, score: float) -> str:
    bucket = "mid"
    if score >= 61:
        bucket = "high"
    elif score <= 40:
        bucket = "low"
    return DIMENSION_BEHAVIOR_TEXT[dimension][bucket]


def _evidence_text(evidence: int) -> str:
    if evidence <= 0:
        return "暂无直接题目"
    if evidence == 1:
        return "1 个题目"
    return f"{evidence} 个题目"


def _format_bullets(lines: list[str]) -> list[str]:
    return [f"- {line}" for line in lines]


def _render_attachment_summary(dimension_scores: dict[str, Any]) -> str:
    abandonment = _score_for_dimension(dimension_scores, "attachment_abandonment_anxiety")
    avoidance = _score_for_dimension(dimension_scores, "attachment_intimacy_avoidance")
    closeness = _score_for_dimension(dimension_scores, "attachment_closeness_need")
    independence = _score_for_dimension(dimension_scores, "attachment_independence_need")
    vulnerability = _score_for_dimension(dimension_scores, "attachment_vulnerability_fear")

    if abandonment >= 61 and independence >= 61:
        return (
            "你可能同时需要稳定回应和个人空间。关系里最重要的不是简单靠近或拉开距离，"
            "而是提前说明节奏：什么时候需要确认，什么时候需要独处。"
        )
    if avoidance >= 61 or vulnerability >= 61:
        return (
            "你在亲密推进、暴露脆弱或表达真实需要时可能会先保护自己。"
            "如果对方推进很快，清楚说明边界会比临时退开更利于关系稳定。"
        )
    if closeness >= 61 and abandonment < 61:
        return (
            "你重视亲密联系和日常分享，但当前结果没有显示特别强的失去担忧。"
            "稳定表达和持续互动会让这类关系更顺畅。"
        )
    return (
        "你的亲密需求、独立需求和脆弱表达目前处在相对中间的位置。"
        "后续游戏中的具体选择会继续细化你在不同压力下的关系模式。"
    )


def _render_communication_disclosure_summary(dimension_scores: dict[str, Any]) -> str:
    directness = _score_for_dimension(dimension_scores, "communication_directness")
    reassurance = _score_for_dimension(dimension_scores, "emotion_reassurance_need")
    transparency = _score_for_dimension(dimension_scores, "info_transparency_preference")
    phone_privacy = _score_for_dimension(dimension_scores, "digital_phone_privacy_need")
    double_standard = _score_for_dimension(dimension_scores, "boundary_double_standard")

    return "\n".join(
        [
            f"- 直接沟通：{score_to_level(directness)}，反映你是否倾向把需要和不安说清楚。",
            f"- 回应性需求：{score_to_level(reassurance)}，反映脆弱表达后对安慰、陪伴和情绪确认的需要。",
            f"- 透明期待：{score_to_level(transparency)}，反映你希望关系中信息公开到什么程度。",
            f"- 手机隐私需求：{score_to_level(phone_privacy)}，反映你对聊天记录、相册和数字空间边界的重视。",
            f"- 表露规则一致性风险：{score_to_level(double_standard)}，用于提示自己表露和期待对方表露之间是否可能不对称。",
        ]
    )


def _render_risk_hint(dimension_scores: dict[str, Any]) -> str:
    risks: list[str] = []

    if _score_for_dimension(dimension_scores, "attachment_abandonment_anxiety") >= 61:
        risks.append("对方长时间不回应时，你可能更容易进入确认需求，需要把不安表达成具体请求。")
    if _score_for_dimension(dimension_scores, "attachment_intimacy_avoidance") >= 61:
        risks.append("关系推进过快时，你可能需要降速选项，避免用冷淡或回避代替说明。")
    if _score_for_dimension(dimension_scores, "attachment_independence_need") >= 61:
        risks.append("个人空间需求较高时，要提前协商联系规则，减少对方误读为不在意。")
    if _score_for_dimension(dimension_scores, "attachment_vulnerability_fear") >= 61:
        risks.append("压力下隐藏脆弱可能让对方误判你的真实需要，修复时建议先说明感受。")
    if _score_for_dimension(dimension_scores, "info_transparency_preference") >= 61:
        risks.append("透明期待较高时，需要把“必要坦白”和“正当隐私”提前协商清楚。")
    if _score_for_dimension(dimension_scores, "boundary_double_standard") >= 61:
        risks.append("如果自己保留较多、却要求对方高度坦白，关系中容易出现透明规则不一致。")

    if not risks:
        risks.append("当前 MVP 结果没有显示单一高风险方向，但证据仍来自自述题，后续行为会继续校准。")

    return "\n".join(f"- {risk}" for risk in risks)

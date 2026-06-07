from __future__ import annotations

from typing import Any, Literal, Mapping


DisclosureStyle = Literal["truthful", "half_truth", "hidden"]
PhoneBoundaryVisibility = Literal["hidden", "discovered"]
RepairStyle = Literal["accountable", "blame_shift"]


AGGREGATOR_INPUT_FIELDS = {
    "truth_type",
    "truth_harm_level",
    "deception_level",
    "evidence_chain_strength",
    "interpretation_type",
    "interpretation_accuracy",
    "projection_bias_effect",
    "threat_bias_effect",
    "communication_response_type",
    "perceived_responsiveness",
    "conflict_escalation_risk",
    "conflict_response_type",
    "defensive_response",
    "contempt_signal",
    "active_listening_skill",
    "validation_skill",
    "stonewalling_level",
    "repair_attempt_quality",
    "relationship_rewards_delta",
    "relationship_costs_delta",
    "approach_reward_delta",
    "avoidance_cost_pressure_delta",
    "relationship_excitement_delta",
    "relationship_safety_delta",
    "boredom_delta",
    "perceived_equity_delta",
    "underbenefit_feeling_delta",
    "overbenefit_guilt_delta",
    "felt_appreciation_delta",
    "taken_for_granted_delta",
    "dependence_delta",
    "privacy_boundary_conflict",
    "occurrence_count",
    "repair_status",
    "pattern_key",
    "timeout_repair_success",
    "trust_building_delta",
}


def supportive_listening_event(
    source_id: str = "player",
    target_id: str = "npc_a",
) -> dict[str, Any]:
    """E-REL-TRU-01: player listens carefully when the partner is low."""

    return {
        "event_id": "E-REL-TRU-01",
        "event_type": "trust_support",
        "title": "低落时认真倾听",
        "short_description": "对方情绪低落时，玩家没有急着评判，而是确认感受并问清需要什么。",
        "trigger": "npc_low_mood_after_work",
        "context": "日常压力下的一次支持性沟通。",
        "source_id": source_id,
        "target_id": target_id,
        "visibility": "public",
        "relationship_delta": {
            "trust_building_delta": 6,
            "relationship_safety_delta": 5,
            "relationship_rewards_delta": 4,
            "avoidance_cost_pressure_delta": -3,
            "perceived_responsiveness": 8,
            "validation_skill": 8,
            "active_listening_skill": 8,
            "repair_attempt_quality": 7,
            "repair_status": "partially_repaired",
            "pattern_key": "reliable_emotional_support",
        },
        "memory_candidate": {
            "memory_type": "repair_memory",
            "note": "对方记得玩家曾经认真接住情绪，并愿意沟通。",
            "visibility": "player_visible",
        },
    }


def forgotten_small_promise_event(
    source_id: str = "player",
    target_id: str = "npc_a",
) -> dict[str, Any]:
    """E-REL-MIN-01: player forgets a small promise and explains poorly."""

    return {
        "event_id": "E-REL-MIN-01",
        "event_type": "minor_reliability_damage",
        "title": "忘记一个小承诺",
        "short_description": "玩家答应顺手带东西却忘了，解释也有点含糊。",
        "trigger": "minor_promise_missed",
        "context": "一次轻微失约，不应直接升级成重大背叛。",
        "source_id": source_id,
        "target_id": target_id,
        "visibility": "public",
        "relationship_delta": {
            "truth_type": "minor_forgetfulness",
            "truth_harm_level": 2,
            "deception_level": 0,
            "evidence_chain_strength": "weak",
            "relationship_costs_delta": 2,
            "perceived_responsiveness": 2,
            "conflict_escalation_risk": 2,
            "trust_building_delta": -2,
            "pattern_key": "minor_promise_forgetfulness",
        },
        "memory_candidate": {
            "memory_type": "neutral_context_memory",
            "note": "轻微失约只作为后续观察背景，不直接写成旧伤。",
            "visibility": "player_visible",
        },
    }


def phone_boundary_event(
    visibility: PhoneBoundaryVisibility = "hidden",
    source_id: str = "player",
    target_id: str = "npc_a",
) -> dict[str, Any]:
    """E-REL-PRI-01: phone privacy boundary sample, hidden or discovered."""

    discovered = visibility == "discovered"
    relationship_delta: dict[str, Any] = {
        "truth_type": "privacy_boundary",
        "truth_harm_level": 0,
        "deception_level": 0,
        "evidence_chain_strength": 0,
        "pattern_key": "privacy_boundary_conflict",
    }
    hidden_delta = {
        "hidden_tension_delta": 3,
        "guilt_delta": 2,
        "privacy_risk_delta": 4,
    }

    if discovered:
        relationship_delta.update(
            truth_harm_level=2,
            privacy_boundary_conflict=8,
            evidence_chain_strength="strong",
            relationship_costs_delta=3,
            conflict_escalation_risk=5,
        )

    return {
        "event_id": "E-REL-PRI-01",
        "event_type": "privacy_boundary",
        "title": "手机边界被触碰",
        "short_description": "玩家越过手机边界；未被发现时只留下隐性压力，被发现后才进入公开冲突。",
        "trigger": "phone_privacy_boundary",
        "context": "数字生活和隐私边界事件。",
        "source_id": source_id,
        "target_id": target_id,
        "visibility": visibility,
        "relationship_delta": relationship_delta,
        "hidden_relationship_delta": hidden_delta,
        "memory_candidate": {
            "memory_type": "neutral_context_memory" if not discovered else "old_wound_memory",
            "note": "未被发现时不写公开旧伤；被发现后会成为边界协商材料。",
            "visibility": "debug_only" if not discovered else "player_visible",
        },
    }


def accountability_repair_event(
    style: RepairStyle = "accountable",
    source_id: str = "player",
    target_id: str = "npc_a",
) -> dict[str, Any]:
    """E-REL-REP-01: conflict repair sample with accountable or defensive response."""

    if style == "accountable":
        return {
            "event_id": "E-REL-REP-01",
            "event_type": "conflict_repair",
            "title": "道歉并承认责任",
            "short_description": "玩家承认自己说重了，并提出下次暂停后回来继续谈。",
            "trigger": "post_conflict_repair",
            "context": "矛盾后的修复尝试。",
            "source_id": source_id,
            "target_id": target_id,
            "visibility": "public",
            "relationship_delta": {
                "conflict_response_type": "repair_attempt",
                "conflict_escalation_risk": 2,
                "validation_skill": 7,
                "active_listening_skill": 6,
                "repair_attempt_quality": 8,
                "timeout_repair_success": True,
                "repair_status": "partially_repaired",
                "perceived_responsiveness": 7,
                "trust_building_delta": 3,
                "pattern_key": "accountable_conflict_repair",
            },
            "memory_candidate": {
                "memory_type": "repair_memory",
                "note": "对方记得这次冲突被认真修复过。",
                "visibility": "player_visible",
            },
        }

    if style == "blame_shift":
        return {
            "event_id": "E-REL-REP-01B",
            "event_type": "conflict_repair",
            "title": "解释但推卸责任",
            "short_description": "玩家说自己不是故意的，但把主要责任推给对方太敏感。",
            "trigger": "post_conflict_repair",
            "context": "矛盾后的低质量解释。",
            "source_id": source_id,
            "target_id": target_id,
            "visibility": "public",
            "relationship_delta": {
                "conflict_response_type": "defensive_explanation",
                "conflict_escalation_risk": 6,
                "defensive_response": 7,
                "validation_skill": 1,
                "repair_attempt_quality": 1,
                "perceived_responsiveness": 1,
                "relationship_costs_delta": 3,
                "pattern_key": "conflict_defensiveness",
            },
            "memory_candidate": {
                "memory_type": "pattern_memory",
                "note": "若类似回应反复出现，才进入防卫模式记忆。",
                "visibility": "player_visible",
            },
        }

    raise ValueError(f"unsupported repair style: {style}")


def dinner_disclosure_event(
    style: DisclosureStyle = "truthful",
    source_id: str = "player",
    target_id: str = "npc_a",
) -> dict[str, Any]:
    """E-REL-SEC-01: player discloses, half-discloses, or hides a dinner plan."""

    base = {
        "event_id": "E-REL-SEC-01",
        "event_type": "truth_disclosure",
        "title": "异性约饭后的说明",
        "trigger": "after_opposite_gender_dinner",
        "context": "真实说明、半真半假和完全隐瞒的对照样例。",
        "source_id": source_id,
        "target_id": target_id,
    }

    if style == "truthful":
        return {
            **base,
            "short_description": "玩家主动说明约饭对象和原因，也愿意讨论边界。",
            "visibility": "public",
            "relationship_delta": {
                "truth_type": "benign_reason",
                "truth_harm_level": 1,
                "deception_level": 0,
                "evidence_chain_strength": "weak",
                "privacy_boundary_conflict": 2,
                "validation_skill": 6,
                "repair_attempt_quality": 6,
                "perceived_responsiveness": 6,
                "relationship_rewards_delta": 2,
                "trust_building_delta": 2,
                "pattern_key": "transparent_dinner_disclosure",
            },
            "memory_candidate": {
                "memory_type": "repair_memory",
                "note": "真实说明可能带来短期波动，但长期信任损伤较小。",
                "visibility": "player_visible",
            },
            "interpretation_event": _dinner_interpretation_payload(style),
        }

    if style == "half_truth":
        return {
            **base,
            "short_description": "玩家说了约饭，但省略对方曾经暧昧过的背景。",
            "visibility": "public",
            "relationship_delta": {
                "truth_type": "privacy_boundary",
                "truth_harm_level": 3,
                "deception_level": 3,
                "evidence_chain_strength": "moderate",
                "privacy_boundary_conflict": 4,
                "relationship_costs_delta": 3,
                "conflict_escalation_risk": 4,
                "pattern_key": "half_truth_dinner_disclosure",
            },
            "memory_candidate": {
                "memory_type": "neutral_context_memory",
                "note": "半真半假会留下后续查证风险，但不直接等同重大背叛。",
                "visibility": "player_visible",
            },
            "interpretation_event": _dinner_interpretation_payload(style),
        }

    if style == "hidden":
        return {
            **base,
            "short_description": "玩家完全不提这次约饭，当前没有被发现。",
            "visibility": "hidden",
            "relationship_delta": {
                "truth_type": "private_space",
                "truth_harm_level": 0,
                "deception_level": 0,
                "evidence_chain_strength": 0,
                "pattern_key": "hidden_dinner_disclosure",
            },
            "hidden_relationship_delta": {
                "hidden_tension_delta": 4,
                "future_discovery_risk_delta": 6,
            },
            "memory_candidate": {
                "memory_type": "neutral_context_memory",
                "note": "未被发现时不生成公开冲突；后续若揭露，风险会被重新计算。",
                "visibility": "debug_only",
            },
            "interpretation_event": _dinner_interpretation_payload(style),
        }

    raise ValueError(f"unsupported disclosure style: {style}")


def relationship_event_samples() -> list[dict[str, Any]]:
    """Return the default small sample set for relationship-chain tests."""

    return [
        supportive_listening_event(),
        forgotten_small_promise_event(),
        phone_boundary_event("hidden"),
        accountability_repair_event("accountable"),
        dinner_disclosure_event("half_truth"),
    ]


def event_to_aggregator_input(event: Mapping[str, Any]) -> dict[str, Any]:
    """Flatten one sample event into relationship_state_aggregator input."""

    relationship_delta = dict(_mapping(event.get("relationship_delta")))
    return {
        "event_id": str(event.get("event_id", "")),
        "event_type": str(event.get("event_type", "relationship_event")),
        "source_id": str(event.get("source_id", relationship_delta.get("source_id", ""))),
        "target_id": str(event.get("target_id", relationship_delta.get("target_id", ""))),
        **{key: value for key, value in relationship_delta.items() if key in AGGREGATOR_INPUT_FIELDS},
    }


def event_to_interpretation_input(event: Mapping[str, Any]) -> dict[str, Any]:
    """Return the optional interpretation payload for samples that define one."""

    payload = _mapping(event.get("interpretation_event"))
    if not payload:
        raise ValueError(f"event {event.get('event_id', '')} has no interpretation payload")
    return dict(payload)


def _dinner_interpretation_payload(style: DisclosureStyle) -> dict[str, Any]:
    if style == "truthful":
        return {
            "event_id": "E-REL-SEC-01:truthful",
            "player_judgment": "trust_no_problem",
            "truth": {
                "truth_type": "busy",
                "truth_reason": "普通工作约饭，主动补充边界信息",
                "truth_intention": "减少误会",
                "truth_harm_level": 10,
                "truth_priority_signal": 8,
                "truth_moral_severity": 0,
            },
            "explanation": {
                "explanation_claim": "今天和同事吃饭，我提前告诉你，也可以讲清楚边界。",
                "explanation_specificity": 85,
                "explanation_consistency": 84,
                "explanation_plausibility": 82,
                "behavior_explanation_gap": 4,
                "excuse_repetition_count": 0,
                "supporting_evidence_strength": 18,
            },
            "observable_traces": {},
        }

    if style == "half_truth":
        return {
            "event_id": "E-REL-SEC-01:half_truth",
            "player_judgment": "suspect_problem",
            "truth": {
                "truth_type": "neglect",
                "truth_reason": "说了约饭，但省略对方曾经暧昧过的背景",
                "truth_intention": "避免当下冲突",
                "truth_harm_level": 35,
                "truth_priority_signal": 45,
                "truth_moral_severity": 20,
            },
            "explanation": {
                "explanation_claim": "只是普通朋友吃个饭，没什么特别的。",
                "explanation_specificity": 45,
                "explanation_consistency": 50,
                "explanation_plausibility": 58,
                "behavior_explanation_gap": 18,
                "excuse_repetition_count": 1,
                "supporting_evidence_strength": 8,
            },
            "observable_traces": {
                "changed_routine_trace": False,
                "explanation_timing_conflict": True,
            },
        }

    return {
        "event_id": "E-REL-SEC-01:hidden",
        "player_judgment": "trust_no_problem",
        "truth": {
            "truth_type": "private_space",
            "truth_reason": "没有主动提起约饭",
            "truth_intention": "暂时不想解释",
            "truth_harm_level": 5,
            "truth_priority_signal": 5,
            "truth_moral_severity": 0,
        },
        "explanation": {
            "explanation_claim": "",
            "explanation_specificity": 50,
            "explanation_consistency": 50,
            "explanation_plausibility": 50,
            "behavior_explanation_gap": 0,
            "excuse_repetition_count": 0,
            "supporting_evidence_strength": 0,
        },
        "observable_traces": {},
    }


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Iterable, Mapping


PERSONALITY_FIELDS = (
    "emotional_stability",
    "jealousy",
    "forgiveness",
    "conflict_avoidance",
    "communication_drive",
    "revenge_tendency",
    "attachment_anxiety",
    "honesty_expectation",
    "self_respect",
)

REACTION_TYPES = (
    "appreciate",
    "soften",
    "communicate",
    "forgive",
    "withdraw",
    "become_sad",
    "confront",
    "test_player",
    "cold_war",
    "passive_aggressive",
    "repair_attempt",
    "set_boundary",
    "record_grievance",
    "retaliate",
    "breakup_warning",
)

DEFAULT_PERSONALITY_VALUE = 50
DEFAULT_STATE = {
    "trust": 50,
    "safety": 50,
    "satisfaction": 50,
    "conflict_risk": 0,
    "deception_risk": 0,
    "repair_chance": 50,
    "hidden_tension": 0,
    "suspicion": 0,
    "unresolved_conflicts": 0,
}

POSITIVE_EVENT_TYPES = {"positive_support", "trust_support", "supportive_listening"}
REPAIR_EVENT_TYPES = {"repair_attempt", "conflict_repair"}
MINOR_EVENT_TYPES = {"minor_disappointment", "minor_reliability_damage"}
PRIVACY_EVENT_TYPES = {"privacy_boundary"}
DECEPTION_EVENT_TYPES = {"deception", "truth_disclosure", "concealment"}
NEGLECT_EVENT_TYPES = {"neglect", "emotional_neglect"}
BETRAYAL_EVENT_TYPES = {"betrayal_like", "betrayal"}
NEGATIVE_EVENT_TYPES = (
    MINOR_EVENT_TYPES
    | PRIVACY_EVENT_TYPES
    | DECEPTION_EVENT_TYPES
    | NEGLECT_EVENT_TYPES
    | BETRAYAL_EVENT_TYPES
)

PUBLIC_CONFLICT_REACTIONS = {"confront", "cold_war", "retaliate", "breakup_warning"}
LEVEL_SCORES = {
    "none": 0,
    "low": 25,
    "weak": 25,
    "minor": 25,
    "medium": 50,
    "moderate": 50,
    "high": 80,
    "strong": 80,
    "critical": 100,
    "conclusive": 100,
}


@dataclass(frozen=True)
class NPCReactionDecision:
    reaction_type: str
    intensity: int
    public_conflict: bool
    relationship_delta: dict[str, int] = field(default_factory=dict)
    memory_candidate: dict[str, Any] = field(default_factory=dict)
    explanation: str = ""
    followup_risk: int = 0
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def decide_npc_reaction(
    event: Mapping[str, Any] | Any,
    personality: Mapping[str, Any] | Any | None = None,
    relationship_state: Mapping[str, Any] | Any | None = None,
    memories: Iterable[Any] | Mapping[str, Any] | Any | None = None,
) -> NPCReactionDecision:
    """Decide one lightweight NPC reaction from event, personality, state, and memories.

    The MVP is deterministic and intentionally local. It does not mutate game state
    and does not replace the relationship aggregator or long-term memory system.
    """

    event_data = _mapping(event)
    personality_data = _normalize_personality(personality)
    state = _normalize_relationship_state(relationship_state)
    memory_profile = _memory_profile(memories, event_data)
    event_profile = _event_profile(event_data)

    tags: list[str] = []
    if event_profile["hidden_undiscovered"]:
        _add(tags, "hidden_undiscovered")
    if memory_profile["old_wound_load"] > 0:
        _add(tags, "memory_sensitive")
    if memory_profile["repeated_deception"] > 0:
        _add(tags, "repeated_deception_memory")

    if event_profile["event_type"] in POSITIVE_EVENT_TYPES:
        return _positive_reaction(event_profile, personality_data, state, memory_profile, tags)

    if event_profile["event_type"] in REPAIR_EVENT_TYPES:
        return _repair_reaction(event_profile, personality_data, state, memory_profile, tags)

    if event_profile["hidden_undiscovered"]:
        return _hidden_reaction(event_profile, personality_data, state, memory_profile, tags)

    return _negative_reaction(event_profile, personality_data, state, memory_profile, tags)


def _positive_reaction(
    event: Mapping[str, Any],
    personality: Mapping[str, int],
    state: Mapping[str, int],
    memory: Mapping[str, int],
    tags: list[str],
) -> NPCReactionDecision:
    severity = int(event["severity"])
    old_wound = int(memory["old_wound_load"])
    repair_chance = int(state["repair_chance"])

    if old_wound >= 25 and repair_chance >= 45:
        reaction_type = "soften"
        explanation = "The support lands as a repair signal because old hurt still exists but the relationship can recover."
        _add(tags, "old_wound_softened")
    else:
        reaction_type = "appreciate"
        explanation = "The behavior is read as reliable emotional support, so the NPC responds warmly."

    intensity = _clamp_int(35 + severity * 0.25 + personality["communication_drive"] * 0.08 - old_wound * 0.1)
    followup_risk = _clamp_int(memory["old_wound_load"] * 0.15 + state["hidden_tension"] * 0.1)
    relationship_delta = {
        "trust_delta": 2,
        "safety_delta": 2,
        "satisfaction_delta": 3,
        "repair_chance_delta": 4 if reaction_type == "soften" else 2,
        "conflict_risk_delta": -2,
    }

    return NPCReactionDecision(
        reaction_type=reaction_type,
        intensity=intensity,
        public_conflict=False,
        relationship_delta=relationship_delta,
        memory_candidate={
            "memory_type": "positive_support_memory",
            "tags": ["reliable_support"],
            "weight": max(1, intensity // 20),
        },
        explanation=explanation,
        followup_risk=followup_risk,
        tags=_unique(tags + ["positive_support"]),
    )


def _repair_reaction(
    event: Mapping[str, Any],
    personality: Mapping[str, int],
    state: Mapping[str, int],
    memory: Mapping[str, int],
    tags: list[str],
) -> NPCReactionDecision:
    severity = int(event["severity"])
    quality = int(event["repair_quality"])
    old_wound = int(memory["old_wound_load"])
    repeated_deception = int(memory["repeated_deception"])
    blame_shift = bool(event["blame_shift"])

    if blame_shift or quality < 40:
        _add(tags, "low_quality_repair")
        if personality["self_respect"] >= 70 or personality["honesty_expectation"] >= 70:
            reaction_type = "set_boundary"
            explanation = "The apology avoids responsibility, so the NPC treats it as a boundary issue rather than repair."
        elif personality["conflict_avoidance"] >= 70:
            reaction_type = "withdraw"
            explanation = "The repair attempt feels unsafe or evasive, so the NPC pulls back."
        else:
            reaction_type = "communicate"
            explanation = "The NPC asks for a clearer repair because blame shifting does not count as real accountability."
        intensity = _clamp_int(35 + severity * 0.35 + old_wound * 0.25)
        return NPCReactionDecision(
            reaction_type=reaction_type,
            intensity=intensity,
            public_conflict=reaction_type == "set_boundary",
            relationship_delta={
                "trust_delta": -1,
                "satisfaction_delta": -2,
                "repair_chance_delta": -3,
                "conflict_risk_delta": 2,
            },
            memory_candidate={
                "memory_type": "pattern_memory",
                "tags": ["defensive_repair", "unresolved_conflict"],
                "weight": max(1, intensity // 25),
            },
            explanation=explanation,
            followup_risk=_clamp_int(30 + old_wound * 0.35 + repeated_deception * 0.4),
            tags=_unique(tags),
        )

    repair_score = (
        quality * 0.45
        + personality["forgiveness"] * 0.25
        + personality["communication_drive"] * 0.2
        + state["repair_chance"] * 0.15
        + memory["repaired_after_conflict"] * 0.15
        - old_wound * 0.25
        - repeated_deception * 0.35
    )

    if repair_score >= 70:
        reaction_type = "forgive"
        explanation = "The NPC can accept the repair because it includes accountability and there is enough repair capacity."
    elif personality["communication_drive"] >= 65:
        reaction_type = "repair_attempt"
        explanation = "The NPC is not fully over it, but chooses to keep the repair conversation open."
    else:
        reaction_type = "soften"
        explanation = "The repair lowers the tension, though it does not erase the old hurt."

    weakened = old_wound >= 30 or repeated_deception >= 25
    if weakened:
        _add(tags, "repair_effect_weakened")
    intensity = _clamp_int(35 + quality * 0.35 + (100 - personality["emotional_stability"]) * 0.08)
    followup_risk = _clamp_int(15 + old_wound * 0.45 + repeated_deception * 0.5 - quality * 0.15)
    relationship_delta = {
        "trust_delta": 1 if weakened else 2,
        "safety_delta": 1,
        "satisfaction_delta": 1 if weakened else 2,
        "repair_chance_delta": 2 if weakened else 5,
        "conflict_risk_delta": -1 if weakened else -3,
    }

    return NPCReactionDecision(
        reaction_type=reaction_type,
        intensity=intensity,
        public_conflict=False,
        relationship_delta=relationship_delta,
        memory_candidate={
            "memory_type": "repair_memory",
            "tags": ["repaired_after_conflict"],
            "weight": max(1, intensity // 20),
        },
        explanation=explanation,
        followup_risk=followup_risk,
        tags=_unique(tags + ["accountable_repair"]),
    )


def _hidden_reaction(
    event: Mapping[str, Any],
    personality: Mapping[str, int],
    state: Mapping[str, int],
    memory: Mapping[str, int],
    tags: list[str],
) -> NPCReactionDecision:
    severity = int(event["severity"])
    suspicion_pressure = (
        severity * 0.25
        + personality["jealousy"] * 0.15
        + personality["attachment_anxiety"] * 0.15
        + state["suspicion"] * 0.25
        + memory["old_wound_load"] * 0.25
    )
    reaction_type = "record_grievance" if suspicion_pressure >= 45 else "become_sad"
    explanation = (
        "The event is hidden or private and not discovered, so it becomes internal tension rather than open conflict."
    )
    intensity = _clamp_int(min(65, 20 + suspicion_pressure))
    followup_risk = _clamp_int(25 + severity * 0.25 + memory["old_wound_load"] * 0.35)

    return NPCReactionDecision(
        reaction_type=reaction_type,
        intensity=intensity,
        public_conflict=False,
        relationship_delta={
            "trust_delta": 0,
            "safety_delta": 0,
            "satisfaction_delta": 0,
            "hidden_tension_delta": max(1, severity // 20),
            "suspicion_delta": max(1, int(suspicion_pressure // 25)),
            "conflict_risk_delta": 0,
        },
        memory_candidate={
            "memory_type": "latent_tension_memory",
            "tags": ["internalized_suspicion"],
            "visibility": "debug_only",
            "weight": max(1, intensity // 25),
        },
        explanation=explanation,
        followup_risk=followup_risk,
        tags=_unique(tags + ["internalized_suspicion"]),
    )


def _negative_reaction(
    event: Mapping[str, Any],
    personality: Mapping[str, int],
    state: Mapping[str, int],
    memory: Mapping[str, int],
    tags: list[str],
) -> NPCReactionDecision:
    severity = int(event["severity"])
    old_wound = int(memory["old_wound_load"])
    repeated_deception = int(memory["repeated_deception"])
    low_satisfaction = 100 - int(state["satisfaction"])
    low_safety = 100 - int(state["safety"])
    is_deception_or_betrayal = bool(event["is_deception_or_betrayal"])

    if (
        is_deception_or_betrayal
        and severity >= 60
        and personality["self_respect"] >= 80
        and low_satisfaction >= 60
        and old_wound >= 30
    ):
        reaction_type = "breakup_warning"
        explanation = "High self-respect, low satisfaction, and unresolved hurt push the NPC to name a bottom line."
    elif (
        is_deception_or_betrayal
        and severity >= 60
        and personality["revenge_tendency"] >= 80
        and personality["forgiveness"] <= 35
        and (low_safety >= 50 or old_wound >= 25 or repeated_deception >= 25)
    ):
        reaction_type = "retaliate"
        explanation = "Retaliation only appears because a discovered deception meets high revenge, low forgiveness, and low safety."
    elif personality["conflict_avoidance"] >= 80 and personality["communication_drive"] <= 50:
        reaction_type = "cold_war" if severity >= 55 else "withdraw"
        explanation = "The NPC avoids direct conflict and lets distance carry the reaction."
    elif personality["jealousy"] >= 75 and personality["attachment_anxiety"] >= 70:
        reaction_type = "confront" if severity >= 50 else "test_player"
        explanation = "Jealousy and attachment anxiety make the NPC seek proof or direct answers."
    elif personality["communication_drive"] >= 75 and personality["forgiveness"] >= 65 and personality["revenge_tendency"] < 65:
        reaction_type = "communicate"
        explanation = "The NPC is hurt, but high communication and forgiveness make direct repair more likely than retaliation."
    elif personality["self_respect"] >= 75 and severity >= 50:
        reaction_type = "set_boundary"
        explanation = "The NPC responds by naming a boundary rather than escalating into revenge."
    elif personality["forgiveness"] >= 70 and severity <= 45:
        reaction_type = "forgive"
        explanation = "The harm is limited enough for a forgiving NPC to let it pass with caution."
    else:
        reaction_type = "become_sad"
        explanation = "The event hurts the NPC, but the strongest response is sadness rather than payback."

    public_conflict = reaction_type in PUBLIC_CONFLICT_REACTIONS
    if not event["discovered"] and event["visibility"] in {"hidden", "private"}:
        public_conflict = False

    intensity = _negative_intensity(event, personality, state, memory, reaction_type)
    followup_risk = _negative_followup_risk(event, personality, state, memory, reaction_type)
    relationship_delta = _negative_relationship_delta(event, reaction_type, public_conflict)
    memory_candidate = _negative_memory_candidate(event, reaction_type, intensity, old_wound)

    return NPCReactionDecision(
        reaction_type=reaction_type,
        intensity=intensity,
        public_conflict=public_conflict,
        relationship_delta=relationship_delta,
        memory_candidate=memory_candidate,
        explanation=explanation,
        followup_risk=followup_risk,
        tags=_unique(tags + _negative_tags(event, reaction_type)),
    )


def _negative_intensity(
    event: Mapping[str, Any],
    personality: Mapping[str, int],
    state: Mapping[str, int],
    memory: Mapping[str, int],
    reaction_type: str,
) -> int:
    severity = int(event["severity"])
    base = (
        severity * 0.55
        + memory["old_wound_load"] * 0.25
        + state["conflict_risk"] * 0.15
        + state["suspicion"] * 0.15
        + (100 - personality["emotional_stability"]) * 0.12
    )
    if reaction_type in {"retaliate", "breakup_warning"}:
        base += 15
    elif reaction_type in {"confront", "cold_war"}:
        base += 8
    return _clamp_int(base)


def _negative_followup_risk(
    event: Mapping[str, Any],
    personality: Mapping[str, int],
    state: Mapping[str, int],
    memory: Mapping[str, int],
    reaction_type: str,
) -> int:
    risk = (
        event["severity"] * 0.35
        + memory["old_wound_load"] * 0.35
        + memory["repeated_deception"] * 0.35
        + state["deception_risk"] * 0.2
        + state["hidden_tension"] * 0.2
    )
    if reaction_type in {"retaliate", "breakup_warning", "cold_war"}:
        risk += 20
    elif reaction_type in {"communicate", "repair_attempt", "forgive"}:
        risk -= 10
    return _clamp_int(risk)


def _negative_relationship_delta(
    event: Mapping[str, Any],
    reaction_type: str,
    public_conflict: bool,
) -> dict[str, int]:
    severity = int(event["severity"])
    trust_loss = 0 if not event["discovered"] else max(1, severity // 25)
    delta = {
        "trust_delta": -trust_loss,
        "safety_delta": -max(1, severity // 30),
        "satisfaction_delta": -max(1, severity // 25),
        "repair_chance_delta": -1,
        "conflict_risk_delta": 1 if public_conflict else 0,
    }
    if reaction_type in {"communicate", "set_boundary"}:
        delta["repair_chance_delta"] = 1
    if reaction_type in {"cold_war", "retaliate", "breakup_warning"}:
        delta["repair_chance_delta"] = -4
        delta["conflict_risk_delta"] = 3
    if reaction_type == "withdraw":
        delta["conflict_risk_delta"] = 0
    return delta


def _negative_memory_candidate(
    event: Mapping[str, Any],
    reaction_type: str,
    intensity: int,
    old_wound: int,
) -> dict[str, Any]:
    if reaction_type in {"retaliate", "breakup_warning", "cold_war"} or old_wound >= 30:
        memory_type = "old_wound_memory"
    elif reaction_type == "record_grievance":
        memory_type = "grievance_memory"
    else:
        memory_type = "neutral_context_memory"

    tags = []
    if event["is_deception_or_betrayal"]:
        tags.append("deception_reaction")
    if reaction_type == "set_boundary":
        tags.append("boundary_set")
    if reaction_type in {"retaliate", "breakup_warning"}:
        tags.append("high_harm_reaction")

    return {
        "memory_type": memory_type,
        "tags": tags,
        "weight": max(1, intensity // 20),
    }


def _negative_tags(event: Mapping[str, Any], reaction_type: str) -> list[str]:
    tags = ["negative_event", reaction_type]
    if event["is_deception_or_betrayal"]:
        tags.append("deception_or_betrayal")
    if reaction_type == "retaliate":
        tags.append("retaliation_not_default")
    if reaction_type == "breakup_warning":
        tags.append("bottom_line_warning")
    return tags


def _event_profile(event: Mapping[str, Any]) -> dict[str, Any]:
    event_type = _normalized_event_type(str(event.get("event_type", "minor_disappointment")))
    relationship_delta = _mapping(event.get("relationship_delta"))
    visibility = str(event.get("visibility", "public")).strip().lower() or "public"
    discovered = _discovered(event, visibility)
    severity = _event_severity(event, relationship_delta, event_type)
    repair_quality = _repair_quality(event, relationship_delta)
    blame_shift = _blame_shift(event, relationship_delta)
    truth_type = str(relationship_delta.get("truth_type", event.get("truth_type", ""))).strip()
    is_deception_or_betrayal = (
        event_type in DECEPTION_EVENT_TYPES
        or event_type in BETRAYAL_EVENT_TYPES
        or _score_100(relationship_delta.get("deception_level", event.get("deception_level", 0))) >= 35
        or truth_type in {"concealment", "betrayal", "manipulation", "boundary_blur"}
    )
    if event_type == "truth_disclosure" and not is_deception_or_betrayal:
        event_type = "privacy_boundary" if truth_type in {"privacy_boundary", "private_space"} else "minor_disappointment"

    return {
        "event_id": str(event.get("event_id", "")),
        "event_type": event_type,
        "severity": severity,
        "visibility": visibility,
        "discovered": discovered,
        "hidden_undiscovered": visibility in {"hidden", "private"} and not discovered,
        "relationship_delta": relationship_delta,
        "memory_tags": _as_list(event.get("memory_tags")),
        "memory_candidate": _mapping(event.get("memory_candidate")),
        "context": str(event.get("context", "")),
        "repair_quality": repair_quality,
        "blame_shift": blame_shift,
        "is_deception_or_betrayal": is_deception_or_betrayal,
    }


def _normalized_event_type(value: str) -> str:
    normalized = value.strip().lower()
    aliases = {
        "trust_support": "positive_support",
        "supportive_listening": "positive_support",
        "minor_reliability_damage": "minor_disappointment",
        "conflict_repair": "repair_attempt",
        "truth_disclosure": "deception",
    }
    return aliases.get(normalized, normalized or "minor_disappointment")


def _discovered(event: Mapping[str, Any], visibility: str) -> bool:
    if "discovered" in event:
        return bool(event.get("discovered"))
    if visibility == "discovered":
        return True
    if visibility in {"hidden", "private"}:
        return False
    return True


def _event_severity(
    event: Mapping[str, Any],
    relationship_delta: Mapping[str, Any],
    event_type: str,
) -> int:
    if "severity" in event:
        return _score_100(event.get("severity", 0))

    candidates = [
        _score_100(relationship_delta.get("truth_harm_level", 0)),
        _score_100(relationship_delta.get("deception_level", 0)),
        _score_100(relationship_delta.get("relationship_costs_delta", 0)),
        _score_100(relationship_delta.get("conflict_escalation_risk", 0)),
        _score_100(relationship_delta.get("privacy_boundary_conflict", 0)),
    ]
    severity = max(candidates)
    defaults = {
        "positive_support": 35,
        "repair_attempt": 45,
        "minor_disappointment": 30,
        "privacy_boundary": 45,
        "deception": 65,
        "neglect": 55,
        "betrayal_like": 75,
    }
    return max(defaults.get(event_type, 40), severity)


def _repair_quality(event: Mapping[str, Any], relationship_delta: Mapping[str, Any]) -> int:
    return max(
        _score_100(event.get("repair_quality", event.get("repair_attempt_quality", 0))),
        _score_100(relationship_delta.get("repair_attempt_quality", 0)),
        _score_100(relationship_delta.get("validation_skill", 0)) // 2,
    )


def _blame_shift(event: Mapping[str, Any], relationship_delta: Mapping[str, Any]) -> bool:
    context = " ".join(
        [
            str(event.get("context", "")),
            str(event.get("repair_style", "")),
            str(event.get("short_description", "")),
            str(event.get("title", "")),
        ]
    ).lower()
    if any(token in context for token in ("blame_shift", "push blame", "defensive", "推卸", "甩锅")):
        return True
    return _score_100(event.get("defensive_response", relationship_delta.get("defensive_response", 0))) >= 60


def _normalize_personality(personality: Mapping[str, Any] | Any | None) -> dict[str, int]:
    data = _mapping(personality)
    result = {field: DEFAULT_PERSONALITY_VALUE for field in PERSONALITY_FIELDS}
    aliases = {
        "jealousy": ("jealousy", "jealousy_tendency"),
        "conflict_avoidance": ("conflict_avoidance", "avoidance_tendency"),
        "communication_drive": ("communication_drive", "communication_initiative"),
        "honesty_expectation": ("honesty_expectation", "honesty_tendency"),
        "attachment_anxiety": ("attachment_anxiety", "security_need"),
    }

    for field in PERSONALITY_FIELDS:
        keys = aliases.get(field, (field,))
        for key in keys:
            if key in data:
                result[field] = _score_100(
                    data.get(key),
                    default=DEFAULT_PERSONALITY_VALUE,
                    scale_small=False,
                )
                break
            if hasattr(personality, key):
                result[field] = _score_100(
                    getattr(personality, key),
                    default=DEFAULT_PERSONALITY_VALUE,
                    scale_small=False,
                )
                break
    return result


def _normalize_relationship_state(state: Mapping[str, Any] | Any | None) -> dict[str, int]:
    data = _mapping(state)
    aliases = {
        "trust": ("trust", "fact_trust", "trust_level"),
        "safety": ("safety", "security", "relationship_safety"),
        "satisfaction": ("satisfaction", "relationship_satisfaction"),
        "conflict_risk": ("conflict_risk", "conflict"),
        "deception_risk": ("deception_risk", "lie_risk"),
        "repair_chance": ("repair_chance", "repair"),
        "hidden_tension": ("hidden_tension", "pressure"),
        "suspicion": ("suspicion", "flaw"),
        "unresolved_conflicts": ("unresolved_conflicts", "unresolved_conflict_count"),
    }
    result: dict[str, int] = {}
    for field, default in DEFAULT_STATE.items():
        value = default
        for key in aliases[field]:
            if key in data:
                value = data.get(key, default)
                break
            if hasattr(state, key):
                value = getattr(state, key)
                break
        result[field] = _score_100(value, default=default, scale_small=False)
    return result


def _memory_profile(
    memories: Iterable[Any] | Mapping[str, Any] | Any | None,
    event: Mapping[str, Any],
) -> dict[str, int]:
    tags = set(_as_list(event.get("memory_tags")))
    candidate = _mapping(event.get("memory_candidate"))
    tags.update(_memory_tags_from_mapping(candidate))

    if memories is not None:
        items: Iterable[Any]
        if isinstance(memories, Mapping) or isinstance(memories, str):
            items = [memories]
        else:
            try:
                items = list(memories)
            except TypeError:
                items = [memories]
        for item in items:
            tags.update(_memory_tags(item))

    repeated_deception = _tag_weight(tags, {"repeated_deception"})
    unresolved_betrayal = _tag_weight(tags, {"unresolved_betrayal"})
    boundary_violation = _tag_weight(tags, {"boundary_violation"})
    emotional_neglect = _tag_weight(tags, {"emotional_neglect"})
    reliable_support = _tag_weight(tags, {"reliable_support"})
    repaired_after_conflict = _tag_weight(tags, {"repaired_after_conflict"})

    old_wound_load = _clamp_int(
        repeated_deception * 0.9
        + unresolved_betrayal
        + boundary_violation * 0.6
        + emotional_neglect * 0.5
        - reliable_support * 0.25
        - repaired_after_conflict * 0.2
    )

    return {
        "old_wound_load": old_wound_load,
        "repeated_deception": repeated_deception,
        "unresolved_betrayal": unresolved_betrayal,
        "boundary_violation": boundary_violation,
        "emotional_neglect": emotional_neglect,
        "reliable_support": reliable_support,
        "repaired_after_conflict": repaired_after_conflict,
    }


def _memory_tags(item: Any) -> set[str]:
    if isinstance(item, str):
        return {item}
    data = _mapping(item)
    tags = set(_as_list(data.get("tags")))
    tags.update(_as_list(data.get("memory_tags")))
    tags.update(_as_list(data.get("trigger_keywords")))
    tags.update(_memory_tags_from_mapping(data))
    return tags


def _memory_tags_from_mapping(data: Mapping[str, Any]) -> set[str]:
    tags: set[str] = set()
    memory_type = str(data.get("memory_type", "")).strip()
    wound_type = str(data.get("wound_type", "")).strip()
    pattern_key = str(data.get("pattern_key", "")).strip()
    note = str(data.get("note", data.get("player_facing_note", ""))).lower()

    text = " ".join([memory_type, wound_type, pattern_key, note])
    if "betrayal" in text or "hidden_contact" in text:
        tags.add("unresolved_betrayal")
    if "deception" in text or "conceal" in text or "half_truth" in text:
        tags.add("repeated_deception")
    if "privacy" in text or "boundary" in text:
        tags.add("boundary_violation")
    if "neglect" in text:
        tags.add("emotional_neglect")
    if "repair" in text:
        tags.add("repaired_after_conflict")
    if "support" in text or "reliable" in text:
        tags.add("reliable_support")
    return tags


def _tag_weight(tags: set[str], target_tags: set[str]) -> int:
    return 35 if tags & target_tags else 0


def _score_100(value: Any, default: int = 0, scale_small: bool = True) -> int:
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in LEVEL_SCORES:
            return LEVEL_SCORES[normalized]
        try:
            number = float(normalized)
        except ValueError:
            return default
    else:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return default

    if scale_small and -10 <= number <= 10:
        number *= 10
    return _clamp_int(number)


def _mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    if hasattr(value, "to_dict"):
        mapped = value.to_dict()
        return mapped if isinstance(mapped, Mapping) else {}
    if hasattr(value, "__dict__"):
        return vars(value)
    return {}


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, Iterable):
        return [str(item) for item in value]
    return [str(value)]


def _clamp_int(value: int | float, low: int = 0, high: int = 100) -> int:
    return int(max(low, min(high, round(value))))


def _add(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def _unique(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result

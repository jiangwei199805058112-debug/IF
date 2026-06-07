from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Iterable, Mapping

from .npc_reaction_decision import (
    DEFAULT_PERSONALITY_VALUE,
    DEFAULT_STATE,
    PERSONALITY_FIELDS,
    NPCReactionDecision,
    decide_npc_reaction,
)


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
}

STATE_ALIASES = {
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


@dataclass(frozen=True)
class PlaytestObservation:
    observation_id: str
    event_id: str = ""
    event_type: str = ""
    event_title: str = ""
    event_visibility: str = "public"
    event_discovered: bool = True
    npc_personality_snapshot: dict[str, int] = field(default_factory=dict)
    relationship_state_before: dict[str, int] = field(default_factory=dict)
    memory_snapshot: list[dict[str, Any]] = field(default_factory=list)
    npc_reaction_type: str = ""
    npc_reaction_intensity: int = 0
    npc_public_conflict: bool = False
    npc_followup_risk: int = 0
    npc_reaction_explanation: str = ""
    relationship_delta: dict[str, int] = field(default_factory=dict)
    memory_candidate: dict[str, Any] = field(default_factory=dict)
    interpretation_summary: str = ""
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_playtest_observation(
    event: Mapping[str, Any] | Any,
    personality: Mapping[str, Any] | Any | None = None,
    relationship_state: Mapping[str, Any] | Any | None = None,
    memories: Iterable[Any] | Mapping[str, Any] | Any | None = None,
) -> PlaytestObservation:
    """Build one structured observation for a player event and NPC reaction.

    This is a passive playtest log builder. It calls the NPC reaction decision
    module, snapshots inputs, and returns a single record without mutating game
    state or the long-term memory store.
    """

    event_data = _mapping(event)
    reaction = decide_npc_reaction(event_data, personality, relationship_state, memories)
    event_id = str(event_data.get("event_id", "unknown_event"))
    event_type = str(event_data.get("event_type", "relationship_event"))
    visibility = str(event_data.get("visibility", "public") or "public")
    discovered = _event_discovered(event_data, visibility)
    personality_snapshot = _personality_snapshot(personality)
    state_snapshot = _relationship_state_snapshot(relationship_state)
    memory_snapshot = _memory_snapshot(memories)

    tags = _unique(
        [
            *reaction.tags,
            f"event_type:{event_type}",
            f"visibility:{visibility}",
            "hidden_undiscovered" if visibility in {"hidden", "private"} and not discovered else "",
        ]
    )

    return PlaytestObservation(
        observation_id=_observation_id(event_id, personality_snapshot, state_snapshot, memory_snapshot),
        event_id=event_id,
        event_type=event_type,
        event_title=_event_title(event_data),
        event_visibility=visibility,
        event_discovered=discovered,
        npc_personality_snapshot=personality_snapshot,
        relationship_state_before=state_snapshot,
        memory_snapshot=memory_snapshot,
        npc_reaction_type=reaction.reaction_type,
        npc_reaction_intensity=reaction.intensity,
        npc_public_conflict=reaction.public_conflict,
        npc_followup_risk=reaction.followup_risk,
        npc_reaction_explanation=reaction.explanation,
        relationship_delta=dict(reaction.relationship_delta),
        memory_candidate=dict(reaction.memory_candidate),
        interpretation_summary=_interpretation_summary(event_data, reaction),
        tags=tags,
    )


def format_playtest_observation(observation: PlaytestObservation | Mapping[str, Any]) -> str:
    """Format an observation into a compact human-readable playtest note."""

    data = observation.to_dict() if isinstance(observation, PlaytestObservation) else dict(_mapping(observation))
    event_title = str(data.get("event_title", "")) or str(data.get("event_id", "unknown_event"))
    personality = _mapping(data.get("npc_personality_snapshot"))
    state = _mapping(data.get("relationship_state_before"))
    memory = data.get("memory_snapshot", [])
    memory_items = memory if isinstance(memory, list) else []
    relationship_delta = _mapping(data.get("relationship_delta"))

    lines = [
        f"event: {event_title} ({data.get('event_id', '')})",
        f"event_type: {data.get('event_type', '')}",
        f"visibility: {data.get('event_visibility', 'public')} discovered={bool(data.get('event_discovered', True))}",
        f"personality: {_personality_summary(personality)}",
        f"relationship_before: trust={state.get('trust', 50)}, safety={state.get('safety', 50)}, satisfaction={state.get('satisfaction', 50)}, suspicion={state.get('suspicion', 0)}",
        f"memory: {_memory_summary(memory_items)}",
        f"reaction: {data.get('npc_reaction_type', '')} intensity={data.get('npc_reaction_intensity', 0)} followup_risk={data.get('npc_followup_risk', 0)}",
        f"public_conflict: {str(bool(data.get('npc_public_conflict', False))).lower()}",
        f"reason: {data.get('npc_reaction_explanation', '')}",
        f"relationship_delta: {_delta_summary(relationship_delta)}",
        f"memory_candidate: {_memory_candidate_summary(_mapping(data.get('memory_candidate')))}",
        f"interpretation: {data.get('interpretation_summary', '')}",
    ]
    tags = data.get("tags", [])
    if tags:
        lines.append("tags: " + ", ".join(str(tag) for tag in tags))
    return "\n".join(lines)


def _event_discovered(event: Mapping[str, Any], visibility: str) -> bool:
    if "discovered" in event:
        return bool(event.get("discovered"))
    if visibility == "discovered":
        return True
    if visibility in {"hidden", "private"}:
        return False
    return True


def _event_title(event: Mapping[str, Any]) -> str:
    return str(
        event.get("title")
        or event.get("event_title")
        or event.get("short_description")
        or event.get("event_id", "")
    )


def _personality_snapshot(personality: Mapping[str, Any] | Any | None) -> dict[str, int]:
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
        for key in aliases.get(field, (field,)):
            if key in data:
                result[field] = _score_100(data.get(key), default=DEFAULT_PERSONALITY_VALUE)
                break
            if hasattr(personality, key):
                result[field] = _score_100(getattr(personality, key), default=DEFAULT_PERSONALITY_VALUE)
                break
    return result


def _relationship_state_snapshot(state: Mapping[str, Any] | Any | None) -> dict[str, int]:
    data = _mapping(state)
    result: dict[str, int] = {}
    for field, default in DEFAULT_STATE.items():
        value = default
        for key in STATE_ALIASES[field]:
            if key in data:
                value = data.get(key, default)
                break
            if hasattr(state, key):
                value = getattr(state, key)
                break
        result[field] = _score_100(value, default=default)
    return result


def _memory_snapshot(memories: Iterable[Any] | Mapping[str, Any] | Any | None) -> list[dict[str, Any]]:
    if memories is None:
        return []
    if isinstance(memories, Mapping) or isinstance(memories, str):
        items = [memories]
    else:
        try:
            items = list(memories)
        except TypeError:
            items = [memories]

    result: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        if isinstance(item, str):
            result.append({"memory_id": f"memory:{index}", "tags": [item], "summary": item})
            continue
        data = _mapping(item)
        result.append(
            {
                "memory_id": str(data.get("memory_id", f"memory:{index}")),
                "memory_type": str(data.get("memory_type", "")),
                "wound_type": str(data.get("wound_type", "")),
                "pattern_key": str(data.get("pattern_key", "")),
                "intensity": _score_100(data.get("intensity", 0)),
                "tags": _as_list(data.get("tags")) + _as_list(data.get("memory_tags")),
                "summary": str(
                    data.get("player_facing_note")
                    or data.get("note")
                    or data.get("debug_note")
                    or data.get("pattern_key", "")
                ),
            }
        )
    return result


def _interpretation_summary(event: Mapping[str, Any], reaction: NPCReactionDecision) -> str:
    if reaction.public_conflict:
        conflict_text = "public conflict is allowed because the event is visible or discovered"
    elif str(event.get("visibility", "public")) in {"hidden", "private"} and not _event_discovered(
        event, str(event.get("visibility", "public"))
    ):
        conflict_text = "hidden or private event remains internal; no public argument is logged"
    else:
        conflict_text = "no public conflict is needed for this reaction"

    return (
        f"{reaction.reaction_type} selected with intensity {reaction.intensity}; "
        f"{conflict_text}; followup risk {reaction.followup_risk}."
    )


def _personality_summary(personality: Mapping[str, Any]) -> str:
    highlights: list[str] = []
    for key in (
        "communication_drive",
        "forgiveness",
        "jealousy",
        "attachment_anxiety",
        "conflict_avoidance",
        "revenge_tendency",
        "self_respect",
    ):
        value = _score_100(personality.get(key, DEFAULT_PERSONALITY_VALUE), default=DEFAULT_PERSONALITY_VALUE)
        if value >= 75:
            highlights.append(f"high_{key}={value}")
        elif value <= 25:
            highlights.append(f"low_{key}={value}")
    if not highlights:
        highlights.append("balanced_profile")
    return ", ".join(highlights)


def _memory_summary(memories: list[dict[str, Any]]) -> str:
    if not memories:
        return "none"
    summaries: list[str] = []
    for memory in memories[:3]:
        label = memory.get("summary") or memory.get("pattern_key") or memory.get("memory_type") or memory.get("memory_id")
        summaries.append(str(label))
    if len(memories) > 3:
        summaries.append(f"+{len(memories) - 3} more")
    return "; ".join(summaries)


def _delta_summary(delta: Mapping[str, Any]) -> str:
    if not delta:
        return "none"
    parts = [f"{key}={value}" for key, value in delta.items() if value not in {0, None, ""}]
    return ", ".join(parts) if parts else "no immediate visible delta"


def _memory_candidate_summary(candidate: Mapping[str, Any]) -> str:
    if not candidate:
        return "none"
    tags = ", ".join(_as_list(candidate.get("tags")))
    memory_type = str(candidate.get("memory_type", ""))
    weight = candidate.get("weight", "")
    return f"type={memory_type}, weight={weight}, tags={tags}"


def _observation_id(
    event_id: str,
    personality: Mapping[str, int],
    state: Mapping[str, int],
    memories: list[dict[str, Any]],
) -> str:
    key_parts = [
        event_id or "unknown_event",
        f"comm{personality.get('communication_drive', 50)}",
        f"jeal{personality.get('jealousy', 50)}",
        f"trust{state.get('trust', 50)}",
        f"mem{len(memories)}",
    ]
    return "obs:" + ":".join(str(part) for part in key_parts)


def _score_100(value: Any, default: int = 0) -> int:
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
    return int(max(0, min(100, round(number))))


def _mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    if hasattr(value, "to_dict"):
        data = value.to_dict()
        return data if isinstance(data, Mapping) else {}
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


def _unique(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result

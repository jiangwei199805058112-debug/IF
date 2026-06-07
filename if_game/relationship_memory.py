from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from typing import Any, Iterable, Mapping


LEVEL_SCORES = {
    "none": 0,
    "low": 2,
    "weak": 2,
    "minor": 2,
    "medium": 5,
    "moderate": 5,
    "acknowledged": 5,
    "high": 8,
    "strong": 8,
    "behavioral": 8,
    "critical": 10,
    "conclusive": 10,
    "sustained": 10,
}

REPAIRED_STATUSES = {"partially_repaired", "repaired"}
UNREPAIRED_STATUSES = {"", "unrepaired", "acknowledged", "reopened", "repeated_after_repair"}


@dataclass(frozen=True)
class RelationshipMemory:
    memory_id: str
    source_event_id: str
    source_id: str
    target_id: str
    memory_type: str
    wound_type: str | None
    pattern_key: str | None
    severity: str
    intensity: int
    trigger_keywords: list[str] = field(default_factory=list)
    created_day: int = 0
    last_triggered_day: int = 0
    occurrence_count: int = 1
    decay_policy: str = "normal_decay"
    repair_status: str = "unrepaired"
    visibility: str = "player_visible"
    player_facing_note: str = ""
    debug_note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def update_relationship_memories(
    memories: Iterable[RelationshipMemory | Mapping[str, Any]],
    event: Mapping[str, Any],
    delta: Any,
    day: int,
) -> list[RelationshipMemory]:
    """Update long-term relationship memories from one aggregated event.

    The relationship state aggregator owns immediate deltas. This module only
    decides whether those deltas should become structured long-term memories.
    """

    event_data = _mapping(event)
    delta_data = _delta_mapping(delta)
    normalized = [_memory_from_any(memory) for memory in memories]

    tags = set(_as_list(delta_data.get("report_tags"))) | set(_as_list(event_data.get("report_tags")))
    pattern_key = _clean_optional(event_data.get("pattern_key") or delta_data.get("pattern_key"))
    occurrence_count = _occurrence_count(event_data, pattern_key, normalized)
    repair_signal = _has_repair_signal(event_data, delta_data, tags)

    if _should_write_old_wound(event_data, delta_data, tags):
        normalized = _upsert_old_wound_memory(
            normalized,
            event_data,
            delta_data,
            tags,
            pattern_key,
            occurrence_count,
            day,
        )

    if pattern_key and occurrence_count >= 3:
        normalized = _upsert_pattern_memory(
            normalized,
            event_data,
            delta_data,
            pattern_key,
            occurrence_count,
            day,
        )

    if repair_signal:
        normalized = _apply_repair_to_old_wounds(normalized, event_data, pattern_key, day)
        normalized = _upsert_repair_memory(
            normalized,
            event_data,
            delta_data,
            pattern_key,
            occurrence_count,
            day,
        )

    return normalized


def update_memories_from_aggregated_event(
    memories: Iterable[RelationshipMemory | Mapping[str, Any]],
    event: Mapping[str, Any],
    delta: Any,
    day: int,
) -> list[RelationshipMemory]:
    """Compatibility alias for callers that name the aggregator bridge directly."""

    return update_relationship_memories(memories, event, delta, day)


def decay_relationship_memories(
    memories: Iterable[RelationshipMemory | Mapping[str, Any]],
    current_day: int,
) -> list[RelationshipMemory]:
    """Apply lightweight day-based decay without deleting memories."""

    decayed: list[RelationshipMemory] = []
    for memory in (_memory_from_any(item) for item in memories):
        periods = max(0, (current_day - memory.last_triggered_day) // 7)
        if periods <= 0:
            decayed.append(memory)
            continue

        decrement = _decay_amount(memory, periods)
        intensity = _clamp_intensity(memory.intensity - decrement)
        decayed.append(replace(memory, intensity=intensity, severity=_severity(intensity)))
    return decayed


def format_memory_summary(
    memories: Iterable[RelationshipMemory | Mapping[str, Any]],
    player_visible_only: bool = True,
) -> list[str]:
    """Format memory summaries without exposing hidden truth/debug fields."""

    lines: list[str] = []
    for memory in (_memory_from_any(item) for item in memories):
        if player_visible_only and memory.visibility != "player_visible":
            continue

        if memory.player_facing_note:
            note = memory.player_facing_note
        elif memory.memory_type == "old_wound_memory":
            note = "这段经历仍可能影响之后的信任和安全感。"
        elif memory.memory_type == "pattern_memory":
            note = "类似问题已经反复出现，之后更容易被联想到同一模式。"
        elif memory.memory_type == "repair_memory":
            note = "一次具体修复会让后续沟通更有回旋余地。"
        else:
            note = "这段互动被保留为关系里的背景记忆。"

        if memory.memory_type == "pattern_memory" and memory.occurrence_count >= 3:
            note = f"{note} 已出现 {memory.occurrence_count} 次。"
        lines.append(note)

    return _unique(lines)


def _upsert_old_wound_memory(
    memories: list[RelationshipMemory],
    event: Mapping[str, Any],
    delta: Mapping[str, Any],
    tags: set[str],
    pattern_key: str | None,
    occurrence_count: int,
    day: int,
) -> list[RelationshipMemory]:
    source_id = _source_id(event, delta)
    target_id = _target_id(event, delta)
    event_id = _event_id(event)
    wound_type = _infer_wound_type(event, tags)
    memory_id = _memory_id("old_wound_memory", source_id, target_id, pattern_key or wound_type or event_id)
    intensity = _old_wound_intensity(event, delta, tags)
    decay_policy = _old_wound_decay_policy(wound_type, intensity)

    index = _find_memory_index(memories, memory_id, "old_wound_memory", source_id, target_id, pattern_key)
    if index is None:
        memories.append(
            RelationshipMemory(
                memory_id=memory_id,
                source_event_id=event_id,
                source_id=source_id,
                target_id=target_id,
                memory_type="old_wound_memory",
                wound_type=wound_type,
                pattern_key=pattern_key,
                severity=_severity(intensity),
                intensity=intensity,
                trigger_keywords=_trigger_keywords(event, wound_type, pattern_key),
                created_day=day,
                last_triggered_day=day,
                occurrence_count=max(1, occurrence_count),
                decay_policy=decay_policy,
                repair_status=_repair_status(event) or "unrepaired",
                visibility="player_visible",
                player_facing_note="这次事件可能会成为之后关系里的旧账。",
                debug_note=_debug_note(event, delta, tags),
            )
        )
        return memories

    existing = memories[index]
    added = max(8, intensity // 4)
    next_status = "reopened" if existing.repair_status in REPAIRED_STATUSES else existing.repair_status
    if _repair_status(event):
        next_status = _repair_status(event)

    new_intensity = _clamp_intensity(max(existing.intensity, intensity) + added)
    memories[index] = replace(
        existing,
        source_event_id=event_id,
        wound_type=existing.wound_type or wound_type,
        severity=_severity(new_intensity),
        intensity=new_intensity,
        trigger_keywords=_unique(existing.trigger_keywords + _trigger_keywords(event, wound_type, pattern_key)),
        last_triggered_day=day,
        occurrence_count=max(existing.occurrence_count + 1, occurrence_count),
        decay_policy=existing.decay_policy if existing.decay_policy else decay_policy,
        repair_status=next_status or "unrepaired",
        player_facing_note="类似的伤害再次出现，旧账被重新触发。",
        debug_note=_debug_note(event, delta, tags),
    )
    return memories


def _upsert_pattern_memory(
    memories: list[RelationshipMemory],
    event: Mapping[str, Any],
    delta: Mapping[str, Any],
    pattern_key: str,
    occurrence_count: int,
    day: int,
) -> list[RelationshipMemory]:
    source_id = _source_id(event, delta)
    target_id = _target_id(event, delta)
    event_id = _event_id(event)
    memory_id = _memory_id("pattern_memory", source_id, target_id, pattern_key)
    base_intensity = _clamp_intensity(20 + occurrence_count * 6)

    index = _find_memory_index(memories, memory_id, "pattern_memory", source_id, target_id, pattern_key)
    if index is None:
        memories.append(
            RelationshipMemory(
                memory_id=memory_id,
                source_event_id=event_id,
                source_id=source_id,
                target_id=target_id,
                memory_type="pattern_memory",
                wound_type=None,
                pattern_key=pattern_key,
                severity=_severity(base_intensity),
                intensity=base_intensity,
                trigger_keywords=_trigger_keywords(event, None, pattern_key),
                created_day=day,
                last_triggered_day=day,
                occurrence_count=occurrence_count,
                decay_policy="pattern_reinforced",
                repair_status=_repair_status(event) or "unrepaired",
                visibility="player_visible",
                player_facing_note="类似问题已经反复出现，之后更容易被联想到同一模式。",
                debug_note=_debug_note(event, delta, {"pattern_memory_risk"}),
            )
        )
        return memories

    existing = memories[index]
    new_count = max(existing.occurrence_count + 1, occurrence_count)
    new_intensity = _clamp_intensity(max(existing.intensity, base_intensity) + 6)
    memories[index] = replace(
        existing,
        source_event_id=event_id,
        severity=_severity(new_intensity),
        intensity=new_intensity,
        trigger_keywords=_unique(existing.trigger_keywords + _trigger_keywords(event, None, pattern_key)),
        last_triggered_day=day,
        occurrence_count=new_count,
        repair_status=_repair_status(event) or existing.repair_status,
        player_facing_note="同类问题继续出现，关系会更容易把它看成一种模式。",
        debug_note=_debug_note(event, delta, {"pattern_memory_risk"}),
    )
    return memories


def _upsert_repair_memory(
    memories: list[RelationshipMemory],
    event: Mapping[str, Any],
    delta: Mapping[str, Any],
    pattern_key: str | None,
    occurrence_count: int,
    day: int,
) -> list[RelationshipMemory]:
    source_id = _source_id(event, delta)
    target_id = _target_id(event, delta)
    event_id = _event_id(event)
    repair_quality = _score(event.get("repair_attempt_quality", 0))
    repair_status = _repair_status(event)
    if repair_status not in REPAIRED_STATUSES:
        repair_status = "partially_repaired"

    memory_id = _memory_id("repair_memory", source_id, target_id, pattern_key or event_id)
    intensity = _clamp_intensity(max(20, repair_quality * 8, _score(delta.get("repair_chance_delta", 0)) * 8))
    index = _find_memory_index(memories, memory_id, "repair_memory", source_id, target_id, pattern_key)

    if index is None:
        memories.append(
            RelationshipMemory(
                memory_id=memory_id,
                source_event_id=event_id,
                source_id=source_id,
                target_id=target_id,
                memory_type="repair_memory",
                wound_type=None,
                pattern_key=pattern_key,
                severity=_severity(intensity),
                intensity=intensity,
                trigger_keywords=_trigger_keywords(event, None, pattern_key) or ["repair"],
                created_day=day,
                last_triggered_day=day,
                occurrence_count=max(1, occurrence_count),
                decay_policy="fast_decay_if_repaired",
                repair_status=repair_status,
                visibility="player_visible",
                player_facing_note="这次具体修复会让后续沟通更有回旋余地。",
                debug_note=_debug_note(event, delta, {"repair_capable"}),
            )
        )
        return memories

    existing = memories[index]
    new_intensity = _clamp_intensity(max(existing.intensity, intensity) + 4)
    memories[index] = replace(
        existing,
        source_event_id=event_id,
        severity=_severity(new_intensity),
        intensity=new_intensity,
        trigger_keywords=_unique(existing.trigger_keywords + _trigger_keywords(event, None, pattern_key)),
        last_triggered_day=day,
        occurrence_count=max(existing.occurrence_count + 1, occurrence_count),
        repair_status="repaired" if repair_status == "repaired" else existing.repair_status,
        player_facing_note="具体修复再次出现，关系里的修复经验更稳定。",
        debug_note=_debug_note(event, delta, {"repair_capable"}),
    )
    return memories


def _apply_repair_to_old_wounds(
    memories: list[RelationshipMemory],
    event: Mapping[str, Any],
    pattern_key: str | None,
    day: int,
) -> list[RelationshipMemory]:
    repair_status = _repair_status(event)
    if repair_status == "repaired":
        amount = 15
        next_status = "repaired"
    else:
        amount = 8
        next_status = "partially_repaired"

    updated: list[RelationshipMemory] = []
    source_id = str(event.get("source_id", event.get("actor_id", "")))
    target_id = str(event.get("target_id", ""))

    for memory in memories:
        if memory.memory_type != "old_wound_memory":
            updated.append(memory)
            continue
        if source_id and memory.source_id != source_id:
            updated.append(memory)
            continue
        if target_id and memory.target_id != target_id:
            updated.append(memory)
            continue
        if pattern_key and memory.pattern_key and memory.pattern_key != pattern_key:
            updated.append(memory)
            continue

        intensity = _clamp_intensity(memory.intensity - amount)
        decay_policy = "fast_decay_if_repaired" if next_status == "repaired" else memory.decay_policy
        updated.append(
            replace(
                memory,
                severity=_severity(intensity),
                intensity=intensity,
                last_triggered_day=day,
                repair_status=next_status,
                decay_policy=decay_policy,
                player_facing_note="这段旧账被认真处理了一部分，但不会被立刻抹掉。",
            )
        )
    return updated


def _should_write_old_wound(
    event: Mapping[str, Any],
    delta: Mapping[str, Any],
    tags: set[str],
) -> bool:
    if _int(delta.get("old_wound_memory_delta", 0)) > 0:
        return True
    if "old_wound_written" in tags:
        return True
    if str(event.get("repair_status", "")) == "repeated_after_repair":
        return True
    return False


def _has_repair_signal(
    event: Mapping[str, Any],
    delta: Mapping[str, Any],
    tags: set[str],
) -> bool:
    if "repair_capable" in tags or "repair_window_open" in tags:
        return True
    if _score(event.get("repair_attempt_quality", 0)) >= 7:
        return True
    if _int(delta.get("repair_chance_delta", 0)) >= 6:
        return True
    return _repair_status(event) in REPAIRED_STATUSES


def _old_wound_intensity(event: Mapping[str, Any], delta: Mapping[str, Any], tags: set[str]) -> int:
    old_wound_delta = max(0, _int(delta.get("old_wound_memory_delta", 0)))
    truth_harm = _score(event.get("truth_harm_level", 0))
    deception = _score(event.get("deception_level", 0))
    contempt = max(_score(event.get("contempt_signal", 0)), 8 if "contempt_risk" in tags else 0)
    stonewalling = _score(event.get("stonewalling_level", 0))

    intensity = max(
        old_wound_delta * 8,
        truth_harm * 5 + deception * 4,
        contempt * 8,
        stonewalling * 6,
        24 if "old_wound_written" in tags else 0,
    )
    return _clamp_intensity(intensity)


def _infer_wound_type(event: Mapping[str, Any], tags: set[str]) -> str:
    truth_type = str(event.get("truth_type", "")).strip()
    conflict_type = str(event.get("conflict_response_type", "")).strip()
    communication_type = str(event.get("communication_response_type", "")).strip()
    pattern_key = str(event.get("pattern_key", "")).strip()

    if "contempt_risk" in tags or conflict_type in {"contempt", "personality_attack", "exit_threat"}:
        return "contempt_attack"
    if communication_type in {"mocking_response", "judgmental_response"}:
        return "vulnerability_mocked"
    if "stonewalling_pattern" in tags or "stonewalling" in pattern_key:
        return "stonewalling_repeated"
    if truth_type in {"betrayal", "concealment"} or "deception_risk" in tags:
        return "betrayal_discovered"
    if "privacy_boundary_conflict" in tags or truth_type == "privacy_boundary":
        return "privacy_violation"
    if "taken_for_granted_sensitive" in tags or "underbenefit" in pattern_key:
        return "taken_for_granted_repeated"
    return "relationship_wound"


def _old_wound_decay_policy(wound_type: str | None, intensity: int) -> str:
    if wound_type in {"betrayal_discovered", "vulnerability_mocked", "contempt_attack", "stonewalling_repeated"}:
        return "no_decay_until_repair"
    if intensity >= 60:
        return "slow_decay"
    return "normal_decay"


def _decay_amount(memory: RelationshipMemory, periods: int) -> int:
    if memory.decay_policy == "normal_decay":
        return periods * 5
    if memory.decay_policy == "slow_decay":
        return periods * 2
    if memory.decay_policy == "fast_decay_if_repaired":
        return periods * 10 if memory.repair_status == "repaired" else periods * 2
    if memory.decay_policy == "no_decay_until_repair":
        if memory.repair_status == "repaired":
            return periods * 10
        if memory.repair_status == "partially_repaired":
            return periods * 5
        return 0
    if memory.decay_policy == "pattern_reinforced":
        return 0
    return 0


def _occurrence_count(
    event: Mapping[str, Any],
    pattern_key: str | None,
    memories: list[RelationshipMemory],
) -> int:
    direct = _int(event.get("occurrence_count", event.get("recent_frequency", 0)))
    if direct > 0:
        return direct
    if pattern_key:
        for memory in memories:
            if memory.pattern_key == pattern_key:
                return memory.occurrence_count + 1
    return 1


def _trigger_keywords(event: Mapping[str, Any], wound_type: str | None, pattern_key: str | None) -> list[str]:
    keywords = _as_list(event.get("trigger_keywords"))
    if pattern_key:
        keywords.append(pattern_key)
    if wound_type:
        keywords.extend(
            {
                "betrayal_discovered": ["trust", "hidden_contact"],
                "privacy_violation": ["privacy", "boundary"],
                "vulnerability_mocked": ["vulnerability", "mockery"],
                "contempt_attack": ["contempt", "mockery"],
                "stonewalling_repeated": ["silence", "conflict"],
                "taken_for_granted_repeated": ["fairness", "underbenefit"],
            }.get(wound_type, ["relationship_wound"])
        )
    return _unique([str(item) for item in keywords if str(item).strip()])


def _memory_from_any(memory: RelationshipMemory | Mapping[str, Any]) -> RelationshipMemory:
    if isinstance(memory, RelationshipMemory):
        return memory
    data = _mapping(memory)
    return RelationshipMemory(
        memory_id=str(data.get("memory_id", "")),
        source_event_id=str(data.get("source_event_id", "")),
        source_id=str(data.get("source_id", "")),
        target_id=str(data.get("target_id", "")),
        memory_type=str(data.get("memory_type", "neutral_context_memory")),
        wound_type=_clean_optional(data.get("wound_type")),
        pattern_key=_clean_optional(data.get("pattern_key")),
        severity=str(data.get("severity", "low")),
        intensity=_clamp_intensity(_int(data.get("intensity", 0))),
        trigger_keywords=_as_list(data.get("trigger_keywords")),
        created_day=_int(data.get("created_day", 0)),
        last_triggered_day=_int(data.get("last_triggered_day", data.get("created_day", 0))),
        occurrence_count=max(1, _int(data.get("occurrence_count", 1))),
        decay_policy=str(data.get("decay_policy", "normal_decay")),
        repair_status=str(data.get("repair_status", "unrepaired")),
        visibility=str(data.get("visibility", "player_visible")),
        player_facing_note=str(data.get("player_facing_note", "")),
        debug_note=str(data.get("debug_note", "")),
    )


def _delta_mapping(delta: Any) -> Mapping[str, Any]:
    if isinstance(delta, Mapping):
        return delta
    if hasattr(delta, "to_dict"):
        return _mapping(delta.to_dict())
    return {
        "source_id": getattr(delta, "source_id", ""),
        "target_id": getattr(delta, "target_id", ""),
        "repair_chance_delta": getattr(delta, "repair_chance_delta", 0),
        "old_wound_memory_delta": getattr(delta, "old_wound_memory_delta", 0),
        "report_tags": getattr(delta, "report_tags", []),
        "memory_notes": getattr(delta, "memory_notes", []),
        "debug_reasons": getattr(delta, "debug_reasons", []),
    }


def _find_memory_index(
    memories: list[RelationshipMemory],
    memory_id: str,
    memory_type: str,
    source_id: str,
    target_id: str,
    pattern_key: str | None,
) -> int | None:
    for index, memory in enumerate(memories):
        if memory.memory_id == memory_id:
            return index
        if (
            memory.memory_type == memory_type
            and memory.source_id == source_id
            and memory.target_id == target_id
            and pattern_key
            and memory.pattern_key == pattern_key
        ):
            return index
    return None


def _memory_id(memory_type: str, source_id: str, target_id: str, key: str) -> str:
    clean_key = key or "general"
    return f"mem:{memory_type}:{source_id or 'unknown'}:{target_id or 'unknown'}:{clean_key}"


def _debug_note(event: Mapping[str, Any], delta: Mapping[str, Any], tags: set[str]) -> str:
    return (
        f"event_id={_event_id(event)}; "
        f"truth_type={event.get('truth_type', '')}; "
        f"deception_level={event.get('deception_level', '')}; "
        f"old_wound_delta={delta.get('old_wound_memory_delta', 0)}; "
        f"tags={','.join(sorted(tags))}"
    )


def _source_id(event: Mapping[str, Any], delta: Mapping[str, Any]) -> str:
    return str(event.get("source_id", event.get("actor_id", delta.get("source_id", ""))))


def _target_id(event: Mapping[str, Any], delta: Mapping[str, Any]) -> str:
    return str(event.get("target_id", delta.get("target_id", "")))


def _event_id(event: Mapping[str, Any]) -> str:
    return str(event.get("event_id", "unknown_event"))


def _repair_status(event: Mapping[str, Any]) -> str:
    return str(event.get("repair_status", "")).strip()


def _score(value: Any) -> int:
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in LEVEL_SCORES:
            return LEVEL_SCORES[normalized]
        try:
            return int(round(float(normalized)))
        except ValueError:
            return 0
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return 0


def _int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in LEVEL_SCORES:
            return LEVEL_SCORES[normalized]
        try:
            return int(round(float(normalized)))
        except ValueError:
            return default
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def _clamp_intensity(value: int | float) -> int:
    return int(max(0, min(100, round(value))))


def _severity(intensity: int) -> str:
    if intensity >= 80:
        return "critical"
    if intensity >= 55:
        return "high"
    if intensity >= 25:
        return "medium"
    return "low"


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, Iterable):
        return [str(item) for item in value]
    return [str(value)]


def _clean_optional(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _unique(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result

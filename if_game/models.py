from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def _get(data: dict[str, Any], key: str, default: Any) -> Any:
    value = data.get(key, default)
    return default if value is None else value


@dataclass
class PersonalityModel:
    security_need: str = "medium"
    emotional_stability: str = "medium"
    communication_initiative: str = "medium"
    trust_baseline: str = "medium"
    jealousy_tendency: str = "medium"
    avoidance_tendency: str = "medium"
    honesty_tendency: str = "medium"
    double_standard_tendency: str = "medium"
    test_tendency: str = "medium"
    social_openness: str = "medium"

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "PersonalityModel":
        data = data or {}
        return cls(
            security_need=_get(data, "security_need", "medium"),
            emotional_stability=_get(data, "emotional_stability", "medium"),
            communication_initiative=_get(data, "communication_initiative", "medium"),
            trust_baseline=_get(data, "trust_baseline", "medium"),
            jealousy_tendency=_get(data, "jealousy_tendency", "medium"),
            avoidance_tendency=_get(data, "avoidance_tendency", "medium"),
            honesty_tendency=_get(data, "honesty_tendency", "medium"),
            double_standard_tendency=_get(data, "double_standard_tendency", "medium"),
            test_tendency=_get(data, "test_tendency", "medium"),
            social_openness=_get(data, "social_openness", "medium"),
        )


@dataclass
class CharacterProfile:
    id: str
    display_name: str
    role: str
    age: int
    work_status: str
    personality: PersonalityModel

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CharacterProfile":
        return cls(
            id=str(_get(data, "id", "")),
            display_name=str(_get(data, "display_name", "")),
            role=str(_get(data, "role", "")),
            age=int(_get(data, "age", 18)),
            work_status=str(_get(data, "work_status", "")),
            personality=PersonalityModel.from_dict(data.get("personality")),
        )


@dataclass
class MemoryEntry:
    day: int
    event_id: str
    branch_id: str
    summary: str
    resolved: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MemoryEntry":
        return cls(
            day=int(_get(data, "day", 0)),
            event_id=str(_get(data, "event_id", "")),
            branch_id=str(_get(data, "branch_id", "")),
            summary=str(_get(data, "summary", "")),
            resolved=bool(_get(data, "resolved", False)),
        )


@dataclass
class OutcomeDelta:
    trust: str = "none"
    security: str = "none"
    pressure: str = "none"
    conflict: str = "none"
    disappointment: str = "none"
    flaw: str = "none"
    crisis: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "OutcomeDelta":
        data = data or {}
        return cls(
            trust=str(_get(data, "trust", "none")),
            security=str(_get(data, "security", "none")),
            pressure=str(_get(data, "pressure", "none")),
            conflict=str(_get(data, "conflict", "none")),
            disappointment=str(_get(data, "disappointment", "none")),
            flaw=str(_get(data, "flaw", "none")),
            crisis=bool(_get(data, "crisis", False)),
        )


@dataclass
class PerceivedRelationshipState:
    feedback_level: str = "stable"
    visible_summary: str = "关系还算稳定。"


@dataclass
class RelationshipReview:
    main_stage: str
    sub_tags: list[str] = field(default_factory=list)
    main_reasons: list[str] = field(default_factory=list)
    turning_points: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    repair_chances: list[str] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "main_stage": self.main_stage,
            "sub_tags": list(self.sub_tags),
            "main_reasons": list(self.main_reasons),
            "turning_points": list(self.turning_points),
            "risks": list(self.risks),
            "repair_chances": list(self.repair_chances),
            "summary": self.summary,
        }


@dataclass
class RelationshipState:
    day: int
    stage: str
    trust: int = 0
    security: int = 0
    pressure: int = 0
    conflict: int = 0
    disappointment: int = 0
    flaw: int = 0
    memory_entries: list[MemoryEntry] = field(default_factory=list)
    active_hooks: list[str] = field(default_factory=list)
    profile_pair_id: str = ""
    pair_title: str = ""
    player: CharacterProfile | None = None
    npc: CharacterProfile | None = None
    perceived: PerceivedRelationshipState = field(default_factory=PerceivedRelationshipState)
    triggered_events: list[str] = field(default_factory=list)
    transcript: list[str] = field(default_factory=list)
    atmosphere_tag: str = "stable"
    atmosphere_history: list[dict[str, Any]] = field(default_factory=list)
    daily_action_history: list[dict[str, Any]] = field(default_factory=list)
    event_resolution_log: list[dict[str, Any]] = field(default_factory=list)

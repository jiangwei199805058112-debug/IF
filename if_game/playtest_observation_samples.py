from __future__ import annotations

from collections import Counter
from copy import deepcopy
from dataclasses import dataclass, field, replace
from typing import Any, Iterable, Mapping

from .playtest_observation import PlaytestObservation, build_playtest_observation
from .relationship_event_samples import (
    accountability_repair_event,
    dinner_disclosure_event,
    forgotten_small_promise_event,
    phone_boundary_event,
    supportive_listening_event,
)


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


NPC_A_COMMUNICATOR = {
    "emotional_stability": 78,
    "jealousy": 22,
    "forgiveness": 86,
    "conflict_avoidance": 24,
    "communication_drive": 92,
    "revenge_tendency": 8,
    "attachment_anxiety": 28,
    "honesty_expectation": 70,
    "self_respect": 62,
}

NPC_B_JEALOUS = {
    "emotional_stability": 42,
    "jealousy": 92,
    "forgiveness": 48,
    "conflict_avoidance": 35,
    "communication_drive": 58,
    "revenge_tendency": 32,
    "attachment_anxiety": 88,
    "honesty_expectation": 82,
    "self_respect": 62,
}

NPC_C_AVOIDANT = {
    "emotional_stability": 54,
    "jealousy": 42,
    "forgiveness": 55,
    "conflict_avoidance": 92,
    "communication_drive": 18,
    "revenge_tendency": 18,
    "attachment_anxiety": 50,
    "honesty_expectation": 58,
    "self_respect": 58,
}

NPC_D_REVENGEFUL = {
    "emotional_stability": 25,
    "jealousy": 72,
    "forgiveness": 12,
    "conflict_avoidance": 24,
    "communication_drive": 36,
    "revenge_tendency": 94,
    "attachment_anxiety": 76,
    "honesty_expectation": 88,
    "self_respect": 48,
}

NPC_E_HIGH_SELF_RESPECT = {
    "emotional_stability": 70,
    "jealousy": 36,
    "forgiveness": 28,
    "conflict_avoidance": 28,
    "communication_drive": 55,
    "revenge_tendency": 18,
    "attachment_anxiety": 38,
    "honesty_expectation": 92,
    "self_respect": 95,
}


SAMPLE_PERSONALITIES = {
    "NPC_A_COMMUNICATOR": NPC_A_COMMUNICATOR,
    "NPC_B_JEALOUS": NPC_B_JEALOUS,
    "NPC_C_AVOIDANT": NPC_C_AVOIDANT,
    "NPC_D_REVENGEFUL": NPC_D_REVENGEFUL,
    "NPC_E_HIGH_SELF_RESPECT": NPC_E_HIGH_SELF_RESPECT,
}


@dataclass(frozen=True)
class ObservationSampleCase:
    case_id: str
    title: str
    event: Mapping[str, Any]
    relationship_state: Mapping[str, Any] = field(default_factory=dict)
    memories: tuple[Any, ...] = ()


def _deception_discovered_event() -> dict[str, Any]:
    event = deepcopy(dinner_disclosure_event("half_truth"))
    event.update(
        {
            "event_id": "CASE_DECEPTION_DISCOVERED",
            "event_type": "deception",
            "title": "Half-truth discovered",
            "visibility": "private",
            "discovered": True,
            "severity": 70,
            "context": "A half-truth about an opposite-gender dinner has been discovered.",
        }
    )
    return event


def _repeat_deception_event() -> dict[str, Any]:
    event = deepcopy(_deception_discovered_event())
    event.update(
        {
            "event_id": "CASE_REPEAT_DECEPTION",
            "title": "Repeated half-truth discovered",
            "context": "A similar half-truth appears after previous deception memories.",
            "memory_tags": ["repeated_deception", "unresolved_betrayal"],
        }
    )
    return event


def _privacy_hidden_event() -> dict[str, Any]:
    event = deepcopy(phone_boundary_event("hidden"))
    event.update(
        {
            "event_id": "CASE_PRIVACY_HIDDEN",
            "title": "Phone boundary hidden",
            "visibility": "hidden",
            "discovered": False,
            "severity": 45,
        }
    )
    return event


CASE_SUPPORT = ObservationSampleCase(
    case_id="CASE_SUPPORT",
    title="Supportive listening",
    event={
        **deepcopy(supportive_listening_event()),
        "event_id": "CASE_SUPPORT",
        "event_type": "positive_support",
        "title": "Supportive listening",
        "severity": 35,
    },
    relationship_state={
        "trust": 62,
        "safety": 58,
        "satisfaction": 60,
        "repair_chance": 62,
        "suspicion": 8,
    },
)

CASE_MINOR = ObservationSampleCase(
    case_id="CASE_MINOR",
    title="Forgotten small promise",
    event={
        **deepcopy(forgotten_small_promise_event()),
        "event_id": "CASE_MINOR",
        "event_type": "minor_disappointment",
        "title": "Forgotten small promise",
        "severity": 30,
    },
    relationship_state={
        "trust": 58,
        "safety": 58,
        "satisfaction": 55,
        "repair_chance": 55,
    },
)

CASE_PRIVACY_HIDDEN = ObservationSampleCase(
    case_id="CASE_PRIVACY_HIDDEN",
    title="Phone boundary hidden",
    event=_privacy_hidden_event(),
    relationship_state={
        "trust": 55,
        "safety": 52,
        "satisfaction": 54,
        "hidden_tension": 28,
        "suspicion": 36,
        "repair_chance": 50,
    },
)

CASE_DECEPTION_DISCOVERED = ObservationSampleCase(
    case_id="CASE_DECEPTION_DISCOVERED",
    title="Half-truth discovered",
    event=_deception_discovered_event(),
    relationship_state={
        "trust": 38,
        "safety": 25,
        "satisfaction": 45,
        "conflict_risk": 38,
        "deception_risk": 55,
        "repair_chance": 42,
        "suspicion": 52,
    },
)

CASE_REPAIR = ObservationSampleCase(
    case_id="CASE_REPAIR",
    title="Accountable repair",
    event={
        **deepcopy(accountability_repair_event("accountable")),
        "event_id": "CASE_REPAIR",
        "event_type": "repair_attempt",
        "title": "Accountable repair",
        "severity": 45,
    },
    relationship_state={
        "trust": 48,
        "safety": 48,
        "satisfaction": 44,
        "repair_chance": 58,
        "conflict_risk": 38,
    },
)

CASE_REPEAT_DECEPTION = ObservationSampleCase(
    case_id="CASE_REPEAT_DECEPTION",
    title="Repeated half-truth discovered",
    event=_repeat_deception_event(),
    relationship_state={
        "trust": 24,
        "safety": 24,
        "satisfaction": 18,
        "conflict_risk": 68,
        "deception_risk": 76,
        "repair_chance": 20,
        "hidden_tension": 55,
        "suspicion": 78,
        "unresolved_conflicts": 60,
    },
    memories=(
        "repeated_deception",
        "unresolved_betrayal",
        {
            "memory_id": "sample:repeated_deception",
            "memory_type": "old_wound_memory",
            "pattern_key": "half_truth_dinner_disclosure",
            "tags": ["repeated_deception", "unresolved_betrayal"],
            "intensity": 72,
            "player_facing_note": "Similar half-truths have already damaged trust.",
        },
    ),
)


SAMPLE_CASES = {
    "CASE_SUPPORT": CASE_SUPPORT,
    "CASE_MINOR": CASE_MINOR,
    "CASE_PRIVACY_HIDDEN": CASE_PRIVACY_HIDDEN,
    "CASE_DECEPTION_DISCOVERED": CASE_DECEPTION_DISCOVERED,
    "CASE_REPAIR": CASE_REPAIR,
    "CASE_REPEAT_DECEPTION": CASE_REPEAT_DECEPTION,
}


def generate_sample_observations(
    cases: Iterable[ObservationSampleCase] | None = None,
    personalities: Mapping[str, Mapping[str, Any]] | None = None,
) -> list[PlaytestObservation]:
    """Generate fixed side-channel observations for personality comparison."""

    selected_cases = list(cases) if cases is not None else list(SAMPLE_CASES.values())
    selected_personalities = personalities or SAMPLE_PERSONALITIES
    observations: list[PlaytestObservation] = []

    for sample_case in selected_cases:
        for npc_id, personality in selected_personalities.items():
            observation = build_playtest_observation(
                deepcopy(dict(sample_case.event)),
                dict(personality),
                dict(sample_case.relationship_state),
                deepcopy(list(sample_case.memories)),
            )
            observations.append(
                replace(
                    observation,
                    tags=_unique(
                        [
                            *observation.tags,
                            f"case:{sample_case.case_id}",
                            f"npc:{npc_id}",
                        ]
                    ),
                )
            )

    return observations


def reaction_type_distribution(
    observations: Iterable[PlaytestObservation] | None = None,
) -> dict[str, int]:
    selected = list(observations) if observations is not None else generate_sample_observations()
    return dict(Counter(observation.npc_reaction_type for observation in selected))


def summarize_sample_observations(
    observations: Iterable[PlaytestObservation] | None = None,
) -> str:
    selected = list(observations) if observations is not None else generate_sample_observations()
    distribution = reaction_type_distribution(selected)
    lines = ["reaction_type distribution:"]
    for reaction_type, count in sorted(distribution.items()):
        lines.append(f"{reaction_type}: {count}")

    lines.extend(["", "key observations:"])
    lines.extend(_key_observations(selected))
    return "\n".join(lines)


def observations_for(
    observations: Iterable[PlaytestObservation],
    case_id: str | None = None,
    npc_id: str | None = None,
) -> list[PlaytestObservation]:
    selected: list[PlaytestObservation] = []
    for observation in observations:
        tags = set(observation.tags)
        if case_id is not None and f"case:{case_id}" not in tags:
            continue
        if npc_id is not None and f"npc:{npc_id}" not in tags:
            continue
        selected.append(observation)
    return selected


def _key_observations(observations: list[PlaytestObservation]) -> list[str]:
    lines: list[str] = []

    support_reactions = {
        observation.npc_reaction_type
        for observation in observations_for(observations, case_id="CASE_SUPPORT")
    }
    if not (support_reactions & {"retaliate", "breakup_warning"}):
        lines.append("support cases stay away from retaliate and breakup_warning.")
    else:
        lines.append("unexpected: support cases produced a high-conflict reaction.")

    hidden_conflicts = [
        observation
        for observation in observations_for(observations, case_id="CASE_PRIVACY_HIDDEN")
        if observation.npc_public_conflict
    ]
    if not hidden_conflicts:
        lines.append("hidden privacy cases have public_conflict=false.")
    else:
        lines.append("unexpected: hidden privacy case produced public conflict.")

    deception_reactions = {
        observation.npc_reaction_type
        for observation in observations_for(observations, case_id="CASE_DECEPTION_DISCOVERED")
    }
    lines.append(
        "discovered deception reactions vary: "
        + ", ".join(sorted(deception_reactions))
    )

    revengeful_retaliations = [
        observation
        for observation in observations_for(observations, npc_id="NPC_D_REVENGEFUL")
        if observation.npc_reaction_type == "retaliate"
    ]
    retaliation_cases = sorted(_case_id(observation) for observation in revengeful_retaliations)
    lines.append(
        "revengeful NPC retaliates only in: "
        + (", ".join(retaliation_cases) if retaliation_cases else "none")
    )

    high_self_respect_repeat = observations_for(
        observations,
        case_id="CASE_REPEAT_DECEPTION",
        npc_id="NPC_E_HIGH_SELF_RESPECT",
    )
    if high_self_respect_repeat:
        lines.append(
            "high self-respect under repeated deception: "
            + high_self_respect_repeat[0].npc_reaction_type
        )

    communicator = observations_for(
        observations,
        case_id="CASE_DECEPTION_DISCOVERED",
        npc_id="NPC_A_COMMUNICATOR",
    )
    avoidant = observations_for(
        observations,
        case_id="CASE_DECEPTION_DISCOVERED",
        npc_id="NPC_C_AVOIDANT",
    )
    if communicator and avoidant:
        lines.append(
            "communicator vs avoidant on discovered deception: "
            f"{communicator[0].npc_reaction_type} vs {avoidant[0].npc_reaction_type}"
        )

    return lines


def _case_id(observation: PlaytestObservation) -> str:
    for tag in observation.tags:
        if tag.startswith("case:"):
            return tag.removeprefix("case:")
    return "unknown_case"


def _unique(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result

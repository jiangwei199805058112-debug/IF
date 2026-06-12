from __future__ import annotations

from typing import Any, Mapping, Sequence


ENTRY_LABELS = {
    "chatting": "正在聊天",
    "ambiguous": "暧昧中",
    "new_relationship": "刚恋爱",
    "正在聊天": "正在聊天",
    "暧昧中": "暧昧中",
    "刚恋爱": "刚恋爱",
}

ENTRY_KEYS = {
    "chatting": "chatting",
    "正在聊天": "chatting",
    "ambiguous": "ambiguous",
    "暧昧中": "ambiguous",
    "new_relationship": "new_relationship",
    "刚恋爱": "new_relationship",
}

ATMOSPHERE_LABELS = {
    "warm_up": "稳定",
    "stable": "稳定",
    "slightly_uncertain": "微妙",
    "needs_clarification": "微妙",
    "repair_window_open": "微妙",
    "cooling_down": "降温",
    "avoidance_accumulating": "降温",
    "tension_rising": "紧张",
    "crisis": "危机",
}

INITIATIVE_LABELS = {
    "warm_up": "正常",
    "stable": "正常",
    "repair_window_open": "正常",
    "slightly_uncertain": "变少",
    "needs_clarification": "变少",
    "cooling_down": "变少",
    "avoidance_accumulating": "明显回避",
    "tension_rising": "明显回避",
    "crisis": "明显回避",
}

UNEASE_LABELS = {
    "warm_up": "低",
    "stable": "低",
    "repair_window_open": "中",
    "slightly_uncertain": "中",
    "needs_clarification": "中",
    "cooling_down": "中",
    "avoidance_accumulating": "高",
    "tension_rising": "高",
    "crisis": "高",
}

REPAIR_WINDOW_LABELS = {
    "warm_up": "开放",
    "stable": "开放",
    "repair_window_open": "开放",
    "slightly_uncertain": "变窄",
    "needs_clarification": "变窄",
    "cooling_down": "变窄",
    "avoidance_accumulating": "暂时关闭",
    "tension_rising": "暂时关闭",
    "crisis": "暂时关闭",
}

ACTION_SETS = {
    "chatting": [
        {"action_key": "light_message", "label": "主动发一条轻松消息"},
        {"action_key": "ask_busy", "label": "认真问对方最近是不是很忙"},
        {"action_key": "share_daily", "label": "分享一点自己的日常"},
        {"action_key": "wait_contact", "label": "等对方主动联系"},
        {"action_key": "focus_self", "label": "先做自己的事，减少查看消息"},
    ],
    "ambiguous": [
        {"action_key": "keep_light", "label": "保持轻松聊天"},
        {"action_key": "express_interest", "label": "试探性表达一点好感"},
        {"action_key": "suggest_meet", "label": "约一次见面"},
        {"action_key": "clarify_thoughts", "label": "认真确认对方最近的想法"},
        {"action_key": "observe", "label": "暂时观察，不主动推进"},
    ],
    "new_relationship": [
        {"action_key": "show_care", "label": "表达关心"},
        {"action_key": "confirm_boundary", "label": "确认相处边界"},
        {"action_key": "arrange_meet", "label": "安排一次见面"},
        {"action_key": "discuss_pace", "label": "谈一下未来节奏"},
        {"action_key": "give_space", "label": "给对方一点空间"},
    ],
}

ACTION_EFFECTS = {
    "light_message": {
        "base_atmosphere": "warm_up",
        "relationship_delta": {"trust": 1},
        "context_tags": ["warm_action"],
    },
    "ask_busy": {
        "base_atmosphere": "needs_clarification",
        "relationship_delta": {"pressure": 1},
        "context_tags": ["repair_action", "clarifying_action"],
    },
    "share_daily": {
        "base_atmosphere": "warm_up",
        "relationship_delta": {"security": 1},
        "context_tags": ["warm_action", "disclosure_action"],
    },
    "wait_contact": {
        "base_atmosphere": "slightly_uncertain",
        "relationship_delta": {"security": -1, "disappointment": 1},
        "context_tags": ["cold_action", "waiting_action"],
    },
    "focus_self": {
        "base_atmosphere": "stable",
        "relationship_delta": {"pressure": -1},
        "context_tags": ["self_regulation_action"],
    },
    "keep_light": {
        "base_atmosphere": "stable",
        "relationship_delta": {},
        "context_tags": ["stable_action"],
    },
    "express_interest": {
        "base_atmosphere": "warm_up",
        "relationship_delta": {"security": 1},
        "context_tags": ["warm_action"],
    },
    "suggest_meet": {
        "base_atmosphere": "warm_up",
        "relationship_delta": {"pressure": 1, "trust": 1},
        "context_tags": ["warm_action", "advance_action"],
    },
    "clarify_thoughts": {
        "base_atmosphere": "needs_clarification",
        "relationship_delta": {"conflict": -1, "pressure": 1},
        "context_tags": ["repair_action", "clarifying_action"],
    },
    "observe": {
        "base_atmosphere": "slightly_uncertain",
        "relationship_delta": {"security": -1},
        "context_tags": ["cold_action", "waiting_action"],
    },
    "show_care": {
        "base_atmosphere": "warm_up",
        "relationship_delta": {"security": 1},
        "context_tags": ["warm_action"],
    },
    "confirm_boundary": {
        "base_atmosphere": "repair_window_open",
        "relationship_delta": {"conflict": -1, "pressure": 1},
        "context_tags": ["repair_action", "boundary_action"],
    },
    "arrange_meet": {
        "base_atmosphere": "warm_up",
        "relationship_delta": {"trust": 1, "pressure": 1},
        "context_tags": ["warm_action", "advance_action"],
    },
    "discuss_pace": {
        "base_atmosphere": "needs_clarification",
        "relationship_delta": {"conflict": -1, "pressure": 1},
        "context_tags": ["repair_action", "clarifying_action"],
    },
    "give_space": {
        "base_atmosphere": "slightly_uncertain",
        "relationship_delta": {"pressure": -1},
        "context_tags": ["cold_action", "space_action"],
    },
}

NPC_NAMES = {
    "A": "周然",
    "B": "许知遥",
    "C": "陈予",
    "D": "夏宁",
    "E": "陆晚",
}

NPC_RESPONSE_TEMPLATES = {
    "A": {
        "light_message": [
            "周然过了一会儿回了个表情，又补一句：“今天还行。” 话题被接住，但节奏还是慢。",
            "周然回：“你这个话题还挺轻松。” 他多聊了两句，只是没有主动展开太多。",
            "周然晚点才回：“刚忙完，看到你发的了。” 语气不冷，但主动性仍然有限。",
        ],
        "ask_busy": [
            "周然过了一会儿回：“最近确实忙，没什么特别的。” 他没有拒绝你，但解释依然很短。",
            "周然说：“不是故意不回，就是事情堆在一起。” 他愿意说明，但还是省掉了细节。",
            "周然停了一阵才回：“我这几天状态一般，晚点跟你说。” 这次至少留下了继续说的口子。",
        ],
        "wait_contact": [
            "周然直到晚上才回一句：“刚看到。” 话题还在，只是主动性很弱。",
            "周然很晚发来：“今天太累了。” 你等到了回应，但没有等到太多热度。",
            "周然隔了几个小时才问：“你今天怎么样？” 这像补上联系，也像维持最低频率。",
        ],
        "clarify_thoughts": "周然停了很久才说：“我不是不想聊，就是最近真的累。” 他愿意解释，但还不太会展开。",
        "confirm_boundary": "周然说：“可以，你说清楚我会记一下。” 他的语气平稳，但回复仍然偏短。",
    },
    "B": {
        "ask_busy": [
            "许知遥回：“怎么突然问这个？你是不是也有什么没说？” 她回应了你，但语气里带着一点反问。",
            "许知遥很快说：“你可以问，但别只让我解释。” 她接住了问题，也把压力推回一点。",
        ],
        "wait_contact": [
            "许知遥先发来一个问号，又补一句：“你今天也挺能忍啊。” 她没有消失，却明显在试探。",
            "许知遥隔了一会儿发：“今天不找我？” 这像主动，也像在确认你会不会先靠近。",
        ],
        "clarify_thoughts": "许知遥说：“你想确认可以，但你也要告诉我你到底在担心什么。” 她接话很快，边界感也更尖。",
        "confirm_boundary": "许知遥回：“可以谈，但别只要求我，你自己的社交也要一样。” 话题被接住，也带着比较。",
    },
    "C": {
        "suggest_meet": "陈予回：“可以，但我这两天预算和时间都要看一下。” 他没有拒绝，只是先把现实条件摆出来。",
        "arrange_meet": "陈予说：“见面可以，选个不太折腾的地方吧。” 他更在意安排是否实际。",
        "share_daily": "陈予回了一个具体建议：“那你先把手头的事做完，晚点再聊。” 回应不热烈，但很实在。",
    },
    "D": {
        "observe": "夏宁隔了很久才回：“随你。” 聊天没有断，但冷意更明显。",
        "wait_contact": "夏宁发来一句：“你不找我，我还以为你不想聊了。” 这句话像回应，也像试探。",
        "give_space": "夏宁说：“那就先这样。” 她接受了空间，但气氛没有真的放松。",
    },
    "E": {
        "show_care": "陆晚回：“我知道你是在关心我。” 她接住了这句话，但仍在观察你会不会持续。",
        "discuss_pace": "陆晚说：“可以慢慢谈，我不想只是靠猜。” 她愿意把节奏摆到台面上。",
        "keep_light": [
            "陆晚顺着你的话题聊了几句，又轻轻问：“你今天心情还好吗？” 她没有逼近，但在确认你的状态。",
            "陆晚接住了你的轻松话题，最后补一句：“这样聊也挺舒服的。” 气氛比前一天松了一点。",
            "陆晚回得不算快，但每句都有回应。她没有推进关系，只是让聊天继续保持温度。",
        ],
    },
}

FALLBACK_RESPONSES = {
    "A": [
        "{name}回得不快，但还是接住了话题：“嗯，我看到了，晚点细说。”",
        "{name}隔了一阵才回：“我刚处理完事。” 话题还在，只是节奏偏慢。",
        "{name}回了一句简短的话，又补了个表情。你能感觉到他没有完全避开。",
    ],
    "B": [
        "{name}很快回：“你今天好像有点不一样，是不是在试我？”",
        "{name}接得很快：“可以聊，但你也别只让我猜。” 回应里带着一点较劲。",
        "{name}问：“你是真的想聊，还是想看我会不会主动？” 话题被接住，但张力也上来了。",
    ],
    "C": [
        "{name}说：“可以，我们把时间和安排说清楚就行。”",
        "{name}回：“这事能谈，先看怎么安排比较实际。” 他把话题拉回可执行的部分。",
        "{name}没有说太多情绪，只问你：“那你希望我具体怎么做？”",
    ],
    "D": [
        "{name}隔了一会儿回：“你想怎样就怎样吧。” 话没断，但温度偏低。",
        "{name}只回了两个字：“随你。” 联系还在，气氛却明显更冷。",
        "{name}晚点才说：“我现在不想聊太多。” 这不是断联，但回避感更明显。",
    ],
    "E": [
        "{name}回：“我知道你在意这个，我们可以慢慢说。”",
        "{name}说：“我不想靠猜，我们把话说清楚会好一点。”",
        "{name}停了一会儿才回：“我会听你说，但也想知道你真正担心什么。”",
    ],
}

ATMOSPHERE_RESULT_TEXT = {
    "warm_up": "关系有一点升温，但还没到可以完全放松的程度。",
    "stable": "今天的互动比较平稳，没有明显升温或降温。",
    "slightly_uncertain": "气氛变得有点微妙，主动性没有完全接上。",
    "needs_clarification": "有些话被摆到了台面上，但还需要后续回应。",
    "repair_window_open": "关系仍有修复窗口，关键在于之后是否继续说清。",
    "cooling_down": "气氛开始降温，联系还在，但热度变弱。",
    "avoidance_accumulating": "回避感正在累积，之后更容易进入冷处理。",
    "tension_rising": "张力变高，接下来的解释和边界会更敏感。",
    "crisis": "关系已经在危机边缘，普通互动很难立刻抵消前面的伤害。",
}


def get_daily_actions(
    day: int,
    entry_mode: str,
    profile_pair_id: str,
    atmosphere: str,
    context_tags: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Return the fixed daily action menu for an ordinary day."""

    entry_key = ENTRY_KEYS.get(entry_mode, "ambiguous")
    actions = ACTION_SETS[entry_key]
    return [
        {
            "action_key": action["action_key"],
            "label": action["label"],
            "day": day,
            "entry_mode": ENTRY_LABELS.get(entry_mode, entry_mode),
        }
        for action in actions
    ]


def resolve_daily_action(
    action_key: str,
    day: int,
    entry_mode: str,
    profile_pair_id: str,
    atmosphere: str,
    relationship_state: Any,
    initial_modifiers: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Resolve one ordinary-day action into player-facing text and light state effects."""

    action = _find_action(action_key, entry_mode)
    effect = ACTION_EFFECTS.get(action["action_key"], ACTION_EFFECTS["keep_light"])
    context_tags = list(effect.get("context_tags", []))
    current_atmosphere = _state_aware_atmosphere(atmosphere, relationship_state)
    next_atmosphere = _next_atmosphere_tag(
        action["action_key"],
        current_atmosphere,
        context_tags,
        relationship_state,
    )

    return {
        "action_label": action["label"],
        "npc_response": _npc_response(profile_pair_id, action["action_key"], day, relationship_state),
        "atmosphere_tag": next_atmosphere,
        "relationship_delta": _bounded_relationship_delta(effect.get("relationship_delta", {})),
        "player_feedback": _player_feedback(action["action_key"], next_atmosphere, initial_modifiers),
        "debug_reason": _debug_reason(action["action_key"], current_atmosphere, next_atmosphere, context_tags),
        "context_tags": context_tags,
    }


def format_daily_status_header(day: int, entry_mode: str, atmosphere: str) -> list[str]:
    """Format the visible daily state header without exposing internal numbers."""

    tag = _known_atmosphere(atmosphere)
    entry_label = ENTRY_LABELS.get(entry_mode, entry_mode)
    return [
        f"状态头部：第 {day} 天｜{entry_label}",
        f"氛围：{ATMOSPHERE_LABELS[tag]}",
        f"对方主动性：{INITIATIVE_LABELS[tag]}",
        f"你的不安：{UNEASE_LABELS[tag]}",
        f"修复窗口：{REPAIR_WINDOW_LABELS[tag]}",
    ]


def format_daily_action_result(result: Mapping[str, Any]) -> list[str]:
    """Format what the player did, how the NPC responded, and how the atmosphere moved."""

    atmosphere_tag = _known_atmosphere(str(result.get("atmosphere_tag", "stable")))
    return [
        f"每日行动：{result.get('action_label', '')}",
        f"对方回应：{result.get('npc_response', '')}",
        f"氛围变化：{ATMOSPHERE_RESULT_TEXT[atmosphere_tag]}",
        f"你的感受：{result.get('player_feedback', '')}",
    ]


def derive_atmosphere_after_event(
    event_id: str,
    branch_id: str,
    choice_tag: str,
    current_atmosphere: str,
) -> str:
    """Map existing key events to the lightweight atmosphere layer."""

    if event_id == "MSG_001":
        if branch_id == "MSG_001_A":
            return "repair_window_open" if choice_tag in {"accept", "ask_softly"} else "stable"
        if branch_id == "MSG_001_E":
            return "tension_rising"
        if choice_tag in {"push_hard", "cool_down"}:
            return "tension_rising" if choice_tag == "push_hard" else "cooling_down"
        return "slightly_uncertain"

    if event_id == "SOC_001":
        if branch_id == "SOC_001_A":
            return "stable"
        if branch_id in {"SOC_001_C", "SOC_001_F"}:
            return "crisis"
        if choice_tag in {"set_boundary", "accept"}:
            return "repair_window_open"
        if choice_tag in {"verify", "cold"}:
            return "tension_rising"
        return "needs_clarification"

    if event_id == "CONFLICT_001":
        if branch_id == "CONFLICT_001_A":
            return "repair_window_open"
        if branch_id == "CONFLICT_001_D":
            return "crisis"
        if branch_id in {"CONFLICT_001_C", "CONFLICT_001_E"}:
            return "cooling_down" if choice_tag in {"cold", "private_talk"} else "tension_rising"
        if choice_tag in {"private_talk", "apologize_boundary", "reconnect_or_break"}:
            return "repair_window_open"
        return "tension_rising"

    return _known_atmosphere(current_atmosphere)


def format_aftershock_context(day: int, event_resolution_log: list[Mapping[str, Any]]) -> list[str]:
    """Return lightweight aftermath copy for day 4, 9, or 13."""

    previous_event = {4: "MSG_001", 9: "SOC_001", 13: "CONFLICT_001"}.get(day)
    if not previous_event:
        return []

    event_log = _find_event_log(event_resolution_log, previous_event)
    if not event_log:
        return []

    choice_tag = str(event_log.get("choice_tag", ""))
    branch_id = str(event_log.get("branch_id", ""))

    if previous_event == "MSG_001":
        if branch_id == "MSG_001_A" or choice_tag == "accept":
            text = "你决定先不把事情说重，但昨天那次延迟仍然让你更注意回复节奏。"
        elif choice_tag == "push_hard":
            text = "昨天你把不满说得比较直接，对方今天的回复明显谨慎了一点。"
        elif choice_tag == "cool_down":
            text = "昨天你也冷了一点，今天聊天框安静得更久。"
        else:
            text = "你温和问过对方是不是太忙，但那个“刚忙完”的解释仍然有点短。"
    elif previous_event == "SOC_001":
        if branch_id in {"SOC_001_C", "SOC_001_F"}:
            text = "昨天的信息缺口变得更重，今天任何解释都会先经过信任问题。"
        elif choice_tag == "set_boundary":
            text = "昨天你把异性社交边界说了出来，今天要看对方是否真的接住。"
        elif choice_tag == "verify":
            text = "昨天你选择查证，今天气氛没有直接爆开，但信任感更紧。"
        elif choice_tag == "cold":
            text = "昨天你先冷下来，今天这件事仍像没有收尾。"
        else:
            text = "昨天你暂时接受了解释，但边界和说明方式还没有完全落地。"
    else:
        if branch_id == "CONFLICT_001_A":
            text = "昨天你们尝试把冲突说清，今天关系还有一点修复余地。"
        elif branch_id == "CONFLICT_001_D":
            text = "昨天连接被切断过，今天每一句回复都像在确认还能不能继续。"
        elif branch_id == "CONFLICT_001_C" or choice_tag == "cold":
            text = "昨天你们把话停住，今天沉默更像一种姿态。"
        elif choice_tag in {"apologize_boundary", "private_talk", "reconnect_or_break"}:
            text = "昨天你试着把冲突收回来，今天还要看对方愿不愿意继续谈。"
        else:
            text = "昨天的冲突没有完全散去，今天的普通回应也带着余波。"

    return [f"余波日：{text}"]


def format_midpoint_feedback(atmosphere: str, action_history: list[Mapping[str, Any]]) -> list[str]:
    """Format day-7 feedback with trend, player pattern, and a day-8 setup."""

    trend = _trend_label(atmosphere, action_history)
    pattern = _behavior_pattern(action_history)
    return [
        "第 7 天中期反馈：",
        f"- 当前氛围趋势：{trend}。",
        f"- 玩家行为模式：{pattern}。",
        "- 第 8 天前的轻微铺垫：一些边界、解释方式和信任问题还没有真正说清。",
    ]


def _find_action(action_key: str, entry_mode: str) -> dict[str, Any]:
    entry_key = ENTRY_KEYS.get(entry_mode, "ambiguous")
    all_actions = ACTION_SETS[entry_key]
    for action in all_actions:
        if action["action_key"] == action_key:
            return action
    return all_actions[0]


def _state_aware_atmosphere(atmosphere: str, relationship_state: Any) -> str:
    tag = _known_atmosphere(atmosphere)
    hooks = set(_as_strings(getattr(relationship_state, "active_hooks", [])))
    if "crisis" in hooks:
        return "crisis"
    if hooks.intersection({"cold_war", "reply_slowdown"}) and tag in {"stable", "warm_up"}:
        return "cooling_down"
    if hooks.intersection({"boundary_talk", "trust_talk", "reply_pattern_watch"}) and tag == "stable":
        return "slightly_uncertain"
    return tag


def _next_atmosphere_tag(
    action_key: str,
    current_atmosphere: str,
    context_tags: list[str],
    relationship_state: Any,
) -> str:
    current = _known_atmosphere(current_atmosphere)
    if current == "crisis":
        return "crisis"

    cool_streak = _cooling_streak(relationship_state)
    if "cold_action" in context_tags:
        cool_streak += 1
        if cool_streak >= 3:
            return "avoidance_accumulating" if current in {"cooling_down", "avoidance_accumulating"} else "cooling_down"
        if current in {"tension_rising", "cooling_down", "avoidance_accumulating"}:
            return "cooling_down"

    if "repair_action" in context_tags:
        return "repair_window_open" if current in {"cooling_down", "tension_rising", "needs_clarification"} else "needs_clarification"

    if "warm_action" in context_tags:
        if current in {"cooling_down", "avoidance_accumulating", "tension_rising"}:
            return "slightly_uncertain"
        return "warm_up"

    if "stable_action" in context_tags and current in {"cooling_down", "avoidance_accumulating", "tension_rising"}:
        return "slightly_uncertain"

    effect = ACTION_EFFECTS.get(action_key, ACTION_EFFECTS["keep_light"])
    return _known_atmosphere(str(effect.get("base_atmosphere", "stable")))


def _cooling_streak(relationship_state: Any) -> int:
    history = getattr(relationship_state, "daily_action_history", [])
    streak = 0
    for item in reversed(history):
        tags = set(_as_strings(_mapping(item).get("context_tags", [])))
        if "cold_action" not in tags:
            break
        streak += 1
    return streak


def _npc_response(profile_pair_id: str, action_key: str, day: int, relationship_state: Any) -> str:
    pair_id = profile_pair_id if profile_pair_id in NPC_NAMES else "A"
    response = NPC_RESPONSE_TEMPLATES.get(pair_id, {}).get(action_key)
    if response:
        return _rotated_response(response, day, _action_repeat_count(relationship_state, action_key))
    name = NPC_NAMES.get(pair_id, "对方")
    fallback = FALLBACK_RESPONSES.get(pair_id, FALLBACK_RESPONSES["A"])
    return _rotated_response(fallback, day, _action_repeat_count(relationship_state, action_key)).format(name=name)


def _rotated_response(response: str | Sequence[str], day: int, repeat_count: int) -> str:
    if isinstance(response, str):
        return response
    variants = [item for item in response if item]
    if not variants:
        return ""
    index = (int(day) + int(repeat_count)) % len(variants)
    return str(variants[index])


def _action_repeat_count(relationship_state: Any, action_key: str) -> int:
    history = getattr(relationship_state, "daily_action_history", [])
    count = 0
    for item in history:
        if str(_mapping(item).get("action_key", "")) == action_key:
            count += 1
    return count


def _player_feedback(
    action_key: str,
    atmosphere_tag: str,
    initial_modifiers: dict[str, Any] | None,
) -> str:
    modifiers = initial_modifiers or {}
    reassurance_delta = int(modifiers.get("reassurance_need_delta", 0) or 0)

    if action_key in {"wait_contact", "observe", "give_space"}:
        if reassurance_delta >= 2:
            return "这一天没有新的消息，你发现自己很难不去反复确认聊天框。"
        if reassurance_delta <= -2:
            return "你把注意力放回自己的事，对方晚些时候发来一句简单问候。"
        return "你没有继续推进，关系没有断开，但主动性明显变弱。"

    if action_key in {"ask_busy", "clarify_thoughts", "confirm_boundary", "discuss_pace"}:
        return "你把问题说得比昨天更具体，接下来要看对方是否持续回应。"

    if atmosphere_tag == "warm_up":
        return "你能感觉到一点靠近，但仍然保留观察。"
    if atmosphere_tag in {"cooling_down", "avoidance_accumulating"}:
        return "这不是一次爆点，但连续这样下去会让关系变冷。"
    if atmosphere_tag == "tension_rising":
        return "你开始更在意对方下一次会怎么解释。"
    return "你把今天的互动当作一个小信号，而不是最终结论。"


def _bounded_relationship_delta(delta: Any) -> dict[str, int]:
    if not isinstance(delta, Mapping):
        return {}
    result: dict[str, int] = {}
    for field in ("trust", "security", "pressure", "conflict", "disappointment", "flaw"):
        value = _int(delta.get(field, 0))
        if value:
            result[field] = max(-1, min(1, value))
    return result


def _trend_label(atmosphere: str, action_history: list[Mapping[str, Any]]) -> str:
    tag = _known_atmosphere(atmosphere)
    if tag in {"tension_rising", "crisis"}:
        return "紧张"
    if tag in {"cooling_down", "avoidance_accumulating"}:
        return "降温"

    warm_count = _history_count(action_history, "warm_action")
    cold_count = _history_count(action_history, "cold_action")
    repair_count = _history_count(action_history, "repair_action")
    if cold_count >= 3 and cold_count > warm_count + repair_count:
        return "降温"
    if warm_count >= cold_count + 2:
        return "升温"
    return "稳定"


def _behavior_pattern(action_history: list[Mapping[str, Any]]) -> str:
    cold_count = _history_count(action_history, "cold_action")
    repair_count = _history_count(action_history, "repair_action")
    warm_count = _history_count(action_history, "warm_action")
    if repair_count >= 2:
        return "修复倾向"
    if cold_count >= 3:
        return "冷处理倾向"
    if cold_count >= 2:
        return "等待观察"
    if warm_count >= 2:
        return "主动沟通"
    return "主动沟通"


def _history_count(action_history: list[Mapping[str, Any]], tag: str) -> int:
    total = 0
    for item in action_history:
        if tag in set(_as_strings(_mapping(item).get("context_tags", []))):
            total += 1
    return total


def _find_event_log(event_resolution_log: list[Mapping[str, Any]], event_id: str) -> Mapping[str, Any] | None:
    for item in reversed(event_resolution_log):
        if str(item.get("event_id", "")) == event_id:
            return item
    return None


def _known_atmosphere(atmosphere: str) -> str:
    return atmosphere if atmosphere in ATMOSPHERE_LABELS else "stable"


def _debug_reason(
    action_key: str,
    current_atmosphere: str,
    next_atmosphere: str,
    context_tags: list[str],
) -> str:
    return (
        f"action={action_key}; atmosphere={current_atmosphere}->{next_atmosphere}; "
        f"tags={','.join(context_tags)}"
    )


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _as_strings(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, tuple):
        return [str(item) for item in value]
    if isinstance(value, set):
        return [str(item) for item in value]
    if value:
        return [str(value)]
    return []


def _int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0

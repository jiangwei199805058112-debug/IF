# 归因、记忆与关系信念系统设计 v0.1

本文档定义 IF 后续可扩展的归因、记忆重构与关系信念系统。它承接：

- `docs/design/15_full_questionnaire_upgrade_plan.md`
- `docs/design/16_questionnaire_dimension_table.md`
- `docs/design/19_relationship_report_templates.md`
- `docs/design/22_questionnaire_scoring_rules.md`
- `docs/design/23_questionnaire_dimension_coverage.md`
- `docs/design/24_questionnaire_json_schema.md`

本文档只做设计沉淀，不修改 Python 代码，不修改现有题库 JSON，也不接入当前 14 天控制台原型。

## 1. 设计目标

IF 的关系模拟不应只判断“发生了什么”，还要模拟角色如何解释这件事。现实亲密关系中，同一事件可能被解释成：

- “他晚回消息，是因为工作忙。”
- “他晚回消息，是因为不在乎我。”
- “他总是这样，迟早会离开。”
- “这次是特殊情况，先看看后续行动。”

这些解释会影响满意度、信任、旧伤记忆、冲突升级和修复机会。因此本系统的目标是新增一个“事件解释层”：

```text
event fact
  ↓
attribution interpretation
  ↓
emotion and trust delta
  ↓
memory write / memory rewrite
  ↓
relationship belief update
  ↓
report tags and future event weights
```

该系统不是心理诊断，不用于评价现实玩家好坏，只用于游戏内关系行为模拟和玩家可读报告。

## 2. 理论映射

### 2.1 归因理论 attribution

归因理论关注人如何解释自己和他人的行为原因。IF 中每个关键事件都可以拆成：

| 层级 | 含义 | 示例 |
| --- | --- | --- |
| 事实层 | 实际发生的行为 | 对方 4 小时没有回消息 |
| 解释层 | 角色认为原因是什么 | 工作忙 / 不在乎 / 故意冷淡 |
| 后果层 | 解释导致的情绪和关系变化 | 安心等待 / 不安追问 / 冷处理 |

IF 不应直接用事件事实决定关系变化，而应让角色的归因风格参与解释。

### 2.2 内部/外部归因

内部归因把行为原因解释为人的人格、态度或真实意图。外部归因把行为原因解释为情境、压力、偶发条件。

| 归因方向 | IF 表达 | 晚回消息示例 |
| --- | --- | --- |
| 内部归因 | “这是对方本人的问题或真实态度” | 他就是不重视我 |
| 外部归因 | “这是情境造成的，不一定代表关系变差” | 他可能在忙、手机没电或开会 |

内部归因更容易改变长期印象和旧伤记忆，外部归因更容易保留修复空间。

### 2.3 稳定/易变归因

稳定归因认为原因长期存在，未来还会重复。易变归因认为原因是暂时状态或短期情境。

| 归因方向 | IF 表达 | 神秘电话示例 |
| --- | --- | --- |
| 稳定归因 | “这说明对方一直不透明” | 他本来就是会藏事的人 |
| 易变归因 | “这可能是一次特殊情况” | 这通电话需要解释，但不一定代表长期隐瞒 |

稳定归因会提高 `risk_repeat_pattern`、`trust_old_wound_memory` 和长期满意度损耗。

### 2.4 普遍/特殊归因

普遍归因认为问题会出现在很多场景。特殊归因认为问题局限于这一次或这类具体事件。

| 归因方向 | IF 表达 | 异性饭局示例 |
| --- | --- | --- |
| 普遍归因 | “他很多事情都会这样处理” | 饭局不说，以后别的事也不会说 |
| 特殊归因 | “这件事本身容易误会” | 异性饭局需要说明，但不代表所有事情都不可信 |

普遍归因会让单一事件扩散到多层信任；特殊归因只影响相关信任层。

### 2.5 幸福伴侣与痛苦伴侣的归因模式

幸福关系中的伴侣更容易：

- 把对方的积极行为解释为内部、稳定、普遍原因；
- 把对方的消极行为解释为外部、易变、特殊原因；
- 给解释和修复留下空间。

痛苦关系中的伴侣更容易：

- 把对方的积极行为解释为外部、易变、特殊原因；
- 把对方的消极行为解释为内部、稳定、普遍原因；
- 把单次事件写入旧伤或关系信念。

IF 中这不应写成“幸福/痛苦人格”，而应作为当前关系状态和历史记忆共同生成的解释偏向。

### 2.6 自利归因 self-serving bias

自利归因指人倾向于把自己的好行为归因为自身品质，把自己的坏行为归因为外部压力；对他人则可能反过来。

IF 示例：

```text
自己晚回消息：我真的太忙了。
对方晚回消息：他没有把我放在优先级。
```

自利归因会影响双标、冲突责任分配、道歉质量和报告中的自述/行为差异。

### 2.7 行动者/观察者效应 actor-observer effect

行动者更容易看到自己行为背后的情境压力，观察者更容易从行为推断对方人格或态度。

IF 示例：

```text
玩家隐瞒异性饭局时：我只是怕吵架，不是不诚实。
NPC 看到玩家隐瞒时：你选择隐瞒，说明我不能相信你。
```

该效应适合接入 NPC 视角、双标配对题、冲突升级和事实信任变化。

### 2.8 记忆重构 reconstructive memory

亲密关系中的记忆不是录像，而会被当前情绪、旧伤、关系信念和后续解释重构。

IF 中同一旧事件可以发生三种变化：

| 重构方向 | 触发条件 | 结果 |
| --- | --- | --- |
| 负向重构 | 新事件与旧伤相似，解释不完整 | 过去的小事被重新理解成早有征兆 |
| 正向重构 | 对方持续补偿、解释一致 | 过去的伤害被重新理解为可修复错误 |
| 模糊重构 | 时间久、证据少、后续事件冲突 | 记忆确定度下降，但情绪残留存在 |

因此旧伤记忆不仅记录“发生过”，还应记录“当前怎么被理解”。

### 2.9 关系信念 relationship beliefs / schemas

关系信念是角色对亲密关系的默认规则，例如：

- 真爱应该自然懂我；
- 关系需要经营和沟通；
- 吵架说明不合适；
- 对方爱我就不会让我不安；
- 一次背叛说明以后都会背叛。

IF 中关系信念会影响事件解释、满意度、修复机会、承诺节奏和报告文本。它不是单一人格标签，而是可被问卷、经历和游戏行为逐步更新的规则系统。

## 3. 系统位置

归因、记忆与信念系统位于问卷画像和事件引擎之间。

```text
self_report_profile
behavior_profile
relationship_state
old_wound_memory
  ↓
attribution_memory_belief_state
  ↓
event interpretation
  ↓
trust layers / satisfaction / conflict / repair
```

与现有 128维主表关系：

- 本文新增字段是系统状态字段，不等同于 128维维度 ID；
- 它们可以由已有维度推导，例如 `trust_old_wound_memory`、`self_justification_tendency`、`boundary_double_standard`；
- 后续也可以通过 Q151-Q180 新题直接测量。

## 4. 字段草案

### 4.1 顶层结构

```text
attribution_memory_belief_state:
  attribution_style:
    positive_behavior_attribution: internal_stable_global
    negative_behavior_attribution: external_unstable_specific
  actor_observer_gap: medium
  self_serving_bias: medium_low
  memory_reconstruction_bias: slightly_negative
  relationship_beliefs:
    destiny_belief: medium
    growth_belief: high
    mind_reading_expectation: low
    conflict_destructive_belief: low
```

### 4.2 字段定义

| 字段 | 类型 | 含义 | 高值表现 |
| --- | --- | --- | --- |
| `attribution_style` | object | 角色解释事件的总体模式 | 形成稳定的好意/恶意解释倾向 |
| `positive_behavior_attribution` | enum/score | 对积极行为如何归因 | 高质量关系中更倾向内部、稳定、普遍 |
| `negative_behavior_attribution` | enum/score | 对消极行为如何归因 | 高冲突关系中更倾向内部、稳定、普遍 |
| `actor_observer_gap` | 0-100 | 解释自己与解释对方时的差距 | 自己看情境，对方看人格 |
| `self_serving_bias` | 0-100 | 自我保护式责任归因倾向 | 自己犯错怪压力，对方犯错怪态度 |
| `memory_reconstruction_bias` | enum/score | 旧记忆被当前情绪重构的方向 | 负向时旧事更容易被重新解释成伤害 |
| `destiny_belief` | 0-100 | 相信关系是否“合适/命中注定” | 一次冲突更容易被看成不合适 |
| `growth_belief` | 0-100 | 相信关系能通过沟通成长 | 更愿意复盘、协商、给修复机会 |
| `mind_reading_expectation` | 0-100 | 期待对方不用说也能懂 | 容易把没察觉解释为不在乎 |
| `conflict_destructive_belief` | 0-100 | 相信冲突会破坏关系 | 容易回避冲突或把争吵视为关系坏掉 |

### 4.3 归因枚举建议

```text
attribution_locus:
  - internal
  - external
attribution_stability:
  - stable
  - unstable
attribution_scope:
  - global
  - specific
attribution_valence:
  - benevolent
  - neutral
  - suspicious
  - hostile
```

组合示例：

| 组合 | 含义 | 报告表达 |
| --- | --- | --- |
| `internal_stable_global` | 认为原因来自对方本质，长期且普遍 | 你更容易把某些行为理解成稳定态度 |
| `external_unstable_specific` | 认为原因来自情境，短期且特殊 | 你更容易给具体情境留下解释空间 |
| `internal_unstable_specific` | 认为对方当下状态不好，但不一定长期如此 | 你会把问题聚焦在这次状态，而非整段关系 |
| `external_stable_global` | 认为外部环境长期阻碍关系 | 你可能把问题理解为现实条件持续不匹配 |

## 5. 与现有维度的映射

| 新字段 | 可由哪些现有维度推导 |
| --- | --- |
| `negative_behavior_attribution` | `trust_suspicion_sensitivity`、`trust_old_wound_memory`、`attachment_abandonment_anxiety` |
| `positive_behavior_attribution` | `trust_baseline`、`attachment_repair_receptivity`、`communication_listening_capacity` |
| `actor_observer_gap` | `boundary_double_standard`、`trust_projection_tendency`、`self_discrepancy_awareness` |
| `self_serving_bias` | `self_justification_tendency`、`moral_accountability_under_exposure`、`communication_defensiveness` |
| `memory_reconstruction_bias` | `trust_old_wound_memory`、`risk_repeat_pattern`、`emotion_suppression_tendency` |
| `destiny_belief` | `family_relationship_script`、`values_security_need`、`attachment_commitment_pace` |
| `growth_belief` | `communication_meta_discussion`、`self_reflection_capacity`、`attachment_repair_receptivity` |
| `mind_reading_expectation` | `emotion_reassurance_need`、`attachment_closeness_need`、`communication_directness` 低值 |
| `conflict_destructive_belief` | `communication_conflict_avoidance`、`emotion_shutdown_tendency`、`family_conflict_model` |

## 6. 影响范围

### 6.1 event interpretation

事件解释应先读取事实，再根据归因字段生成感知结果。

```text
晚回消息 fact:
  delay_hours: 4
  prior_notice: false
  current_pressure: high

interpretation:
  if negative_behavior_attribution is internal_stable_global:
    perceived_meaning = "对方不重视我"
  if negative_behavior_attribution is external_unstable_specific:
    perceived_meaning = "对方可能临时忙，但需要后续说明"
```

同一事实可以产生不同感知值，避免事件引擎机械加减。

### 6.2 relationship satisfaction

满意度不只受行为影响，也受解释影响。

| 归因模式 | 积极行为影响 | 消极行为影响 |
| --- | --- | --- |
| 幸福型归因 | 积极行为更能提高满意度 | 消极行为损耗较小，保留修复空间 |
| 痛苦型归因 | 积极行为被视为偶然，提升有限 | 消极行为被放大，满意度下降明显 |
| 自利归因高 | 自己行为对满意度损耗小，对方行为损耗大 | 容易形成“我有理由，你没理由”的关系叙事 |

### 6.3 trust layers

归因应作用于多层信任，而不是只改一个总信任值。

| 事件解释 | 主要影响信任层 |
| --- | --- |
| “他不回是忙” | 情感信任小幅下降或不变 |
| “他不回是不在乎” | 情感信任下降 |
| “他隐瞒异性饭局说明不诚实” | 事实信任、忠诚信任下降 |
| “他答应补偿但没做到” | 行动信任下降 |
| “他查我手机是因为不相信我” | 隐私信任下降 |
| “出事时他会逃” | 危机信任下降 |

### 6.4 old wound memory

旧伤记忆应记录事实、当时解释、当前解释和重构历史。

```text
old_wound_memory:
  memory_id: wound_message_delay_001
  original_event_id: day_4_late_reply
  original_interpretation: "可能是忙"
  current_interpretation: "这是冷落模式的早期信号"
  reconstruction_bias: negative
  activation_triggers:
    - late_reply
    - vague_explanation
  repair_progress: partial
```

当新事件与旧伤相似时，系统可以重新激活旧记忆，让本次事件变得更敏感。

### 6.5 conflict escalation

冲突升级可以由“事实严重度 × 归因恶意度 × 旧伤激活 × 信念”共同决定。

```text
escalation_risk =
  event_severity
  + hostile_attribution
  + old_wound_activation
  + mind_reading_expectation
  + conflict_destructive_belief
  - growth_belief
  - repair_history
```

高 `mind_reading_expectation` 会让“对方没有主动懂我”变成冲突理由。高 `conflict_destructive_belief` 会让小争吵更快升级为“我们是不是不合适”。

### 6.6 repair chance

修复机会不是只看道歉本身，还要看对方如何解释道歉。

| 条件 | 修复机会 |
| --- | --- |
| 高 `growth_belief` + 道歉具体 + 行动补偿 | 明显提高 |
| 高 `destiny_belief` + 把冲突视为“不合适” | 道歉效果下降 |
| 高 `negative_behavior_attribution` + 旧伤多次激活 | 修复需要更长行动证据 |
| 高 `self_serving_bias` | 自己道歉容易形式化，对方道歉更容易被挑错 |

### 6.7 report tags

报告标签应使用关系行为表达，不写诊断。

| 字段状态 | 可见标签候选 | 隐藏标签候选 |
| --- | --- | --- |
| 高 `negative_behavior_attribution` | 容易把模糊行为理解为关系风险 | `suspicious_attribution_pattern` |
| 高 `self_serving_bias` | 冲突中更容易为自己保留情境解释 | `self_serving_attribution_gap` |
| 高 `actor_observer_gap` | 自己和对方同类行为的解释标准不完全一致 | `actor_observer_gap_risk` |
| 负向 `memory_reconstruction_bias` | 新冲突容易重新激活旧伤 | `negative_memory_rewrite_risk` |
| 高 `growth_belief` | 愿意通过复盘和行动修复关系 | `repair_growth_belief_strength` |
| 高 `mind_reading_expectation` | 期待对方主动读懂需求 | `mind_reading_expectation_risk` |
| 高 `conflict_destructive_belief` | 容易把争吵理解成关系受损 | `conflict_fragility_belief` |

## 7. 事件例子

### 7.1 晚回消息

事实：

```text
event: late_reply
delay_hours: 4
prior_notice: false
external_pressure: work_high
```

不同解释：

| 归因模式 | 解释 | 后果 |
| --- | --- | --- |
| 外部、易变、特殊 | 他可能临时忙，但需要之后说明 | 轻微不安，等待解释 |
| 内部、稳定、普遍 | 他就是不把我放在优先级 | 情感信任下降，旧伤激活 |
| 自利归因高 | 我晚回是忙，他晚回是不在乎 | 双标和冲突责任偏差上升 |

系统影响：

- `event interpretation`：生成“忙/不在乎/冷处理”的感知文本；
- `relationship satisfaction`：按解释不同小幅或明显下降；
- `old wound memory`：若过去有冷落记忆，则写入重复模式；
- `repair chance`：主动说明原因并补偿联系可缓和。

### 7.2 神秘电话

事实：

```text
event: mysterious_call
phone_screen_hidden: true
explanation_detail: low
prior_trust: medium
```

不同解释：

| 归因模式 | 解释 | 后果 |
| --- | --- | --- |
| 特殊归因 | 这通电话可能不方便说，但需要边界说明 | 事实信任轻微下降 |
| 普遍归因 | 他很多事情都不会说全 | 事实信任和隐私信任下降 |
| 稳定内部归因 | 他本来就有秘密管理习惯 | 旧伤记忆增强 |

系统影响：

- `trust layers`：优先影响事实信任、隐私信任；
- `conflict escalation`：若解释继续模糊，怀疑敏感上升；
- `report tags`：可能生成“解释不完整敏感”“秘密管理风险”。

### 7.3 异性饭局

事实：

```text
event: opposite_sex_meal
reported_beforehand: false
meal_context: one_on_one
later_explanation: partial
```

不同解释：

| 归因模式 | 解释 | 后果 |
| --- | --- | --- |
| 外部、特殊 | 可能怕误会，但这件事需要补充说明 | 短期冲突，保留修复 |
| 内部、稳定 | 他会选择性表达关键事实 | 事实信任下降 |
| 普遍、恶意 | 饭局只是其中一件，他以后也会藏 | 事实信任、忠诚信任、旧伤记忆同步下降 |

系统影响：

- `event interpretation`：区分“边界失误”和“信息隐瞒模式”；
- `trust layers`：事实信任和忠诚信任同时变化；
- `repair chance`：完整说明、承认省略重点、后续边界协议可修复。

### 7.4 争吵后冷处理

事实：

```text
event: cold_treatment_after_fight
silence_hours: 12
conflict_unresolved: true
previous_cold_treatment_count: 2
```

不同解释：

| 归因模式 | 解释 | 后果 |
| --- | --- | --- |
| 易变归因 | 他情绪过载，需要时间冷静 | 短期不安，等待恢复 |
| 稳定归因 | 他每次冲突都逃避 | 冲突升级，行动信任下降 |
| 破坏性冲突信念高 | 一吵架就说明关系坏掉了 | 满意度明显下降，分手念头上升 |

系统影响：

- `conflict escalation`：旧冷处理次数越多，升级越快；
- `old wound memory`：写入“冲突后被丢下”的旧伤；
- `repair chance`：恢复沟通时若能解释冷静时间规则，可降低重复风险。

### 7.5 主动道歉和补偿

事实：

```text
event: apology_and_compensation
apology_specificity: high
responsibility_taken: true
compensation_action: concrete
repeat_prevention: stated
```

不同解释：

| 归因模式 | 解释 | 后果 |
| --- | --- | --- |
| 积极内部稳定归因 | 他是真的愿意修复，也有责任感 | 修复机会高，行动信任恢复 |
| 积极外部易变归因 | 他只是怕我生气，暂时哄一下 | 修复有限，需要后续行动 |
| 负向记忆重构高 | 这次道歉让我想起以前每次也说会改 | 道歉效果被旧伤抵消 |

系统影响：

- `repair chance`：具体道歉和补偿明显提高修复；
- `memory_reconstruction_bias`：持续行动可把旧伤向正向重构；
- `report tags`：可能生成“可通过具体行动修复”“需要长期行动证据”。

## 8. 计分与更新建议

### 8.1 初始来源

初始字段可来自三类输入：

1. 问卷：Q001-Q150 及未来 Q151-Q180；
2. 当前关系状态：满意度、未解决冲突、信任层；
3. 历史记忆：旧伤数量、修复进度、重复模式。

### 8.2 更新规则草案

```text
if negative_event and explanation_is_internal_stable_global:
  relationship_satisfaction -= high_delta
  trust_old_wound_memory += medium_delta
  memory_reconstruction_bias shifts negative

if positive_event and explanation_is_internal_stable_global:
  relationship_satisfaction += high_delta
  repair_chance += medium_delta
  positive_behavior_attribution shifts stable

if apology_specific and growth_belief high:
  repair_chance += high_delta
  old_wound_repair_progress += medium_delta

if self_action explained externally but partner_same_action explained internally:
  actor_observer_gap += medium_delta
  self_serving_bias += medium_delta
```

### 8.3 可信度

这些字段不应由单题或单次事件强行确定。

| 证据数量 | 可信度 |
| ---: | --- |
| 1 | 低，只用于弱提示 |
| 2-3 | 中，可用于事件权重 |
| 4-6 | 中高，可用于报告可见标签 |
| 7+ | 高，可用于长期画像 |

## 9. 未来 Q151-Q180 加题方向

`docs/design/23_questionnaire_dimension_coverage.md` 已建议 Q151-Q180 用于补强低覆盖维度。若加入归因、记忆与关系信念系统，可在其中插入或替换以下题目方向。

### 9.1 优先加入字段

| 字段 | 建议题型 | 题目方向 |
| --- | --- | --- |
| `positive_behavior_attribution` | `scenario_choice` | 对方主动关心你时，你更倾向认为是稳定在乎、临时补偿还是礼貌行为 |
| `negative_behavior_attribution` | `primary_with_secondary` | 对方晚回、解释不完整或冷处理时，你第一解释是什么 |
| `actor_observer_gap` | `npc_perspective` / `reverse_check` | 自己晚回与对方晚回、自己隐瞒与对方隐瞒的解释差异 |
| `self_serving_bias` | `reverse_check` | 自己犯错时看情境，对方犯错时看态度的程度 |
| `memory_reconstruction_bias` | `scenario_choice` | 新冲突发生后是否会重新理解过去小事 |
| `destiny_belief` | `slider` | 是否相信合适的人不需要太多磨合 |
| `growth_belief` | `slider` | 是否相信关系可以通过沟通和行动变好 |
| `mind_reading_expectation` | `slider` | 是否期待亲密的人不用明说也应该懂 |
| `conflict_destructive_belief` | `slider` | 是否觉得争吵意味着关系已经伤了根基 |

### 9.2 题号草案

| 题号 | 目标字段 | 题型 | 主题 |
| --- | --- | --- | --- |
| Q181 | `negative_behavior_attribution` | `primary_with_secondary` | 对方长时间不回后，你认为最可能原因是什么 |
| Q182 | `positive_behavior_attribution` | `scenario_choice` | 对方主动补偿时，你如何解释这份补偿 |
| Q183 | `actor_observer_gap` | `npc_perspective` | 自己和对方同样晚回消息时，解释是否一致 |
| Q184 | `self_serving_bias` | `reverse_check` | 自己隐瞒与对方隐瞒时，责任解释是否一致 |
| Q185 | `memory_reconstruction_bias` | `scenario_choice` | 新冲突是否会改变你对旧事件的理解 |
| Q186 | `destiny_belief`、`growth_belief` | `axis_2d` | 命中注定 vs 关系经营二维坐标 |
| Q187 | `mind_reading_expectation` | `slider` | 亲密关系中“应该自然懂我”的期待强度 |
| Q188 | `conflict_destructive_belief` | `slider` | 冲突是否意味着关系受损 |

如果必须限制在 Q151-Q180 内，可优先把 Q181-Q188 合并进 `Q173-Q180：危机模式补强`，因为这些字段直接影响冲突、旧伤和修复。

## 10. JSON 字段扩展建议

未来题库 JSON 可新增可选字段，不影响当前 MVP 必须字段。

```json
{
  "id": "Q181",
  "module_id": "attribution_memory_belief",
  "title": "晚回消息的原因解释",
  "selection_mode": "primary_with_secondary",
  "dimensions": [
    "trust_suspicion_sensitivity",
    "trust_old_wound_memory",
    "attachment_abandonment_anxiety"
  ],
  "attribution_effects": {
    "partner_not_care": {
      "locus": "internal",
      "stability": "stable",
      "scope": "global",
      "valence": "suspicious",
      "field_effects": {
        "negative_behavior_attribution": 8,
        "mind_reading_expectation": 3
      }
    },
    "partner_busy": {
      "locus": "external",
      "stability": "unstable",
      "scope": "specific",
      "valence": "neutral",
      "field_effects": {
        "negative_behavior_attribution": -5,
        "growth_belief": 2
      }
    }
  }
}
```

说明：

- `attribution_effects` 是后续扩展字段，不是当前 MVP 必须字段；
- `field_effects` 影响本文系统字段，而非 128维主表；
- 选项仍可同时影响 `dimension_effects`，用于兼容原计分系统。

## 11. 报告表达边界

报告应写：

```text
你在关系不安时，可能更容易把模糊行为理解为稳定态度变化。
你对自己的行为更容易看到情境压力，对对方同类行为则更容易要求明确解释。
你相信关系可以通过具体沟通和行动修复，因此道歉是否具体会明显影响后续感受。
```

报告不应写：

```text
你就是多疑的人。
你一定会翻旧账。
你有认知偏差。
你们注定不合适。
```

## 12. MVP 非目标

当前不做：

- Python 实现；
- 修改 `if_game/data/questionnaire_mvp.json`；
- 修改 Q001-Q150 现有题库内容；
- 接入 14 天控制台主流程；
- 调整现有 scoring 或 reporting；
- 把字段作为心理诊断或现实关系建议。

## 13. 后续实施顺序

建议后续按以下顺序推进：

1. 先在问卷题库中设计归因/信念补题，优先覆盖 `actor_observer_gap`、`self_serving_bias`、`growth_belief`；
2. 扩展 JSON schema，允许题目写入 `attribution_effects`；
3. 在行为画像中新增 `attribution_memory_belief_state`；
4. 让事件解释层先只影响报告和调试输出；
5. 再逐步接入信任层、旧伤记忆和修复机会；
6. 最后把游戏行为反向修正问卷自述归因字段。

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

## 4. 真实原因层与解释可信度系统

归因系统不能只模拟“玩家或 NPC 如何误解对方”。IF 还必须模拟：对方行为背后是否真的存在忽视、隐瞒、暧昧、背叛、操控或优先级下降。

核心原则：

1. 解释偏差不等于事实不存在。玩家怀疑可能来自焦虑，也可能是准确捕捉到了异常线索。
2. 怀疑不一定错误，信任也不一定正确。高信任可能带来稳定，也可能让角色低估真实风险。
3. 同一个可疑行为可能是误会，也可能是真实失信。系统必须同时保存事实、解释和证据，而不是只保存情绪反应。
4. “忙”不是万能解释。忙可以解释回复延迟，但不能自动解释社交媒体更新、在线互动、选择性回复、反复说法变化或删除记录。
5. 行为解释必须和可见线索进行逻辑校验。解释越模糊、线索越冲突、借口越重复，解释可信度越低。
6. 不要把玩家怀疑直接写成“焦虑”，也不要把对方异常行为全部心理学化洗白。
7. 不要把一次异常直接判定为出轨。应结合可见线索、解释一致性、旧记录、重复模式和后续补救。

真正真实的系统应接近：

```text
真实原因 × 可见线索 × 解释可信度 × 过去记忆 × 关系信念 × 证据链 × 后续补救
= 关系后果
```

### 4.1 五层结构

IF 事件至少应区分五层：

| 层级 | 英文字段 | 含义 | 例子 |
| --- | --- | --- | --- |
| 事实层 | `truth layer` | 系统内部知道的真实原因和真实发生事项 | 确实在开会 / 正在和暧昧对象聊天 |
| 意图层 | `intention layer` | 行为背后的动机和主观意图 | 忘记回复 / 故意冷处理 / 想保留解释空间 |
| 可见行为层 | `observable behavior` | 玩家或 NPC 能看到的外部线索 | 在线、点赞、朋友圈更新、删除记录 |
| 解释层 | `interpretation layer` | 当事人给出的说法和对方的理解 | “没看手机” / “你就是不在乎” |
| 证据层 | `evidence layer` | 支持或反驳解释的证据链 | 共同好友、付款记录、位置、截图、通话记录 |

同一事件必须允许以下组合同时存在：

```text
truth_type: concealment
observable_behavior:
  social_media_updated_but_no_reply: true
explanation_claim: "没看手机"
interpretation_layer: "对方可能在敷衍"
evidence_chain_strength: medium
```

这意味着系统既能模拟误会，也能模拟真实失信。

### 4.2 真实原因层字段

| 字段 | 类型 | 含义 | 示例 |
| --- | --- | --- | --- |
| `truth_type` | enum | 行为真实类型 | `busy`、`neglect`、`avoidance`、`concealment`、`betrayal`、`manipulation` |
| `truth_reason` | string/enum | 真实原因的具体说明 | 工作会议、情绪过载、怕冲突、和前任联系 |
| `truth_intention` | enum | 主观意图 | 无意延迟、回避沟通、保留秘密、试探对方、操控情绪 |
| `truth_harm_level` | 0-100/level | 真实行为造成关系伤害的程度 | 低：临时忙；高：持续欺骗 |
| `truth_priority_signal` | 0-100/level | 该行为是否体现优先级下降 | 在线但只不回伴侣时升高 |
| `truth_moral_severity` | 0-100/level | 道德严重度 | 普通疏忽低，隐瞒暧昧高，背叛最高 |

`truth_type` 建议起步枚举：

| `truth_type` | 含义 | 常见事件 |
| --- | --- | --- |
| `busy` | 真实外部事务占用 | 工作、家庭、突发事项 |
| `neglect` | 没有恶意但确实低优先级 | 看到了但觉得晚点回也无所谓 |
| `avoidance` | 为避开压力、冲突或亲密而退开 | 冷处理、拖延解释 |
| `concealment` | 有意识保留关键信息 | 异性饭局不说、神秘电话模糊 |
| `betrayal` | 真实越过忠诚或边界 | 暧昧、前任复联、关系替代 |
| `manipulation` | 有策略地制造不安或控制 | 故意不回、冷淡惩罚、测试对方 |

### 4.3 解释层字段

| 字段 | 类型 | 含义 | 高风险表现 |
| --- | --- | --- | --- |
| `explanation_claim` | string/enum | 对方给出的说法 | “没看手机”“妈妈打电话”“普通同事” |
| `explanation_specificity` | 0-100 | 解释是否具体 | 时间、地点、对象、原因都模糊时低 |
| `explanation_consistency` | 0-100 | 前后说法是否一致 | 一会儿说工作，一会儿说家人时下降 |
| `explanation_plausibility` | 0-100 | 解释本身是否符合上下文常识 | 半夜 3 点“妈妈打电话”基础可信度较低 |
| `behavior_explanation_gap` | 0-100 | 可见行为和解释之间的差距 | 说没看手机，但有点赞、在线、群聊发言 |
| `excuse_repetition_count` | integer | 同类借口重复次数 | 每次都说忙、家人、手机没电 |

解释可信度建议：

```text
explanation_credibility =
  explanation_specificity
  + explanation_consistency
  + explanation_plausibility
  + supporting_evidence
  - behavior_explanation_gap
  - excuse_repetition_penalty
```

如果对方声称“没看手机”，但同时出现社交媒体更新、在线、点赞、群聊发言，则 `behavior_explanation_gap` 上升，`explanation_plausibility` 和整体解释可信度下降。

如果半夜 3 点声称“妈妈打电话”，不能写死绝不可能。特殊背景可以提高可信度，例如母亲生病、跨时区、家庭突发事件、能提供一致细节。但在没有背景、细节模糊、反复出现或删除记录时，基础 `explanation_plausibility` 应较低。

反复出现同类借口时：

```text
excuse_repetition_count += 1
behavior_explanation_gap += repeated_excuse_delta
trust_old_wound_memory += repeated_pattern_delta
```

### 4.4 可见线索字段

| 字段 | 含义 | 对解释可信度的影响 |
| --- | --- | --- |
| `online_but_no_reply` | 在线但未回复 | 不直接判定失信，但提高选择性可用可能 |
| `social_media_updated_but_no_reply` | 更新社媒但未回复 | “没看手机”可信度下降 |
| `message_seen_but_ignored` | 已读但不回 | 优先级下降、回避或操控可能上升 |
| `selective_availability` | 对别人可用，对伴侣不可用 | `truth_priority_signal` 上升 |
| `late_night_implausible_call` | 深夜异常电话 | 需要背景和证据支持 |
| `explanation_timing_conflict` | 解释时间线冲突 | 事实信任下降 |
| `deleted_chat_trace` | 删除聊天痕迹 | 证据链增强，解释可信度下降 |
| `third_party_witness` | 第三方目击或传话 | 证据强度上升 |
| `payment_or_location_trace` | 付款、定位、照片等轨迹 | 可直接校验事实层 |

可见线索不等于最终事实，但必须参与逻辑校验。系统不能在有明显冲突线索时仍把“忙”作为默认洗白解释。

### 4.5 证据与校准字段

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `evidence_chain_strength` | 0-100/level | 当前证据链强度 |
| `exposure_risk` | 0-100/level | 真相未来暴露概率 |
| `interpretation_accuracy` | enum/score | 本次判断和事实是否匹配 |
| `trust_calibration` | 0-100/level | 信任和怀疑是否校准到事实 |
| `suspicion_accuracy_history` | list/score | 过去怀疑命中的历史 |
| `misplaced_trust_history` | list/score | 过去相信但后来发现有问题的历史 |
| `accurate_alertness_tag` | bool/tag | 准确警觉标签 |
| `over_suspicion_tag` | bool/tag | 过度怀疑标签 |
| `selective_blindness_tag` | bool/tag | 选择性失明标签 |

### 4.6 判断 × 事实四象限

| 判断 | 事实 | 类型 | 游戏后果 |
| --- | --- | --- | --- |
| 怀疑有问题 | 真的有问题 | 准确警觉 | 可以触发证据链和事实揭露 |
| 怀疑有问题 | 实际没问题 | 误会/焦虑 | 损害隐私信任和情绪安全 |
| 相信没问题 | 实际没问题 | 稳定信任 | 关系稳定或轻微波动 |
| 相信没问题 | 真的有问题 | 被欺骗/低估风险 | 后续揭穿时伤害更大 |

该表用于避免两个错误：

- 把所有怀疑都写成焦虑；
- 把所有信任都写成成熟。

成熟的关系系统应该能识别“准确警觉”和“低估风险”。

### 4.7 对关系系统的影响

| 影响对象 | 作用规则 |
| --- | --- |
| `fact_trust` / 事实信任 | 解释不一致、证据冲突、删除记录、半真半假会降低事实信任 |
| `loyalty_trust` / 忠诚信任 | 异性饭局、前任、暧昧对象、选择性隐瞒会影响忠诚信任 |
| `emotional_trust` / 情感信任 | 忽视、低优先级、故意冷处理会影响“对方是否在乎我” |
| `priority_feeling` / 被重视感 | 在线不回、已读不回、对别人可用会降低被重视感 |
| `old_wound_memory` / 旧伤记忆 | 重复借口、同类失信、后续揭穿会写入长期伤口 |
| `relationship_satisfaction` / 关系满意度 | 真实伤害、解释可信度和归因模式共同决定满意度变化 |
| `conflict_escalation` / 冲突升级 | 证据冲突、解释变化、旧伤激活会提高升级风险 |
| `repair_chance` / 修复机会 | 真实伤害低、解释一致、补偿具体、后续行为稳定时提高 |
| `lie_evidence_chain` / 谎言证据链 | 删除记录、第三方目击、付款定位、说法冲突会增强证据链 |
| `report_tags` / 报告标签 | 由多次判断校准生成，不由单次怀疑生成 |
| `npc_reaction` / NPC反应 | NPC 也会根据事实层、解释层和证据层决定是否相信玩家 |

### 4.8 现实事件例子

#### 4.8.1 晚回消息

同样是“4 小时没回”，不同 `truth_type` 的关系含义完全不同。

| `truth_type` | 真实原因 | 关系影响 |
| --- | --- | --- |
| `busy` | 真实工作、家庭或突发事务 | 若后续说明具体，信任小幅波动；若长期不提前说明，仍会降低被重视感 |
| `neglect` | 看到了但觉得不急，伴侣优先级较低 | `priority_feeling` 和 `emotional_trust` 下降 |
| `avoidance` | 不想面对冲突或亲密压力 | 冲突未解决、行动信任下降，旧伤可能激活 |
| `concealment` | 正在做不想说明的事 | 事实信任下降，证据链开始形成 |
| `betrayal` | 与前任、暧昧对象或替代关系有关 | 忠诚信任明显下降，揭穿后伤害高 |
| `manipulation` | 故意不回以制造不安或惩罚 | 情感信任和安全感下降，操控标签上升 |

系统不能只问“玩家是否焦虑”，还要判断真实原因和可见线索是否支持该焦虑。

#### 4.8.2 社交媒体更新但不回消息

事实：

```text
observable_behavior:
  social_media_updated_but_no_reply: true
  online_but_no_reply: true
explanation_claim: "没看手机"
```

处理：

- 不直接判定出轨；
- 但“没看手机”的解释可信度下降；
- `selective_availability` 上升；
- `truth_priority_signal` 上升；
- 如果反复出现，则 `excuse_repetition_count` 和 `behavior_explanation_gap` 增加；
- 对关系的主要影响是 `priority_feeling`、`emotional_trust` 和 `fact_trust`。

报告不应写“你太焦虑”，而应写：

```text
你对“对方明明在线却不回应”的优先级信号比较敏感。这个敏感不一定错误，系统会结合后续解释一致性和重复模式继续校准。
```

#### 4.8.3 半夜异常电话

事实：

```text
observable_behavior:
  late_night_implausible_call: true
time: 03:00
explanation_claim: "妈妈打电话"
```

处理原则：

- 不能绝对判假。家庭急事、跨时区、疾病、突发事故都可能成立；
- 基础 `explanation_plausibility` 较低，因为时间和常见生活规律冲突；
- 如果有特殊背景、细节一致、后续可验证，可信度上升；
- 如果无细节、反复出现、解释变化、删除记录，`evidence_chain_strength` 上升；
- 若第三方证据或通话记录支持解释，则怀疑可能转为误会。

#### 4.8.4 异性饭局

两种分支：

| 情况 | 事实信任 | 忠诚信任 | 修复机会 |
| --- | --- | --- | --- |
| 提前说明、边界清楚、事后解释一致 | 基本稳定 | 基本稳定或轻微波动 | 高 |
| 临时隐瞒、说法模糊、被共同好友撞见 | 明显下降 | 视饭局对象和上下文下降 | 取决于是否承认省略重点 |

关键不是“异性饭局一定有问题”，而是：

- 是否提前说明；
- 是否一对一；
- 是否有暧昧历史；
- 是否省略关键事实；
- 是否被第三方撞见后才补充；
- 后续边界协议是否清楚。

#### 4.8.5 神秘电话

| `truth_type` | 真实情况 | 解释可信度处理 |
| --- | --- | --- |
| `busy` / family_emergency | 真实家人急事 | 需要细节一致和背景支持；支持后可恢复事实信任 |
| `busy` / work_call | 普通工作电话 | 若职业/时间合理，可信度中高 |
| `concealment` | 前任或暧昧对象来电但不想说 | 事实信任下降，证据链增强 |
| `betrayal` | 与越界关系有关 | 忠诚信任下降，后续揭穿伤害高 |
| `manipulation` / fabricated_excuse | 临时编造借口转移视线 | 解释一致性低，事实信任快速下降 |

系统应允许“神秘电话只是普通电话”，也应允许它是真实隐瞒入口。

#### 4.8.6 主动道歉和补偿

| 类型 | 识别依据 | 系统影响 |
| --- | --- | --- |
| 真诚修复 | 承认具体事实，解释一致，有后续行动 | `repair_chance` 上升，旧伤修复进度增加 |
| 心虚补偿 | 补偿强但解释含糊，回避关键事实 | 短期满意度上升，事实信任仍不稳定 |
| 表演式道歉 | 话术漂亮但不承担具体责任 | 修复机会有限，重复后伤害更大 |
| 只想快速翻篇 | 催促对方别再提，缺少补救 | 冲突未解决，旧伤记忆上升 |

判断道歉不能只看“是否道歉”，要结合：

- `truth_harm_level`；
- `explanation_consistency`；
- `truth_moral_severity`；
- 后续行为是否改变；
- 是否继续使用同类借口。

### 4.9 报告标签示例

| 标签 | 含义 | 生成原则 |
| --- | --- | --- |
| `accurate_alertness` | 准确警觉型 | 多次怀疑与事实问题匹配 |
| `over_suspicion` | 过度怀疑型 | 多次怀疑但事实无问题，并造成关系损耗 |
| `misplaced_trust` | 低估风险型 | 多次相信无问题，但后续证据显示有问题 |
| `selective_blindness` | 选择性失明型 | 可见线索明显冲突，但持续忽略 |
| `evidence_sensitive` | 证据敏感型 | 会根据可见线索调整判断 |
| `priority_neglect_sensitive` | 优先级忽视敏感型 | 对在线不回、已读不回、选择性可用敏感 |
| `repeated_excuse_alert` | 重复借口警觉 | 对同类借口反复出现敏感 |
| `plausible_explanation_acceptor` | 合理解释接受型 | 解释具体、一致、有证据时愿意缓和 |

这些标签必须由多次事件或问卷 + 行为共同支持，不应由单次异常生成。

### 4.10 问卷字段与隐藏系统字段

适合加入 Q151-Q180 或后续补题的字段：

| 字段 | 原因 |
| --- | --- |
| `trust_calibration` | 可通过情境题测试“该怀疑时是否怀疑，该信任时是否信任” |
| `suspicion_accuracy_history` | 可通过自述过去经验和场景题测量 |
| `evidence_sensitive` | 可测量玩家是否根据证据调整判断 |
| `repeated_excuse_alert` | 可测量对重复借口的敏感度 |
| `priority_neglect_sensitive` | 可测量对优先级下降线索的反应 |
| `plausible_explanation_acceptor` | 可测量是否接受具体、一致、可验证解释 |

只适合隐藏系统的字段：

| 字段 | 原因 |
| --- | --- |
| `truth_type` | 玩家不应在问卷中知道事件真实答案 |
| `truth_reason` | 属于系统内部事实 |
| `truth_intention` | 属于 NPC 或事件真实动机 |
| `truth_harm_level` | 需要由事件事实和后果计算 |
| `evidence_chain_strength` | 来自动态线索，不适合静态自述 |
| `interpretation_accuracy` | 必须对比判断和真实事实后才能计算 |
| `exposure_risk` | 谎言和证据系统内部使用 |

### 4.11 与谎言证据链的关系

如果未来新增 `docs/design/21_lie_evidence_memory_system.md`，本文字段应与谎言证据链共享以下结构：

```text
lie_evidence_chain:
  truth_type: concealment
  explanation_claim: "普通同事电话"
  omitted_parts:
    - 前任
    - 深夜
  observable_traces:
    - deleted_chat_trace
    - late_night_implausible_call
  evidence_chain_strength: medium_high
  exposure_risk: high
```

谎言证据链负责“证据如何累积和暴露”，解释可信度系统负责“角色如何根据证据校准信任和怀疑”。

### 4.12 报告表达边界补充

报告应避免：

```text
你只是焦虑。
对方只是忙。
你一定被背叛了。
你太多疑，所以才觉得对方异常。
```

报告应写：

```text
你对解释和可见行为不一致的情况比较敏感。这个敏感可能帮助你识别真实风险，也可能在证据不足时放大误会，系统会根据后续事实和证据链继续校准。
```

## 5. 字段草案

### 5.1 顶层结构

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

### 5.2 字段定义

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

### 5.3 归因枚举建议

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

## 6. 与现有维度的映射

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

## 7. 影响范围

### 7.1 event interpretation

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

### 7.2 relationship satisfaction

满意度不只受行为影响，也受解释影响。

| 归因模式 | 积极行为影响 | 消极行为影响 |
| --- | --- | --- |
| 幸福型归因 | 积极行为更能提高满意度 | 消极行为损耗较小，保留修复空间 |
| 痛苦型归因 | 积极行为被视为偶然，提升有限 | 消极行为被放大，满意度下降明显 |
| 自利归因高 | 自己行为对满意度损耗小，对方行为损耗大 | 容易形成“我有理由，你没理由”的关系叙事 |

### 7.3 trust layers

归因应作用于多层信任，而不是只改一个总信任值。

| 事件解释 | 主要影响信任层 |
| --- | --- |
| “他不回是忙” | 情感信任小幅下降或不变 |
| “他不回是不在乎” | 情感信任下降 |
| “他隐瞒异性饭局说明不诚实” | 事实信任、忠诚信任下降 |
| “他答应补偿但没做到” | 行动信任下降 |
| “他查我手机是因为不相信我” | 隐私信任下降 |
| “出事时他会逃” | 危机信任下降 |

### 7.4 old wound memory

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

### 7.5 conflict escalation

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

### 7.6 repair chance

修复机会不是只看道歉本身，还要看对方如何解释道歉。

| 条件 | 修复机会 |
| --- | --- |
| 高 `growth_belief` + 道歉具体 + 行动补偿 | 明显提高 |
| 高 `destiny_belief` + 把冲突视为“不合适” | 道歉效果下降 |
| 高 `negative_behavior_attribution` + 旧伤多次激活 | 修复需要更长行动证据 |
| 高 `self_serving_bias` | 自己道歉容易形式化，对方道歉更容易被挑错 |

### 7.7 report tags

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

## 8. 事件例子

### 8.1 晚回消息

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

### 8.2 神秘电话

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

### 8.3 异性饭局

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

### 8.4 争吵后冷处理

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

### 8.5 主动道歉和补偿

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

## 9. 计分与更新建议

### 9.1 初始来源

初始字段可来自三类输入：

1. 问卷：Q001-Q150 及未来 Q151-Q180；
2. 当前关系状态：满意度、未解决冲突、信任层；
3. 历史记忆：旧伤数量、修复进度、重复模式。

### 9.2 更新规则草案

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

### 9.3 可信度

这些字段不应由单题或单次事件强行确定。

| 证据数量 | 可信度 |
| ---: | --- |
| 1 | 低，只用于弱提示 |
| 2-3 | 中，可用于事件权重 |
| 4-6 | 中高，可用于报告可见标签 |
| 7+ | 高，可用于长期画像 |

## 10. 未来 Q151-Q180 加题方向

`docs/design/23_questionnaire_dimension_coverage.md` 已建议 Q151-Q180 用于补强低覆盖维度。若加入归因、记忆与关系信念系统，可在其中插入或替换以下题目方向。

### 10.1 优先加入字段

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

### 10.2 题号草案

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

## 11. JSON 字段扩展建议

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

## 12. 报告表达边界

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

## 13. MVP 非目标

当前不做：

- Python 实现；
- 修改 `if_game/data/questionnaire_mvp.json`；
- 修改 Q001-Q150 现有题库内容；
- 接入 14 天控制台主流程；
- 调整现有 scoring 或 reporting；
- 把字段作为心理诊断或现实关系建议。

## 14. 后续实施顺序

建议后续按以下顺序推进：

1. 先在问卷题库中设计归因/信念补题，优先覆盖 `actor_observer_gap`、`self_serving_bias`、`growth_belief`；
2. 扩展 JSON schema，允许题目写入 `attribution_effects`；
3. 在行为画像中新增 `attribution_memory_belief_state`；
4. 让事件解释层先只影响报告和调试输出；
5. 再逐步接入信任层、旧伤记忆和修复机会；
6. 最后把游戏行为反向修正问卷自述归因字段。

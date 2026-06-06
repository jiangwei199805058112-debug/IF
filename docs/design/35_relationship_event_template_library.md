# 关系事件模板库

本文档用于把 `docs/design/25_attribution_memory_belief_system.md` 到 `docs/design/34_relationship_state_aggregator_implementation_plan.md` 中的系统设计转化为可写剧情、可做测试、可接入 `relationship_state_aggregator` 的事件模板库。

它不是完整剧情正文，也不是代码配置文件。它的作用是为后续 Codex 实现事件、测试和报告输出提供统一事件母版。

核心原则：

```text
每个关系事件都不应只写“发生了什么”，还要写：
真实原因是什么、玩家/NPC看见了什么、如何解释、如何沟通、是否修复、如何影响信任/满意度/亲密/稳定/旧伤。
```

---

## 1. 事件模板总结构

后续所有关键关系事件建议按以下结构整理：

```text
event_id:
event_title:
source_system:
scene:
truth_variants:
observable_traces:
player_interpretations:
npc_interpretations:
communication_options:
possible_responses:
aggregator_inputs:
expected_state_delta:
report_tags:
memory_write_rules:
not_do:
```

### 1.1 字段说明

| 字段 | 含义 |
| --- | --- |
| `event_id` | 事件唯一 ID |
| `event_title` | 玩家可读标题 |
| `source_system` | 来源系统，如 attribution、disclosure、conflict、exchange、equity |
| `scene` | 场景描述 |
| `truth_variants` | 真实原因分支，不同真相导致不同解释结果 |
| `observable_traces` | 玩家/NPC 能看见的线索 |
| `player_interpretations` | 玩家可能如何理解 |
| `npc_interpretations` | NPC 可能如何理解 |
| `communication_options` | 玩家可选表达方式 |
| `possible_responses` | NPC 或系统可能回应 |
| `aggregator_inputs` | 建议传入 `relationship_state_aggregator` 的字段 |
| `expected_state_delta` | 预期影响方向 |
| `report_tags` | 可能生成的报告标签 |
| `memory_write_rules` | 是否写入旧伤、修复记忆或长期信念 |
| `not_do` | 实现时禁止的简化或误判 |

---

## 2. 认知误读事件

来源系统：

```text
docs/design/25_attribution_memory_belief_system.md
docs/design/26_partner_perception_and_impression_system.md
docs/design/31_system_integration_consistency_rules.md
```

### E-COG-01：晚回消息

```text
event_id: E-COG-01
event_title: 晚回消息
source_system: attribution / partner_perception
```

#### 场景

对方 4 小时没有回复你的消息，但期间手机状态或社交平台有一些模糊线索。

#### 真实原因分支

| truth_type | 说明 |
| --- | --- |
| `busy` | 真的在忙，未及时处理私人消息 |
| `avoidance` | 看到了，但不想面对这段对话 |
| `neglect` | 对玩家优先级下降 |
| `concealment` | 正在处理不想让玩家知道的人或事 |
| `phone_unavailable` | 手机没电、开会、客观不可用 |

#### 可见线索

```text
online_but_no_reply
social_media_updated_but_no_reply
message_seen_but_ignored
selective_availability
explanation_timing_conflict
```

#### 玩家解释

- “他/她应该只是忙。”
- “他/她对别人有空，对我没空。”
- “他/她在故意冷淡我。”
- “我是不是太敏感了？”
- “这和之前那次一样，又开始回避了。”

#### aggregator 输入重点

```text
truth_harm_level
deception_level
evidence_chain_strength
interpretation_accuracy
threat_bias_effect
selective_blindness_effect
```

#### 预期影响

| 情况 | 影响 |
| --- | --- |
| 真实忙 + 证据弱 + 玩家信任 | 轻微或无影响 |
| 真实忙 + 玩家高威胁扫描 | 满意度小降，信任不应大扣 |
| 真实回避 + 证据强 | 信任和安全感下降 |
| 真实隐瞒 + 解释前后不一致 | 信任明显下降，可能写旧伤 |

#### 禁止误判

```text
晚回 = 不爱
在线 = 一定故意不回
怀疑 = 一定焦虑
信任 = 一定成熟
```

---

### E-COG-02：见面越来越随便

```text
event_id: E-COG-02
event_title: 见面越来越随便
source_system: partner_perception / impression_management
```

#### 场景

关系稳定后，对方见你时不再像暧昧期那样精心准备，穿着、语气、仪式感都变得更随意。

#### 真实原因分支

| truth_type | 说明 |
| --- | --- |
| `comfort` | 关系稳定后更放松 |
| `stress` | 最近压力大，没有精力经营形象 |
| `effort_decay` | 关系经营投入下降 |
| `taken_for_granted` | 觉得玩家不会离开，因此减少投入 |
| `selective_effort` | 对外界或其他人仍高投入，对玩家低投入 |

#### 玩家解释

- “这是关系稳定后的真实和放松。”
- “他/她不重视我了。”
- “是不是不爱了？”
- “他/她是不是把精力给别人了？”
- “也许我期待太高。”

#### aggregator 输入重点

```text
relationship_rewards_delta
relationship_costs_delta
approach_reward_delta
avoidance_cost_pressure_delta
felt_appreciation_delta
taken_for_granted_delta
```

#### 预期影响

| 情况 | 影响 |
| --- | --- |
| 放松 + 玩家能正向理解 | 安全感上升，刺激感小降 |
| 压力导致 + 有解释和补偿 | 满意度小降后可恢复 |
| 投入衰减 + 被理所当然 | 满意度、亲密感和公平感下降 |
| 选择性投入 | 触发危险知觉和关系比较 |

#### 禁止误判

```text
随便 = 一定不爱
随便 = 一定更信任
仪式感下降 = 一定出轨
```

---

### E-COG-03：对方说“你就是这样的人”

```text
event_id: E-COG-03
event_title: 你就是这样的人
source_system: attribution / partner_model_accuracy
```

#### 场景

一次小冲突中，对方把你的具体行为上升到人格判断。

#### 真实原因分支

| truth_type | 说明 |
| --- | --- |
| `accurate_pattern` | 你确实多次重复类似行为 |
| `old_model` | 对方用旧印象理解现在的你 |
| `projection` | 对方把自己的恐惧投射到你身上 |
| `conflict_attack` | 对方情绪中用人格攻击压制你 |

#### 预期影响

- 如果确实是重复模式：触发关系信念更新；
- 如果是旧印象固化：玩家委屈，修复机会取决于对方是否愿意更新认知；
- 如果是人格攻击：旧伤记忆上升；
- 如果双方能回到具体行为：修复机会增加。

#### 禁止误判

```text
人格判断 = 一定错误
具体重复行为 = 不能被指出
指出模式 = 必然攻击
```

---

## 3. 自我表露与回应事件

来源系统：

```text
docs/design/27_communication_self_disclosure_system.md
docs/design/28_questionnaire_communication_disclosure_module.md
```

### E-DIS-01：第一次说起过去伤害

```text
event_id: E-DIS-01
event_title: 第一次说起过去伤害
source_system: self_disclosure / responsiveness
```

#### 场景

玩家向 NPC 说起一段过去让自己很难受的经历。

#### 真实内容层级

| disclosure_depth | 内容 |
| --- | --- |
| 低 | 普通不开心经历 |
| 中 | 家庭、前任或长期压力 |
| 高 | 创伤、自卑、羞耻、重大秘密 |

#### NPC 可能回应

| response_type | 说明 | 影响 |
| --- | --- | --- |
| `attentive_validation` | 认真听并确认感受 | 亲密感和安全感上升 |
| `quick_comfort` | 安慰但很快转移话题 | 小幅失落 |
| `problem_solving_only` | 直接给方案，忽略情绪 | 视玩家需求而定 |
| `dismissive` | “你想太多了” | 表露安全感下降 |
| `mocking` | 拿脆弱开玩笑 | 高伤害，写旧伤 |
| `reciprocal_disclosure` | 也分享自己的经历 | 互惠表露上升 |

#### aggregator 输入重点

```text
self_disclosure_depth
perceived_responsiveness
emotional_validation
safe_disclosure_space_delta
old_wound_memory_delta
```

#### 禁止误判

```text
说了秘密 = 一定加亲密
对方沉默 = 一定石墙
给建议 = 一定无效
```

---

### E-DIS-02：一方说很多，另一方很少说

```text
event_id: E-DIS-02
event_title: 表露互惠失衡
source_system: self_disclosure / reciprocity
```

#### 场景

玩家在关系中说了很多私人内容，但 NPC 始终很少表露自己。

#### 真实原因分支

| truth_type | 说明 |
| --- | --- |
| `slow_pacing` | NPC 只是节奏慢 |
| `privacy_boundary` | NPC 隐私边界强 |
| `low_trust` | NPC 尚未足够信任玩家 |
| `concealment` | NPC 确实有重要事实不想说 |
| `avoidant_style` | NPC 习惯回避深层暴露 |

#### 预期影响

- 对高互惠需求玩家：满意度和安全感下降；
- 对高隐私尊重玩家：影响较小；
- 若有隐瞒证据：转入解释可信度系统；
- 若 NPC 后续主动解释边界：修复机会增加。

---

### E-DIS-03：说“我爱你”后对方沉默

```text
event_id: E-DIS-03
event_title: 爱意表达后的沉默
source_system: affection_expression / responsiveness
```

#### 真实原因分支

| truth_type | 说明 |
| --- | --- |
| `not_ready` | 对方还没准备好说 |
| `low_verbal_affection` | 对方不习惯语言表达 |
| `commitment_fear` | 对方害怕承诺 |
| `low_investment` | 对方投入不足 |
| `processing` | 对方需要时间处理情绪 |

#### 预期影响

- 对高语言爱意需求玩家：安全感下降；
- 若对方之后用行动补足：影响可修复；
- 若长期回避承诺：满意度和稳定性下降；
- 不应一次沉默直接判定“不爱”。

---

## 4. 秘密与隐私事件

来源系统：

```text
docs/design/25_attribution_memory_belief_system.md
docs/design/27_communication_self_disclosure_system.md
docs/design/31_system_integration_consistency_rules.md
```

### E-SEC-01：对方不愿谈前任

```text
event_id: E-SEC-01
event_title: 不愿谈前任
source_system: privacy_boundary / taboo_topic
```

#### 真实原因分支

| truth_type | 说明 |
| --- | --- |
| `privacy_boundary` | 认为过去细节属于隐私 |
| `not_ready` | 还没准备好谈 |
| `protect_partner` | 怕玩家比较或受伤 |
| `unresolved_attachment` | 确实还没放下 |
| `concealment` | 隐瞒当前仍有联系 |

#### 可见线索

```text
explanation_consistency
current_contact_trace
avoidance_repetition
phone_privacy_shift
third_party_witness
```

#### aggregator 输入重点

```text
privacy_boundary_conflict
secret_damage_level
deception_level
evidence_chain_strength
trust_delta
intimacy_delta
```

#### 禁止误判

```text
不谈前任 = 一定有鬼
追问前任 = 一定关心
隐私边界 = 欺骗
```

---

### E-SEC-02：被发现还有小号

```text
event_id: E-SEC-02
event_title: 被发现还有小号
source_system: deception / evidence_chain
```

#### 真实原因分支

| truth_type | 说明 |
| --- | --- |
| `private_space` | 小号只是私人空间 |
| `avoid_conflict` | 害怕某些内容引发争吵 |
| `concealment` | 隐藏暧昧或边界内容 |
| `betrayal` | 存在现实背叛证据 |
| `identity_split` | 维持两套身份或关系圈 |

#### 预期影响

- 如果只是私人空间：主要是边界协商；
- 如果解释不一致或删除证据：信任下降；
- 如果涉及暧昧/背叛：高信任损伤；
- 若玩家直接偷看：玩家自身边界问题也应记录。

---

### E-SEC-03：删除聊天记录

```text
event_id: E-SEC-03
event_title: 删除聊天记录
source_system: evidence_chain / deception
```

#### 真实原因分支

| truth_type | 说明 |
| --- | --- |
| `habit_cleanup` | 习惯清理，无特殊内容 |
| `privacy_boundary` | 不希望任何聊天被查看 |
| `avoid_conflict` | 怕玩家误会 |
| `concealment` | 隐藏边界模糊内容 |
| `betrayal` | 隐藏背叛证据 |

#### aggregator 输入重点

```text
deleted_or_hidden_trace = true
evidence_chain_strength
explanation_consistency
deception_level
truth_harm_level
```

#### 禁止误判

```text
删除记录 = 一定背叛
没删记录 = 一定清白
查看记录 = 一定合理
```

---

## 5. 冲突修复事件

来源系统：

```text
docs/design/29_conflict_communication_repair_system.md
```

### E-CON-01：对方抱怨你迟到

```text
event_id: E-CON-01
event_title: 迟到抱怨
source_system: conflict_repair
```

#### 玩家回应选项

| option | 类型 | 影响 |
| --- | --- | --- |
| “我知道你等很久了，对不起，我下次提前出门。” | 承认 + 修复 | 信任和修复机会提升 |
| “堵车又不是我想的。” | 防卫 | 修复机会下降 |
| “你上次不也迟到？” | 反向抱怨 | 冲突升级 |
| “别小题大做。” | 否定感受 | 旧伤上升 |
| 沉默不说话 | 视情境判断 | 可能是处理，也可能是石墙 |

#### aggregator 输入重点

```text
validation_skill
repair_attempt_quality
defensive_response
cross_complaining
contempt_signal
stonewalling_level
```

---

### E-CON-02：玩家请求暂停争吵

```text
event_id: E-CON-02
event_title: 暂停争吵
source_system: conflict_timeout
```

#### 有效暂停条件

```text
说明自己需要冷静
说明不是逃避
给出回来继续谈的时间或条件
之后真的回来处理问题
```

#### 预期影响

| 情况 | 影响 |
| --- | --- |
| 有效暂停 | 降低冲突升级，提高修复机会 |
| 暂停后消失 | 接近石墙，降低信任 |
| 用暂停惩罚对方 | 冷处理风险上升 |
| 不暂停继续攻击 | 冲突升级 |

#### 禁止误判

```text
暂停 = 冷暴力
继续吵 = 真诚
沉默 = 一定有害
```

---

### E-CON-03：一方用嘲讽回应脆弱表达

```text
event_id: E-CON-03
event_title: 嘲讽脆弱表达
source_system: contempt / old_wound
```

#### 场景

玩家说出一件难过的事，对方用玩笑、讥讽或轻视回应。

#### 影响

```text
old_wound_memory_delta 高
safe_disclosure_space_delta 下降
intimacy_delta 下降
trust_delta 下降
report_tags: contempt_risk / disclosure_regret / low_responsiveness
```

#### 禁止误判

```text
只是开玩笑 = 无伤害
脆弱表达被攻击 = 普通冲突
```

---

## 6. 社会交换与依赖事件

来源系统：

```text
docs/design/30_social_exchange_dependency_system.md
docs/design/32_approach_avoidance_turbulence_system.md
```

### E-EXC-01：关系不错，但总觉得不够

```text
event_id: E-EXC-01
event_title: 关系不错但不够
source_system: comparison_level / satisfaction
```

#### 场景

对方稳定、可靠、没有严重问题，但玩家仍感觉这段关系没有达到自己期待。

#### 可能原因

| reason | 说明 |
| --- | --- |
| `high_comparison_level` | 玩家期待水平高 |
| `low_approach_reward` | 安全但缺少快乐和新鲜感 |
| `low_verbal_affection` | 对方表达不足 |
| `low_self_expansion` | 关系没有带来成长或探索 |
| `social_comparison_pressure` | 受到朋友/社媒比较影响 |

#### 预期影响

- 信任不一定下降；
- 满意度下降；
- 稳定性取决于 CLalt 和投入；
- 可通过共同新鲜体验、沟通期待、现实调整修复。

---

### E-EXC-02：遇到更有吸引力的新对象

```text
event_id: E-EXC-02
event_title: 替代对象出现
source_system: CLalt / alternative_attraction
```

#### 场景

玩家在社交场合遇到一个更有新鲜感、更理解自己或更有吸引力的人。

#### 影响因素

```text
current_relationship_satisfaction
comparison_level_alternatives
alternative_partner_attraction
relationship_investment
moral_boundary
current_conflict_level
novelty_need
```

#### 预期影响

| 当前关系状态 | 影响 |
| --- | --- |
| 高满意 + 高投入 | 轻微波动 |
| 低满意 + 高 CLalt | 离开倾向上升 |
| 安全但沉闷 | 外部新鲜感吸引强 |
| 高冲突高刺激关系 | 替代对象可能成为逃离出口 |

#### 禁止误判

```text
觉得别人有吸引力 = 已经背叛
当前满意 = 永远不会动摇
替代选择高 = 一定离开
```

---

### E-EXC-03：不幸福但难以分开

```text
event_id: E-EXC-03
event_title: 不幸福但难以分开
source_system: dependence / investment / leaving_cost
```

#### 场景

双方长期不满意，但共同住所、朋友圈、家庭、经济和投入损失让关系继续维持。

#### aggregator 输入重点

```text
satisfaction_delta < 0
dependence_delta > 0
stability_delta 可高
relationship_investment
leaving_cost
comparison_level_alternatives
```

#### 禁止误判

```text
还在一起 = 爱
不分手 = 满意
依赖高 = 亲密高
```

---

## 7. 沉闷、新鲜感与动荡事件

来源系统：

```text
docs/design/32_approach_avoidance_turbulence_system.md
```

### E-TUR-01：安全但沉闷

```text
event_id: E-TUR-01
event_title: 安全但沉闷
source_system: approach_avoidance / boredom
```

#### 场景

关系几乎没有大冲突，但双方越来越像室友，缺少新鲜体验、共同成长和主动亲密。

#### aggregator 输入重点

```text
avoidance_cost_pressure_delta 下降
approach_reward_delta 低
boredom_delta 上升
relationship_safety_delta 上升或稳定
excitement_delta 下降
```

#### 预期影响

- 安全感不一定低；
- 满意度可能缓慢下降；
- 替代新鲜感吸引上升；
- 通过共同新体验可修复。

---

### E-TUR-02：高刺激高风险关系

```text
event_id: E-TUR-02
event_title: 高刺激高风险
source_system: approach_avoidance / volatility
```

#### 场景

双方强烈吸引、亲密和激情很高，但争吵、怀疑、冷淡和复合也频繁出现。

#### 预期影响

```text
excitement_delta 高
intimacy_delta 波动高
safety_delta 低
stability_delta 低或波动
old_wound_memory_delta 可能累积
report_tags: risk_excitement_pattern
```

#### 禁止误判

```text
激情强 = 关系健康
冲突多 = 一定该结束
高风险 = 没有真实吸引
```

---

### E-TUR-03：关系转正式后的动荡

```text
event_id: E-TUR-03
event_title: 从暧昧转正式后的动荡
source_system: relationship_turbulence
```

#### 场景

关系从暧昧/约会进入正式伴侣阶段后，时间安排、朋友关系、个人空间和未来期待突然需要协调。

#### 可能冲突

- 一方期待更多陪伴；
- 一方想保留个人时间；
- 朋友抱怨玩家消失太久；
- 周末安排不一致；
- 对未来承诺节奏不一致。

#### 预期影响

- 动荡不一定代表失败；
- 如果能协商规则，长期稳定性上升；
- 如果一方控制或回避，满意度下降；
- 可写为关系阶段转换事件。

---

## 8. 共有、交换与公平事件

来源系统：

```text
docs/design/33_communal_exchange_equity_system.md
```

### E-EQU-01：家务和生活安排不公平

```text
event_id: E-EQU-01
event_title: 家务和生活安排不公平
source_system: equity / household_labor
```

#### 场景

同居或长期相处后，玩家发现自己总是在收拾、提醒、安排、照顾细节，对方习以为常。

#### 真实结构

| factor | 说明 |
| --- | --- |
| `actual_contribution_gap` | 实际贡献差异 |
| `felt_appreciation` | 对方是否看见和感谢 |
| `taken_for_granted` | 是否被理所当然对待 |
| `household_equity_sensitivity` | 玩家对家务公平的敏感度 |
| `repair_action` | 是否重新分工或补偿 |

#### 预期影响

```text
perceived_equity_delta 下降
underbenefit_feeling_delta 上升
satisfaction_delta 下降
old_wound_memory_delta 视长期重复程度上升
```

#### 禁止误判

```text
家务是小事
五五分才公平
做得多就是活该
```

---

### E-EQU-02：短期多承担，对方低谷

```text
event_id: E-EQU-02
event_title: 对方低谷时短期多承担
source_system: communal_care / delayed_reciprocity
```

#### 场景

NPC 最近压力很大，玩家短期承担更多照顾、家务或情绪支持。

#### 预期影响

| 条件 | 影响 |
| --- | --- |
| 对方看见并感谢 | 共有感和亲密感上升 |
| 对方低谷后回流 | 长期公平稳定 |
| 对方长期理所当然 | 获益不足和怨恨上升 |
| 玩家本就高公平敏感 | 更需要明确感谢和修复 |

#### 禁止误判

```text
短期不对等 = 不公平
照顾对方 = 牺牲自己
共有关系 = 无限付出
```

---

### E-EQU-03：开始记账

```text
event_id: E-EQU-03
event_title: 开始在心里记账
source_system: exchange_shift_under_stress
```

#### 场景

玩家开始频繁想到“我为你做了这么多，你为我做了什么？”

#### 可能原因

- 长期付出未被看见；
- 对方只在有需要时靠近；
- 玩家高交换倾向；
- 共有关系在压力下转为交换记账；
- 旧伤记忆被触发。

#### 预期影响

```text
scorekeeping_tendency 上升
communal_strength 下降
satisfaction_delta 下降
repair_chance 取决于双方能否重新表达感谢和分工
```

---

## 9. 聚合器测试专用事件

这些事件可直接用于后续 `relationship_state_aggregator_test.py`。

### T-AGG-01：隐私边界冲突但没有欺骗

```text
truth_harm_level: low
deception_level: 0
privacy_boundary_conflict: high
evidence_chain_strength: low
```

预期：

```text
trust_delta 不应大幅下降
satisfaction_delta 或 intimacy_delta 可小幅下降
report_tags 包含 privacy_boundary_conflict
```

---

### T-AGG-02：准确警觉而不是疑心病

```text
truth_harm_level: high
evidence_chain_strength: high
interpretation_accuracy: accurate_alertness
```

预期：

```text
report_tags 包含 accurate_alertness
不出现 over_suspicion_pattern
trust_delta 由真实伤害主导下降
```

---

### T-AGG-03：有效暂停不是石墙

```text
stonewalling_level: 0
timeout_repair_success: true
repair_attempt_quality: high
```

预期：

```text
repair_chance_delta > 0
old_wound_memory_delta <= 0
不出现 stonewalling_pattern
```

---

### T-AGG-04：安全但沉闷

```text
avoidance_cost_pressure_delta: negative
approach_reward_delta: low
boredom_delta: high
```

预期：

```text
safety_delta >= 0
excitement_delta 不自动上升
report_tags 可包含 safe_but_bored_pattern
```

---

### T-AGG-05：同一欺骗事件不能重复扣信任

```text
truth_harm_level: high
deception_level: high
evidence_chain_strength: high
conflict_escalation_risk: high
```

预期：

```text
trust_delta 有上限
真实原因层主导信任损失
冲突层只修正旧伤、修复机会和满意度
```

---

## 10. 报告标签候选汇总

| 标签 | 来源事件 |
| --- | --- |
| `accurate_alertness` | E-COG-01、T-AGG-02 |
| `confident_misreader` | E-COG-03 |
| `low_responsiveness` | E-DIS-01 |
| `disclosure_regret` | E-DIS-01、E-CON-03 |
| `privacy_boundary_conflict` | E-SEC-01、T-AGG-01 |
| `deception_risk` | E-SEC-02、E-SEC-03 |
| `stonewalling_pattern` | E-CON-02 失败分支 |
| `repair_capable` | E-CON-01、E-CON-02 成功分支 |
| `safe_but_bored_pattern` | E-TUR-01、T-AGG-04 |
| `risk_excitement_pattern` | E-TUR-02 |
| `alternative_sensitive` | E-EXC-02 |
| `investment_bound` | E-EXC-03 |
| `underbenefit_sensitive` | E-EQU-01 |
| `care_responsive` | E-EQU-02 |
| `scorekeeping_pattern` | E-EQU-03 |

---

## 11. 不做什么

本事件模板库暂不做：

1. 不写完整小说化剧情；
2. 不直接生成 JSON 配置；
3. 不要求所有事件都立刻实现；
4. 不把单一事件写成固定结局；
5. 不上传原始截图或大段原文；
6. 不接 AI API；
7. 不替代 `relationship_state_aggregator` 的测试。

---

## 12. 一句话总结

```text
本事件模板库的作用，是把 IF 已有的关系心理系统转化成可执行事件母版：
每个事件都必须同时考虑真实原因、可见线索、解释偏差、沟通回应、修复机会、关系状态变化和报告标签。
```

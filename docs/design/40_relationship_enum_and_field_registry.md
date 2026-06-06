# 关系枚举与字段注册表

本文档用于统一 IF 关系系统中的枚举值、字段名和标签 ID，避免后续代码实现时出现：

```text
同一个概念多个名字
字符串拼写不一致
事件 truth_type 无法统一处理
report_tag 无法查词典
aggregator 输入字段不稳定
RelationshipStateDelta 输出字段反复变动
```

本文件服务于：

```text
docs/design/25_attribution_memory_belief_system.md
docs/design/26_partner_perception_and_impression_system.md
docs/design/31_system_integration_consistency_rules.md
docs/design/34_relationship_state_aggregator_implementation_plan.md
docs/design/35_relationship_event_template_library.md
docs/design/37_relationship_report_tag_dictionary.md
docs/design/38_relationship_system_logic_audit_and_optimization_notes.md
```

---

## 1. 使用原则

### 1.1 代码中的枚举值应优先来自本文档

后续如果写：

```text
truth_type
observable_trace
interpretation_type
interpretation_accuracy
communication_response_type
conflict_response_type
report_tag
aggregator_input
state_delta_field
```

应优先使用本文档注册值。

### 1.2 不在事件里随手造新字符串

禁止后续配置或代码中随手写：

```text
maybe_cheating
suspicious_phone
bad_silence
love_problem
```

应先检查是否已有注册值。确实缺少时，再补本文档。

### 1.3 枚举值使用 snake_case

统一格式：

```text
lower_snake_case
```

示例：

```text
accurate_alertness
privacy_boundary_conflict
message_seen_but_ignored
```

---

## 2. 通用等级枚举

### 2.1 强度等级 `level`

用于多数强度字段。

```text
none
low
medium
high
critical
```

说明：

| 值 | 含义 |
| --- | --- |
| `none` | 没有明显影响 |
| `low` | 轻微影响 |
| `medium` | 中等影响 |
| `high` | 明显影响 |
| `critical` | 严重影响，可能进入危机或旧伤 |

### 2.2 数值等级建议

如果代码用整数，可使用：

```text
none = 0
low = 1-3
medium = 4-6
high = 7-9
critical = 10+
```

MVP 阶段也可以直接使用整数，但报告层不应直接展示数字。

---

## 3. 事件类型 `event_type`

| 枚举值 | 含义 | 来源系统 |
| --- | --- | --- |
| `message_delay` | 消息延迟/晚回 | 25、35 |
| `selective_availability` | 对别人有空、对伴侣没空 | 25、35 |
| `impression_effort_change` | 形象经营/投入变化 | 26、35 |
| `partner_model_challenge` | 伴侣认知被挑战 | 26 |
| `self_disclosure` | 自我表露事件 | 27、35 |
| `responsiveness_test` | 回应性事件 | 27、35 |
| `privacy_boundary` | 隐私边界事件 | 27、31、35 |
| `secret_discovery` | 秘密被发现 | 25、27、35 |
| `digital_evidence` | 数字证据事件 | 25、35 |
| `conflict_complaint` | 抱怨/不满表达 | 29、35 |
| `conflict_timeout` | 暂停争吵 | 29、35 |
| `conflict_repair` | 冲突修复 | 29、35 |
| `contempt_or_mockery` | 嘲讽/蔑视/攻击脆弱点 | 29、35 |
| `alternative_attraction` | 替代对象吸引 | 30、35 |
| `relationship_boredom` | 关系沉闷 | 32、35 |
| `relationship_turbulence` | 关系动荡 | 32、35 |
| `equity_conflict` | 公平冲突 | 33、35 |
| `caregiving_imbalance` | 照顾/家务/情绪劳动不平衡 | 33、35 |
| `scorekeeping_shift` | 从共有转向记账 | 33、35 |

---

## 4. 真实原因类型 `truth_type`

### 4.1 通用真相类型

| 枚举值 | 含义 | 伤害倾向 |
| --- | --- | --- |
| `benign_reason` | 良性原因，没有明显伤害意图 | low |
| `busy` | 真的在忙 | low |
| `phone_unavailable` | 手机/客观条件不可用 | low |
| `stress` | 压力导致表现下降 | low-medium |
| `processing` | 需要时间处理情绪或信息 | low |
| `not_ready` | 尚未准备好表达/承诺/谈论 | low-medium |
| `comfort` | 关系稳定后更放松 | low |
| `slow_pacing` | 节奏慢，不代表恶意 | low |
| `privacy_boundary` | 正当隐私边界 | low-medium |
| `protect_partner` | 为避免伤害对方而暂时保留 | medium |
| `avoidance` | 看见问题但回避处理 | medium |
| `low_trust` | 尚未足够信任对方 | medium |
| `neglect` | 对关系投入或优先级下降 | medium-high |
| `effort_decay` | 经营投入减少 | medium |
| `taken_for_granted` | 把对方付出视为理所当然 | medium-high |
| `selective_effort` | 对外部高投入，对伴侣低投入 | medium-high |
| `concealment` | 隐瞒关键信息 | high |
| `unresolved_attachment` | 对前任或旧关系仍有未处理牵连 | medium-high |
| `boundary_blur` | 与他人边界模糊 | high |
| `betrayal` | 背叛或严重违背承诺 | critical |
| `identity_split` | 维持两套身份/关系圈 | high-critical |
| `habit_cleanup` | 习惯性清理记录，无特殊隐瞒 | low |
| `avoid_conflict` | 为避免冲突而隐瞒或删除 | medium-high |
| `accurate_pattern` | 被指出的是确实重复存在的模式 | medium |
| `old_model` | 对方使用旧印象解释现在 | medium |
| `projection` | 把自身恐惧或行为投射到对方 | medium |
| `conflict_attack` | 冲突中为了压制或攻击对方 | high |

### 4.2 使用边界

`truth_type` 表示系统真实原因，玩家不一定能看到。

玩家可见报告不应直接暴露：

```text
truth_type = betrayal
truth_type = concealment
```

除非剧情中已有足够证据或真相已揭露。

---

## 5. 可见线索 `observable_trace`

| 枚举值 | 含义 |
| --- | --- |
| `online_but_no_reply` | 在线但未回复 |
| `message_seen_but_ignored` | 已读但未回 |
| `social_media_updated_but_no_reply` | 社交媒体更新但未回复 |
| `selective_availability_trace` | 对其他人/事有空，对当前关系无空 |
| `explanation_timing_conflict` | 解释和时间线冲突 |
| `explanation_content_conflict` | 解释内容前后矛盾 |
| `explanation_overly_vague` | 解释过于模糊 |
| `deleted_or_hidden_trace` | 删除或隐藏痕迹 |
| `phone_privacy_shift` | 手机隐私行为突然变化 |
| `current_contact_trace` | 当前仍有联系痕迹 |
| `third_party_witness` | 第三方证词/共同好友线索 |
| `payment_or_location_trace` | 支付、定位、出行记录线索 |
| `alt_account_trace` | 小号/备用账号痕迹 |
| `changed_routine_trace` | 作息或日常模式异常变化 |
| `repeated_pattern_trace` | 同类事件重复出现 |
| `no_clear_trace` | 没有明确线索 |

---

## 6. 证据强度字段

### 6.1 `evidence_chain_strength`

用于描述证据链强度。

```text
none
weak
moderate
strong
conclusive
```

| 值 | 含义 |
| --- | --- |
| `none` | 无证据，只是感受或猜测 |
| `weak` | 有模糊线索，但不能支持强判断 |
| `moderate` | 有多个线索，支持怀疑但仍有解释空间 |
| `strong` | 证据较强，负面解释可信度高 |
| `conclusive` | 真相基本确认 |

### 6.2 `explanation_consistency`

```text
consistent
minor_gap
major_gap
contradictory
unknown
```

---

## 7. 解释类型 `interpretation_type`

| 枚举值 | 含义 |
| --- | --- |
| `benign_interpretation` | 善意解释 |
| `neutral_uncertainty` | 暂时不确定，不做强判断 |
| `suspicion` | 怀疑有问题 |
| `negative_intent_attribution` | 归因为恶意、故意或不在乎 |
| `self_blame` | 归因为自己不够好或做错 |
| `relationship_threat_interpretation` | 解释为关系威胁 |
| `privacy_respect_interpretation` | 解释为正当隐私 |
| `control_interpretation` | 解释为控制或被控制 |
| `abandonment_interpretation` | 解释为被抛弃/优先级下降 |
| `projection_interpretation` | 基于自身行为或恐惧投射 |
| `old_wound_interpretation` | 被旧伤记忆触发的解释 |

---

## 8. 解释准确度 `interpretation_accuracy`

| 枚举值 | 含义 |
| --- | --- |
| `accurate_alertness` | 怀疑有问题，且事实/证据支持 |
| `stable_trust` | 相信没问题，且事实确实没问题 |
| `over_suspicion` | 怀疑有问题，但事实/证据不足 |
| `selective_blindness` | 相信没问题，但事实存在问题 |
| `unknown` | 当前证据不足，无法判断 |
| `partially_accurate` | 部分准确，部分误读 |
| `confident_misread` | 很自信但判断错误 |

### 8.1 与报告标签区别

`interpretation_accuracy` 是系统裁决字段。

`report_tag` 可输出：

```text
accurate_alertness
over_suspicion_pattern
confident_misreader
selective_blindness_pattern
```

两者不完全等同。

---

## 9. 沟通回应类型 `communication_response_type`

| 枚举值 | 含义 | 关系影响倾向 |
| --- | --- | --- |
| `attentive_validation` | 认真倾听并确认感受 | positive |
| `active_listening` | 复述、澄清、确认理解 | positive |
| `supportive_silence` | 支持性沉默，陪伴不打断 | positive-neutral |
| `processing_silence` | 处理性沉默，之后会回应 | neutral |
| `quick_comfort` | 快速安慰但较浅 | mild_positive |
| `problem_solving_only` | 只给方案，忽略情绪 | context_dependent |
| `reciprocal_disclosure` | 互惠表露 | positive |
| `dismissive_response` | 敷衍、否定或转移 | negative |
| `mocking_response` | 嘲笑、讽刺、拿脆弱开玩笑 | high_negative |
| `judgmental_response` | 评判、道德压迫 | negative |
| `intrusive_questioning` | 追问过度，像审问 | negative |
| `no_response` | 没有回应 | context_dependent |

---

## 10. 冲突回应类型 `conflict_response_type`

| 枚举值 | 含义 | 关系影响倾向 |
| --- | --- | --- |
| `precise_expression` | 聚焦具体行为和感受 | positive |
| `i_statement` | 第一人称表达 | positive |
| `xyz_statement` | XYZ 陈述 | positive |
| `validation_before_disagreement` | 先确认感受再表达不同意见 | positive |
| `repair_attempt` | 道歉、补偿或提出调整 | positive |
| `effective_timeout` | 有效暂停并回来处理 | positive-neutral |
| `defensive_explanation` | 防卫性解释 | negative |
| `cross_complaining` | 反向抱怨 | negative |
| `kitchen_sinking` | 翻旧账堆叠 | negative |
| `mind_reading_attack` | 读心式攻击 | negative |
| `personality_attack` | 人格攻击 | high_negative |
| `contempt` | 蔑视、讥讽、羞辱 | high_negative |
| `stonewalling` | 石墙/长期拒绝回应 | high_negative |
| `exit_threat` | 分手威胁 | high_negative |
| `appeasement_without_understanding` | 表面认错但没有理解 | unstable |

---

## 11. 聚合器输入字段注册表

### 11.1 基础方向字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `event_id` | string | 事件 ID |
| `event_type` | enum | 事件类型 |
| `source_id` | string | 事件发起/行为主体 |
| `target_id` | string | 事件影响对象 |
| `perspective_id` | string | 当前结算视角，可等于 source 或 target |
| `day` | int | 当前天数或时间索引 |

### 11.2 事实与证据字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `truth_type` | enum | 真实原因类型 |
| `truth_harm_level` | int/level | 事实伤害强度 |
| `deception_level` | int/level | 欺骗强度 |
| `boundary_violation_level` | int/level | 边界侵犯强度 |
| `evidence_chain_strength` | int/enum | 证据链强度 |
| `explanation_consistency` | enum | 解释一致性 |
| `observable_traces` | list[enum] | 可见线索列表 |

### 11.3 解释与认知字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `interpretation_type` | enum | 解释类型 |
| `interpretation_accuracy` | enum | 解释准确度 |
| `partner_model_confidence` | int | 对伴侣模型的自信程度 |
| `partner_model_accuracy` | int | 伴侣模型准确度 |
| `projection_bias_effect` | int | 投射偏差影响 |
| `threat_bias_effect` | int | 威胁扫描影响 |
| `selective_blindness_effect` | int | 选择性忽视影响 |

### 11.4 沟通与表露字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `disclosure_depth` | int | 表露深度 |
| `disclosure_pacing_risk` | int | 表露节奏风险 |
| `perceived_responsiveness` | int | 被回应感 |
| `emotional_validation` | int | 情绪确认程度 |
| `privacy_boundary_conflict` | int | 隐私边界冲突强度 |
| `secret_damage_level` | int | 秘密对关系的伤害强度 |
| `communication_response_type` | enum | 沟通回应类型 |

### 11.5 冲突与修复字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `conflict_response_type` | enum | 冲突回应类型 |
| `conflict_escalation_risk` | int | 冲突升级风险 |
| `criticism_intensity` | int | 批评强度 |
| `contempt_signal` | int | 蔑视信号强度 |
| `defensive_response` | int | 防卫反应强度 |
| `stonewalling_level` | int | 石墙程度 |
| `active_listening_skill` | int | 积极倾听程度 |
| `validation_skill` | int | 感受确认能力 |
| `timeout_repair_success` | bool | 暂停后是否回来处理 |
| `repair_attempt_quality` | int | 修复尝试质量 |

### 11.6 社会交换与依赖字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `relationship_rewards_delta` | int | 关系奖赏变化 |
| `relationship_costs_delta` | int | 关系代价变化 |
| `comparison_level_gap` | int | 当前关系结果与期待差距 |
| `comparison_level_alternatives_delta` | int | 替代选择吸引变化 |
| `investment_weight_delta` | int | 投入绑定变化 |
| `leaving_cost_delta` | int | 离开成本变化 |
| `dependence_gap_delta` | int | 双方依赖差异变化 |

### 11.7 接近/回避与动荡字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `approach_reward_delta` | int | 正向奖赏/快乐/新鲜感变化 |
| `avoidance_cost_pressure_delta` | int | 痛苦/威胁/回避压力变化 |
| `relationship_excitement_delta` | int | 关系活力变化 |
| `relationship_safety_delta` | int | 关系安全感变化 |
| `boredom_delta` | int | 沉闷变化 |
| `turbulence_delta` | int | 关系动荡变化 |
| `self_expansion_delta` | int | 自我延伸/共同成长变化 |

### 11.8 共有/交换与公平字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `communal_care_delta` | int | 共有照顾变化 |
| `exchange_scorekeeping_delta` | int | 记账倾向变化 |
| `perceived_equity_delta` | int | 主观公平感变化 |
| `underbenefit_feeling_delta` | int | 获益不足感变化 |
| `overbenefit_guilt_delta` | int | 过度获益内疚变化 |
| `felt_appreciation_delta` | int | 被看见/被感谢变化 |
| `taken_for_granted_delta` | int | 被理所当然对待变化 |

---

## 12. RelationshipStateDelta 输出字段注册表

### 12.1 MVP 必备字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `source_id` | string | 本次 delta 的行为主体或来源角色 |
| `target_id` | string | 本次 delta 影响的对象角色 |
| `trust_delta` | int | 信任变化 |
| `satisfaction_delta` | int | 满意度变化 |
| `intimacy_delta` | int | 亲密感变化 |
| `stability_delta` | int | 关系稳定性变化 |
| `repair_chance_delta` | int | 修复机会变化 |
| `old_wound_memory_delta` | int | 旧伤记忆强度变化 |
| `safety_delta` | int | 安全感变化，MVP 可默认为 0 |
| `excitement_delta` | int | 活力/刺激变化，MVP 可默认为 0 |
| `fairness_delta` | int | 公平感变化，MVP 可默认为 0 |
| `dependence_delta` | int | 依赖度变化，MVP 可默认为 0 |
| `report_tags` | list | 报告标签 |
| `memory_notes` | list | 记忆记录摘要 |
| `debug_reasons` | list | 调试解释，不一定给玩家看 |

### 12.2 后续建议字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `player_facing_summary` | string | 玩家可见摘要 |
| `hidden_truth_notes` | list | 仅 debug 可见的真实原因说明 |
| `tag_details` | list[ReportTag] | 带强度和来源的标签结构 |
| `memory_events` | list[RelationshipMemory] | 结构化记忆事件 |

---

## 13. 报告标签 ID 注册表

本节注册可直接用于 `report_tags` 的标签 ID。详细玩家可读表达见 `docs/design/37_relationship_report_tag_dictionary.md`。

### 13.1 认知与归因标签

```text
accurate_alertness
over_suspicion_pattern
confident_misreader
selective_blindness_pattern
outdated_partner_model
romantic_idealizer
```

### 13.2 表露与回应标签

```text
deep_discloser
guarded_discloser
fast_disclosure_pattern
high_responsiveness_need
disclosure_regret
low_responsiveness
```

### 13.3 秘密与边界标签

```text
privacy_boundary_conflict
high_transparency_expectation
deception_risk
```

### 13.4 冲突与修复标签

```text
active_listener
repair_capable
stonewalling_pattern
contempt_risk
mind_reading_pattern
```

### 13.5 社会交换与依赖标签

```text
high_comparison_level
alternative_sensitive
investment_bound
fear_of_loss_pattern
```

### 13.6 接近/回避与动荡标签

```text
safe_but_bored_pattern
risk_excitement_pattern
turbulence_sensitive
self_expansion_seeker
```

### 13.7 共有/交换/公平标签

```text
communal_oriented
exchange_oriented
underbenefit_sensitive
scorekeeping_pattern
taken_for_granted_sensitive
```

### 13.8 聚合器状态标签

```text
trust_damage_event
repair_window_open
old_wound_written
short_term_fluctuation
```

---

## 14. ReportTag 结构建议

MVP 可以先用：

```python
report_tags: list[str]
```

后续建议升级为：

```python
@dataclass
class ReportTag:
    tag_id: str
    label: str
    strength: str
    source_event_id: str
    target_character_id: str
    scope: str
    player_facing_text: str
```

### 14.1 `scope` 枚举

```text
event
pattern
questionnaire
relationship_state
debug_only
```

---

## 15. 旧伤记忆字段注册建议

后续结构化旧伤记忆可使用：

```python
@dataclass
class RelationshipMemory:
    memory_id: str
    source_event_id: str
    source_id: str
    target_id: str
    wound_type: str
    severity: str
    trigger_keywords: list[str]
    created_day: int
    last_triggered_day: int
    decay_policy: str
    repair_status: str
```

### 15.1 `wound_type` 枚举

```text
betrayal_discovered
privacy_violation
vulnerability_mocked
contempt_attack
stonewalling_repeated
promise_broken
taken_for_granted_repeated
public_humiliation
abandonment_triggered
```

### 15.2 `repair_status` 枚举

```text
unrepaired
partially_repaired
repaired
reopened
```

### 15.3 `decay_policy` 枚举

```text
no_decay_until_repair
slow_decay
normal_decay
fast_decay_if_repaired
pattern_reinforced
```

---

## 16. 禁止/废弃字符串

后续不要在代码和配置中新增以下模糊值：

```text
bad_silence
maybe_cheating
love_problem
trust_issue
weird_behavior
toxic
crazy
clingy
cold_person
```

建议替换为：

| 禁止值 | 替代值 |
| --- | --- |
| `bad_silence` | `stonewalling` / `processing_silence` / `supportive_silence` |
| `maybe_cheating` | `boundary_blur` / `concealment` / `betrayal` |
| `love_problem` | `relationship_threat_interpretation` |
| `trust_issue` | `trust_damage_event` / `deception_risk` |
| `weird_behavior` | 具体 `observable_trace` |
| `toxic` | 具体行为标签，如 `contempt_risk`、`stonewalling_pattern` |
| `clingy` | `fear_of_loss_pattern` / `high_responsiveness_need` |
| `cold_person` | `guarded_discloser` / `low_responsiveness` |

---

## 17. 后续代码落地建议

### 17.1 MVP 阶段

先不必把本文档全部转成 Python Enum。可以先：

```text
1. 在 relationship_state_aggregator.py 中使用常量集合。
2. 测试里引用这些常量或直接用注册值。
3. 避免拼错即可。
```

### 17.2 稳定后

可新增：

```text
if_game/relationship_constants.py
```

包含：

```python
TRUTH_TYPES = {...}
OBSERVABLE_TRACES = {...}
INTERPRETATION_TYPES = {...}
INTERPRETATION_ACCURACIES = {...}
REPORT_TAGS = {...}
```

暂不建议一开始就上复杂 Enum 类，避免过度工程化。

---

## 18. 一句话总结

```text
40 号文档的作用，是把 IF 关系系统里所有容易写乱的字符串和字段统一注册，保证后续事件、聚合器、报告标签和测试使用同一套语言。
```

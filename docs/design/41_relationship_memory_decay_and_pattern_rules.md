# 关系记忆衰减与模式阈值规则

本文档用于补充 IF 关系系统中的重复事件、旧伤记忆、修复记忆、时间衰减、模式阈值和长期关系信念更新规则。

它承接：

```text
docs/design/25_attribution_memory_belief_system.md
docs/design/29_conflict_communication_repair_system.md
docs/design/31_system_integration_consistency_rules.md
docs/design/34_relationship_state_aggregator_implementation_plan.md
docs/design/35_relationship_event_template_library.md
docs/design/38_relationship_system_logic_audit_and_optimization_notes.md
docs/design/40_relationship_enum_and_field_registry.md
```

核心原则：

```text
亲密关系里，很多伤害不是一次事件造成的，而是重复模式造成的。
一次晚回消息可能只是短期波动；连续多次晚回且解释不一致，才会变成信任结构问题。
一次沉默可能是在处理情绪；长期沉默且不回到问题，才会成为石墙模式。
一次家务不平衡可以协商；长期被理所当然对待，才会形成获益不足和旧伤。
```

---

## 1. 设计目的

当前 `relationship_state_aggregator` 方案已经能处理单次事件的关系状态变化。但 IF 是长期关系模拟，必须继续处理：

```text
同类事件是否重复发生？
旧伤是否被再次触发？
修复是否真的发生？
时间过去后记忆是否淡化？
某些轻微事件是否因为重复而变成模式？
某些高伤害事件是否一次就写入长期记忆？
```

因此需要在单次 `RelationshipStateDelta` 之外，设计长期记忆层。

---

## 2. 关系记忆类型

### 2.1 记忆不只有旧伤

IF 中关系记忆至少分为四类：

| 类型 | 含义 | 例子 |
| --- | --- | --- |
| `positive_memory` | 正向记忆 | 被认真安慰、被保护、危机中被选择 |
| `repair_memory` | 修复记忆 | 冲突后对方真诚道歉并改变 |
| `old_wound_memory` | 旧伤记忆 | 被欺骗、被嘲讽脆弱、被长期冷处理 |
| `pattern_memory` | 模式记忆 | 同类问题反复出现，形成“他/她总是这样”的信念 |

### 2.2 不同记忆影响不同状态

| 记忆类型 | 主要影响 |
| --- | --- |
| `positive_memory` | 亲密感、信任、关系韧性 |
| `repair_memory` | 修复机会、冲突后恢复速度、成长信念 |
| `old_wound_memory` | 威胁扫描、信任、脆弱表露、安全感 |
| `pattern_memory` | 伴侣模型、归因方式、未来预测、满意度 |

---

## 3. RelationshipMemory 结构草案

后续代码可使用：

```python
@dataclass
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
    trigger_keywords: list[str]
    created_day: int
    last_triggered_day: int
    occurrence_count: int
    decay_policy: str
    repair_status: str
    visibility: str
    player_facing_note: str
    debug_note: str
```

### 3.1 字段说明

| 字段 | 含义 |
| --- | --- |
| `memory_id` | 记忆唯一 ID |
| `source_event_id` | 来源事件 ID |
| `source_id` | 行为主体 |
| `target_id` | 受影响对象 |
| `memory_type` | 正向、修复、旧伤、模式 |
| `wound_type` | 旧伤类型，非旧伤可为空 |
| `pattern_key` | 重复模式键 |
| `severity` | 严重程度 |
| `intensity` | 当前强度，建议 0-100 |
| `trigger_keywords` | 后续触发该记忆的关键词或事件类型 |
| `created_day` | 创建时间 |
| `last_triggered_day` | 最近触发时间 |
| `occurrence_count` | 同类事件累计次数 |
| `decay_policy` | 衰减规则 |
| `repair_status` | 修复状态 |
| `visibility` | 玩家可见 / debug 可见 |
| `player_facing_note` | 玩家报告可见摘要 |
| `debug_note` | 调试用真实原因说明 |

---

## 4. 记忆类型枚举

### 4.1 `memory_type`

```text
positive_memory
repair_memory
old_wound_memory
pattern_memory
neutral_context_memory
```

### 4.2 `wound_type`

沿用 `40_relationship_enum_and_field_registry.md`，并补充说明：

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

### 4.3 `repair_status`

```text
unrepaired
acknowledged
partially_repaired
repaired
reopened
repeated_after_repair
```

说明：

| 状态 | 含义 |
| --- | --- |
| `unrepaired` | 伤害发生后没有被认真处理 |
| `acknowledged` | 对方承认伤害，但行动不足 |
| `partially_repaired` | 有道歉或补偿，但未完全恢复 |
| `repaired` | 经过持续行动，伤害明显修复 |
| `reopened` | 旧伤被新事件重新触发 |
| `repeated_after_repair` | 修复后又犯同类问题，伤害加重 |

### 4.4 `visibility`

```text
player_visible
npc_visible
debug_only
revealed_later
```

---

## 5. 模式键 `pattern_key`

同类事件需要归并到模式键，而不是每次都创建完全独立记忆。

### 5.1 常用模式键

| pattern_key | 对应问题 |
| --- | --- |
| `late_reply_inconsistency` | 晚回消息 + 解释不一致 |
| `selective_availability` | 对别人有空，对伴侣没空 |
| `privacy_boundary_conflict` | 隐私边界反复冲突 |
| `hidden_contact_or_ex` | 前任/异性联系隐瞒 |
| `deleted_or_hidden_digital_trace` | 删除、隐藏数字痕迹 |
| `conflict_defensiveness` | 被指出问题后防卫 |
| `cross_complaining_loop` | 反向抱怨循环 |
| `stonewalling_after_conflict` | 冲突后沉默/石墙 |
| `contempt_or_mockery` | 嘲讽、蔑视、羞辱 |
| `failed_repair_promise` | 道歉后不改变 |
| `household_underbenefit` | 家务/照料长期不公平 |
| `emotional_labor_imbalance` | 情绪劳动长期单方承担 |
| `boredom_without_repair` | 关系沉闷但不处理 |
| `alternative_attention_pull` | 外部新鲜感反复拉动 |
| `exit_threat_pattern` | 分手威胁反复出现 |

### 5.2 模式键的作用

```text
同类轻微事件重复出现时，pattern_key 用于累计 occurrence_count。
当 occurrence_count 达到阈值，系统才从短期波动升级为模式记忆。
```

---

## 6. 单次事件与重复模式的区别

### 6.1 单次轻微事件

例子：

```text
对方一次晚回消息，解释基本合理。
```

处理：

```text
memory_type: neutral_context_memory 或不写记忆
intensity: 0-10
pattern_count +1 可选
不写 old_wound_memory
```

### 6.2 重复轻微事件

例子：

```text
对方连续多次晚回，每次解释都很模糊。
```

处理：

```text
pattern_key: late_reply_inconsistency
occurrence_count 增加
达到阈值后写 pattern_memory
可能影响 trust_suspicion_sensitivity 和 trust_old_wound_memory
```

### 6.3 单次高伤害事件

例子：

```text
脆弱表露后被嘲讽。
```

处理：

```text
memory_type: old_wound_memory
wound_type: vulnerability_mocked
severity: high
即使只发生一次，也可写入长期记忆
```

### 6.4 重复高伤害事件

例子：

```text
多次嘲讽、羞辱或拿脆弱开玩笑。
```

处理：

```text
old_wound_memory 强化
repair_status 若没有修复，进入 pattern_reinforced
关系安全感和表露意愿显著下降
```

---

## 7. 模式阈值规则

### 7.1 通用阈值

| 次数 | 处理 |
| --- | --- |
| 1 次 | 事件波动，通常不形成模式 |
| 2 次 | 可提示“类似事件再次出现” |
| 3 次 | 形成轻度模式提示 |
| 5 次 | 形成稳定模式记忆 |
| 8 次以上 | 进入关系信念更新 |

### 7.2 高伤害事件阈值

以下事件可以一次写入旧伤：

```text
betrayal_discovered
vulnerability_mocked
contempt_attack
public_humiliation
privacy_violation 严重级别
```

以下事件通常需要重复才写旧伤：

```text
message_delay
minor_defensiveness
low_responsiveness
small_household_imbalance
routine_boredom
```

### 7.3 修复后的重复

如果同类事件已经被修复过，但又再次发生：

```text
repair_status: repeated_after_repair
intensity 增幅高于普通重复
trust_delta 下降更明显
```

原因：

```text
修复后重复会破坏“对方会改变”的信念。
```

---

## 8. 时间衰减规则

### 8.1 decay_policy

```text
no_decay_until_repair
slow_decay
normal_decay
fast_decay_if_repaired
pattern_reinforced
```

### 8.2 衰减解释

| decay_policy | 含义 | 适用场景 |
| --- | --- | --- |
| `no_decay_until_repair` | 不修复就不自然淡化 | 背叛、羞辱、嘲讽脆弱 |
| `slow_decay` | 会慢慢淡化，但保留影响 | 隐私冲突、反复防卫 |
| `normal_decay` | 普通小波动可自然下降 | 轻微误会、一次不高兴 |
| `fast_decay_if_repaired` | 修复后较快下降 | 道歉具体且后续行动一致 |
| `pattern_reinforced` | 因重复而增强，不衰减 | 反复同类问题 |

### 8.3 建议数值

如果 `intensity` 使用 0-100：

| 策略 | 每 7 天无触发时变化 |
| --- | --- |
| `normal_decay` | -5 到 -10 |
| `slow_decay` | -1 到 -3 |
| `fast_decay_if_repaired` | -10 到 -20 |
| `no_decay_until_repair` | 0 |
| `pattern_reinforced` | 0 或 +1 到 +3 |

MVP 不必实现具体天数衰减，但字段要预留。

---

## 9. 修复记忆规则

### 9.1 修复不是一句道歉

修复需要至少包含：

```text
承认事实
承认影响
承担责任
具体补偿或改变
后续一段时间不重复
```

### 9.2 修复质量等级

```text
none
symbolic
acknowledged
behavioral
sustained
```

| 等级 | 含义 |
| --- | --- |
| `none` | 没有修复 |
| `symbolic` | 只有形式道歉或安慰 |
| `acknowledged` | 承认伤害，但行动不足 |
| `behavioral` | 有具体改变或补偿 |
| `sustained` | 一段时间内持续改变 |

### 9.3 修复记忆的作用

高质量修复会生成：

```text
memory_type: repair_memory
repair_status: repaired 或 partially_repaired
```

影响：

```text
repair_chance_delta 上升
relationship_resilience 上升
old_wound intensity 下降
```

但修复记忆不应直接删除旧伤。更合理的是：

```text
旧伤仍存在，但被标记为已修复或部分修复。
后续类似事件若不再发生，旧伤逐渐淡化。
```

---

## 10. 旧伤再触发规则

### 10.1 触发条件

旧伤被触发通常来自：

```text
同类事件再次发生
相似语气或场景出现
对方使用相似解释
玩家/NPC 看到相似线索
关系压力升高
```

### 10.2 再触发效果

当旧伤再触发时：

```text
last_triggered_day 更新
intensity 上升
repair_status 可变为 reopened
解释倾向更负面
信任恢复更慢
```

### 10.3 示例

旧伤：

```text
wound_type: vulnerability_mocked
trigger_keywords: 脆弱表达, 嘲讽, 开玩笑
```

后续事件：

```text
玩家再次说起不安，对方用玩笑带过。
```

即使这次玩笑本身不严重，也会触发旧伤：

```text
repair_status: reopened
intensity +10
safe_disclosure_space_delta 下降
```

---

## 11. 正向记忆与关系韧性

### 11.1 关系不应只记伤害

如果系统只记录旧伤，会导致关系越来越负面。因此需要正向记忆。

正向记忆来源：

```text
对方在压力中选择坦白
冲突后主动修复
脆弱表达被接住
重要时刻被陪伴
对方为公平主动调整
面对诱惑时主动设边界
```

### 11.2 正向记忆效果

```text
trust_delta 上升
intimacy_delta 上升
repair_chance_delta 上升
relationship_resilience 上升
```

### 11.3 正向记忆抵消规则

正向记忆可以缓冲轻微事件，但不应抵消严重背叛。

```text
许多稳定陪伴可以让一次小误会更容易被善意解释。
但不能直接抹掉严重欺骗、羞辱或背叛。
```

---

## 12. 模式记忆与关系信念更新

### 12.1 从事件到模式

关系信念不应被单次普通事件改写。建议：

```text
轻微事件重复 3 次 → 模式提示
轻微事件重复 5 次 → 模式记忆
重复 8 次以上 → 关系信念更新
高伤害事件 1 次 → 可直接进入旧伤
高伤害事件重复 → 关系信念快速更新
```

### 12.2 可能更新的关系信念

| 信念 | 触发来源 |
| --- | --- |
| `partner_is_reliable` 下降 | 反复承诺后不做 |
| `partner_respects_vulnerability` 下降 | 嘲讽脆弱表达 |
| `partner_will_repair` 上升 | 冲突后持续修复 |
| `relationship_is_safe` 下降 | 背叛、石墙、羞辱 |
| `my_needs_matter_here` 下降 | 长期不被回应或被理所当然 |
| `conflict_can_be_repaired` 上升 | 多次冲突后有效解决 |

---

## 13. 问卷自述与行为校准

### 13.1 基本原则

```text
问卷结果 = 初始倾向
游戏行为 = 动态证据
重复行为 > 单题自述
关键事件 > 抽象自评
```

### 13.2 权重建议

| 阶段 | 问卷权重 | 行为权重 |
| --- | --- | --- |
| 游戏初期 | 70% | 30% |
| 出现 3 次同类行为后 | 50% | 50% |
| 出现 5 次同类行为后 | 30% | 70% |
| 关键高伤害事件后 | 局部被行为覆盖 | 局部优先 |

### 13.3 自述-行为差异标签

可新增运行时标签：

```text
self_report_behavior_gap
```

触发例子：

```text
问卷说尊重隐私，但游戏中多次查手机。
问卷说会修复冲突，但每次都冷处理。
问卷说不在意外部选择，但反复暧昧比较。
```

---

## 14. 旧伤与玩家可见报告边界

### 14.1 玩家可见报告

玩家可见报告只能使用当前角色能知道的信息。

可以写：

```text
这次事件让你更容易联想到过去类似的不安。
```

不应写：

```text
系统判定对方真实原因是 concealment，所以你写入 betrayal_discovered 旧伤。
```

除非真相已经揭露。

### 14.2 debug 报告

debug 可显示：

```text
truth_type
wound_type
pattern_key
memory intensity
decay_policy
repair_status
```

---

## 15. 与 relationship_state_aggregator 的关系

### 15.1 聚合器负责单次 delta

`relationship_state_aggregator` 负责一次事件的即时变化：

```text
trust_delta
satisfaction_delta
intimacy_delta
repair_chance_delta
old_wound_memory_delta
```

### 15.2 记忆系统负责长期状态

记忆系统负责：

```text
是否创建记忆
是否更新 pattern_count
是否触发旧伤
是否衰减
是否改变长期关系信念
```

### 15.3 代码顺序建议

```text
event → aggregator → memory_update → report_generation
```

---

## 16. MVP 实现建议

第一版不需要完整记忆系统，但应预留：

```text
memory_notes
pattern_key
occurrence_count
repair_status
```

### 16.1 最小可实现规则

MVP 可先实现：

```text
1. 如果 old_wound_memory_delta > 0，生成 memory_notes。
2. 如果 report_tags 包含 old_wound_written，生成一条旧伤摘要。
3. 如果同一 pattern_key 在测试输入中 occurrence_count >= 3，增加 pattern 标签。
4. 如果 repair_attempt_quality 高，降低旧伤写入强度或生成 repair_memory 摘要。
```

### 16.2 暂缓

```text
真实时间衰减
复杂记忆列表管理
跨角色长期记忆数据库
完整行为校准
```

---

## 17. 不做什么

本系统暂不做：

1. 不让所有小事都写旧伤；
2. 不让旧伤永远无法修复；
3. 不用正向记忆抹掉严重伤害；
4. 不把一次争吵直接升级为长期模式；
5. 不把问卷自述永久固定为角色本质；
6. 不向玩家暴露未揭露的真实原因；
7. 不做心理诊断；
8. 不接 AI API。

---

## 18. 一句话总结

```text
IF 的关系记忆系统要模拟的不是“每件事加减分”，而是：
哪些事件会自然淡化，哪些会因为重复变成模式，哪些会一次写入旧伤，哪些能通过持续修复变成关系韧性。
```

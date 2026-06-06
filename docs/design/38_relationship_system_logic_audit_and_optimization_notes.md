# 关系系统逻辑审查与优化清单

本文档用于对 IF 当前 `25-37` 号关系系统文档进行一次横向逻辑审查，识别潜在矛盾、命名冲突、实现风险和后续需要补充的规则。

本文件不是新玩法设计，而是系统审计结果。后续实现时，如果 `25-37` 中出现含糊或冲突，应优先参考本文档的修正口径。

---

## 1. 审查范围

本次审查覆盖：

```text
docs/design/25_attribution_memory_belief_system.md
docs/design/26_partner_perception_and_impression_system.md
docs/design/27_communication_self_disclosure_system.md
docs/design/28_questionnaire_communication_disclosure_module.md
docs/design/29_conflict_communication_repair_system.md
docs/design/30_social_exchange_dependency_system.md
docs/design/31_system_integration_consistency_rules.md
docs/design/32_approach_avoidance_turbulence_system.md
docs/design/33_communal_exchange_equity_system.md
docs/design/34_relationship_state_aggregator_implementation_plan.md
docs/design/35_relationship_event_template_library.md
docs/design/36_questionnaire_expansion_candidate_pool.md
docs/design/37_relationship_report_tag_dictionary.md
docs/context/2026-06-07_after_relationship_docs_backlog.md
docs/context/codex_task_prompts.md
README.md
```

---

## 2. 总体结论

当前系统没有发现需要推翻重做的根本逻辑错误。

已经成立的核心链路是：

```text
事实层
→ 证据层
→ 伴侣认知层
→ 归因解释层
→ 沟通/表露层
→ 冲突/修复层
→ 奖赏/代价层
→ 接近/回避层
→ 共有/公平层
→ 聚合器统一结算
→ 报告标签输出
```

但当前仍有若干实现前必须修正或补充的点，尤其集中在：

```text
版本号冲突
字段命名和维度注册
MVP 范围与测试范围不完全一致
玩家/NPC 双向状态
关系状态的方向性
事件反复发生和时间衰减
报告标签作用域
```

---

## 3. 问题一：README 文档版本号与 Codex 代码任务版本号冲突

### 3.1 问题

当前 README 已经使用：

```text
v0.1.33 关系状态聚合器实施方案
v0.1.34 关系事件模板库
v0.1.35 问卷扩展候选题池
v0.1.36 关系报告标签词典
v0.1.37 后续任务清单与 Codex 任务提示词库
```

但 `docs/context/codex_task_prompts.md` 中仍写：

```text
v0.1.33 relationship_state_aggregator.py 原型
v0.1.34 aggregator 关键裁决测试补全
v0.1.35 relationship_interpretation.py 接入 aggregator
v0.1.36 冲突沟通事件接入 aggregator
v0.1.37 社会交换/公平轻量接入 aggregator
v0.1.38 问卷补 4 个沟通表露题
```

这会导致后续 Codex 更新 README 时出现重复版本号。

### 3.2 风险

Codex 可能新增第二个 `v0.1.33`，让 README 版本线混乱。

### 3.3 修正口径

从当前状态开始，代码实现版本应顺延为：

```text
v0.1.38 relationship_state_aggregator.py 原型
v0.1.39 aggregator 关键裁决测试补全
v0.1.40 relationship_interpretation.py 接入 aggregator
v0.1.41 冲突沟通事件接入 aggregator
v0.1.42 社会交换/公平轻量接入 aggregator
v0.1.43 问卷补 4 个沟通表露题
```

### 3.4 后续操作

后续应修改：

```text
docs/context/codex_task_prompts.md
docs/context/2026-06-07_after_relationship_docs_backlog.md
```

把其中的代码任务版本号统一顺延。

---

## 4. 问题二：`31_system_integration_consistency_rules.md` 覆盖范围已过期

### 4.1 问题

`31_system_integration_consistency_rules.md` 原始定位是对 `25-30` 做横向校对。后来新增了：

```text
32 接近/回避与动荡
33 共有/交换与公平
34 聚合器实施方案
35 事件模板库
36 问卷候选题池
37 标签词典
```

因此 `31` 的覆盖说明已经不是最新全局口径。

### 4.2 风险

后续阅读者可能误以为 `31` 已完整覆盖 `32-37`，但它实际没有。

### 4.3 修正口径

`31` 仍然有效，但应视为：

```text
第一轮一致性规则：覆盖 25-30。
```

本文档 `38` 作为：

```text
第二轮一致性审查：覆盖 25-37。
```

### 4.4 后续操作

不需要立刻重写 `31`。后续可在 README 或 `31` 开头补一句：

```text
32-37 的补充一致性审查见 docs/design/38_relationship_system_logic_audit_and_optimization_notes.md。
```

---

## 5. 问题三：聚合器 MVP 输出与后续测试范围存在轻微不一致

### 5.1 问题

`34_relationship_state_aggregator_implementation_plan.md` 中写 MVP 暂缓：

```text
dependence_delta
fairness_delta
safety_delta
excitement_delta
完整 CL / CLalt 计算
完整共有/交换关系模型
完整关系动荡轨迹
```

但后续测试又希望覆盖：

```text
低痛苦不等于高快乐
高快乐不等于安全
公平不是五五分
```

这些测试天然需要 `safety_delta`、`excitement_delta`、`fairness_delta` 或等价标签。

### 5.2 风险

Codex 实现 v0.1.38 原型时，如果严格按 MVP 输出砍掉这些字段，后续 v0.1.39 测试又要补字段，造成返工。

### 5.3 修正口径

MVP 仍不做完整系统，但建议一开始就在 `RelationshipStateDelta` 中保留这些字段，默认值为 0：

```text
safety_delta
excitement_delta
fairness_delta
dependence_delta
```

第一版不必复杂计算，但字段应存在，方便后续测试和扩展。

### 5.4 后续操作

修改 Codex 提示词：v0.1.38 原型中 `RelationshipStateDelta` 直接包含这些字段，但实现逻辑可以先很轻。

---

## 6. 问题四：问卷候选维度未必都存在于 128 维主表

### 6.1 问题

`36_questionnaire_expansion_candidate_pool.md` 中出现大量新维度，例如：

```text
self_disclosure_willingness
perceived_responsiveness_need
privacy_boundary_strength
comparison_level_alternatives
safe_but_bored_pattern
communal_orientation
felt_appreciation_need
```

这些字段是很有用的系统变量，但它们未必已经存在于 `docs/design/16_questionnaire_dimension_table.md` 的 128 维主表中。

### 6.2 风险

后续如果直接加入 `questionnaire_mvp.json` 并运行：

```bash
python scripts/check_questionnaire_dimension_ids.py
```

可能出现未识别维度 ID。

### 6.3 修正口径

在真正改问卷 JSON 前，必须先做以下二选一：

#### 方案 A：映射到现有 128 维

新增文档或表格：

```text
docs/design/39_questionnaire_dimension_alias_mapping.md
```

把新增变量映射到既有 128 维，例如：

```text
self_disclosure_willingness → vulnerability_disclosure 或 intimacy_expression 类维度
privacy_boundary_strength → boundary_privacy 类维度
perceived_responsiveness_need → emotional_support_need 类维度
```

#### 方案 B：扩展维度表

将 128 维扩展到 160 维或增加扩展维度区。

### 6.4 当前建议

优先选方案 A。当前不建议马上扩到 160 维，避免问卷系统膨胀。

---

## 7. 问题五：事件 `truth_type`、标签、字段值缺少统一枚举表

### 7.1 问题

`35_relationship_event_template_library.md` 中已经有很多事件分支：

```text
busy
avoidance
neglect
concealment
phone_unavailable
comfort
stress
effort_decay
taken_for_granted
selective_effort
```

`37_relationship_report_tag_dictionary.md` 中也有很多标签 ID。

目前这些字符串分散在多个文档里，没有统一注册表。

### 7.2 风险

代码实现时可能出现：

```text
同一个概念多个名字
大小写不一致
标签拼错
truth_type 无法统一处理
事件配置难以校验
```

### 7.3 修正口径

后续建议新增：

```text
docs/design/39_relationship_enum_and_field_registry.md
```

内容包括：

```text
truth_type 枚举
observable_trace 枚举
interpretation_type 枚举
communication_response_type 枚举
report_tag 枚举
aggregator_input 字段注册表
RelationshipStateDelta 字段注册表
```

### 7.4 优先级

高。建议在正式写复杂事件 JSON 前完成。

---

## 8. 问题六：玩家与 NPC 的状态方向性需要更明确

### 8.1 问题

当前文档多数从“玩家如何理解 NPC”角度写，但 IF 需要双方都可能误读、撒谎、表露、回避、修复、受伤。

关系状态也不应只有一份全局值。至少要区分：

```text
player_to_npc_trust
npc_to_player_trust
player_satisfaction
npc_satisfaction
player_intimacy
npc_intimacy
player_dependence
npc_dependence
```

### 8.2 风险

如果后续只实现单一 `trust_delta`，容易把双方状态误写成完全对称。

现实上可能出现：

```text
玩家更满意，NPC 不满意。
玩家更依赖，NPC 更不怕失去。
玩家信任 NPC，但 NPC 不信任玩家。
玩家觉得修复了，NPC 写入旧伤。
```

### 8.3 修正口径

`relationship_state_aggregator` 第一版可以先输出单向事件影响，但必须在结构上保留方向：

```text
actor_id
target_id
perspective
```

或直接输出：

```text
source_character_id
target_character_id
state_delta_direction
```

### 8.4 后续建议

在 `RelationshipStateDelta` 中至少保留：

```text
source_id
target_id
```

后续再升级为双方状态聚合。

---

## 9. 问题七：重复事件、时间衰减和累积阈值还不够明确

### 9.1 问题

当前系统主要处理“单次事件 delta”，但亲密关系里很多伤害和修复来自重复模式。

例如：

```text
一次晚回消息：小事
连续十次晚回并解释不一致：信任结构问题
一次家务不平衡：可协商
长期家务不平衡：获益不足和怨恨
一次沉默：可能是在处理
长期沉默：石墙模式
```

### 9.2 风险

如果只看单次事件，系统会低估重复模式；如果每次都重扣，又会过度惩罚。

### 9.3 修正口径

后续聚合器需要加入：

```text
repeat_count
recent_frequency
last_occurrence_day
pattern_threshold
decay_rate
```

### 9.4 建议规则

```text
一次轻微事件：短期波动
重复 3 次：形成模式提示
重复 5 次以上：进入关系信念更新
高伤害事件：可直接写旧伤
低伤害事件：需要重复才写旧伤
```

---

## 10. 问题八：旧伤记忆不应只是数字

### 10.1 问题

当前 `old_wound_memory_delta` 是必要字段，但旧伤如果只做数字，会丢掉内容。

### 10.2 风险

后续报告无法解释“为什么玩家现在这么敏感”，只能看到一个旧伤分数。

### 10.3 修正口径

旧伤记忆应至少包含：

```text
memory_id
source_event_id
wound_type
severity
trigger_keywords
created_day
last_triggered_day
decay_policy
repair_status
```

### 10.4 示例

```text
wound_type: vulnerability_mocked
severity: high
trigger_keywords: 脆弱表达, 嘲讽, 被轻视
repair_status: unrepaired
```

这比单纯 `old_wound_memory_delta = +8` 更适合长期关系模拟。

---

## 11. 问题九：报告标签需要作用域和强度，不应只是字符串列表

### 11.1 问题

`34` 的 MVP 可以先输出 `report_tags: list[str]`，但 `37` 已经提出更好的结构：

```python
@dataclass
class ReportTag:
    tag_id: str
    label: str
    strength: str
    source: str
    player_facing_text: str
```

### 11.2 风险

如果长期只用字符串列表，会出现：

```text
标签不知道来自哪个事件
标签不知道强度
同一标签无法区分玩家/NPC
矛盾标签难以排除
报告难以生成自然语言
```

### 11.3 修正口径

MVP 可用 `list[str]`，但测试和设计上应预留：

```text
tag_id
strength
source_event_id
target_character_id
scope: event / pattern / questionnaire
```

### 11.4 后续建议

在 v0.1.38 原型中可以仍用字符串，但 `debug_reasons` 应记录来源，避免后续完全无上下文。

---

## 12. 问题十：问卷自述与游戏行为校准规则还需要落地说明

### 12.1 问题

多个文档都强调：

```text
问卷结果 = 初始画像
游戏行为 = 动态修正
```

但尚未明确如何修正。

### 12.2 风险

后续可能让问卷分数永久决定角色，导致游戏行为失去意义。

### 12.3 修正口径

后续应补一个轻量规则：

```text
初始问卷权重：60%-80%
早期游戏行为权重：20%-40%
重复行为出现后：行为权重逐渐上升
关键事件行为：可以局部覆盖问卷自述
```

### 12.4 示例

```text
问卷说自己尊重隐私。
但游戏中连续 3 次查手机。
则 privacy_boundary_respect 应下降，并标记 self_report_behavior_gap。
```

---

## 13. 问题十一：关系状态与事件报告之间缺少“玩家可见/系统隐藏”边界

### 13.1 问题

IF 有真实原因层和隐藏事实层。玩家不应总能看到真实原因。

### 13.2 风险

报告如果直接说：

```text
对方真实原因是 concealment。
```

会破坏游戏中的不确定性和推理体验。

### 13.3 修正口径

报告输出应分两层：

```text
玩家可见报告：只写玩家当前有证据能判断的内容。
开发/调试报告：可显示真实原因、证据强度、聚合器输入和 debug_reasons。
```

### 13.4 后续建议

`RelationshipStateDelta` 可区分：

```text
player_facing_summary
debug_reasons
hidden_truth_notes
```

---

## 14. 问题十二：系统目前偏关系双人内部，外部社交网络影响可后续补强

### 14.1 问题

当前主要关注两个人内部互动，但 IF 是现实向亲密关系模拟，外部因素应继续保留扩展口：

```text
朋友意见
共同圈子
流言
家庭压力
学校/工作压力
经济与居住条件
社交媒体可见性
```

### 14.2 当前状态

早期题库和文档已有一些社交网络/现实压力内容，但 `25-37` 新系统里相对偏心理内部机制。

### 14.3 修正口径

不需要现在扩展，但后续事件模板库可以增加一组：

```text
外部社交网络事件
现实压力事件
社交媒体展示事件
家庭介入事件
```

---

## 15. 优先级排序

### P0：代码前必须修正

```text
1. Codex 任务版本号冲突：代码任务应从 v0.1.38 起。
2. 问卷候选维度需要映射到 128 维或建立 alias 表。
3. 聚合器字段应保留方向性：source_id / target_id。
4. MVP 输出建议保留 safety/excitement/fairness/dependence 字段，默认 0。
```

### P1：实现时必须注意

```text
5. truth_type/report_tag/aggregator 字段需要统一注册表。
6. 旧伤记忆需要结构化，不宜只有数字。
7. report_tags 需要作用域和强度。
8. 玩家可见报告和 debug 报告要区分。
```

### P2：后续扩展

```text
9. 重复事件和时间衰减。
10. 问卷自述与行为校准。
11. 外部社交网络和现实压力事件补强。
```

---

## 16. 建议新增/修改文档

后续建议新增：

```text
docs/design/39_questionnaire_dimension_alias_mapping.md
docs/design/40_relationship_enum_and_field_registry.md
docs/design/41_relationship_memory_decay_and_pattern_rules.md
```

并修改：

```text
docs/context/codex_task_prompts.md
docs/context/2026-06-07_after_relationship_docs_backlog.md
```

核心修改：

```text
把后续代码任务版本号从 v0.1.33-v0.1.38 改为 v0.1.38-v0.1.43。
```

---

## 17. 一句话总结

```text
当前 IF 关系系统的理论链路是成立的，没有根本矛盾；但在进入代码前，必须先修正版本号、字段注册、维度映射和状态方向性，否则 Codex 实现时容易出现重复版本、未知维度、字符串混乱和单向关系状态误判。
```

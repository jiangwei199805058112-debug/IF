# Codex 任务提示词库

本文档用于记录 IF 后续代码任务的版本号和执行边界。

## 版本号修正

README 当前已经使用 `v0.1.38-v0.1.41` 记录以下文档任务：

```text
v0.1.38 关系系统逻辑审查与优化清单
v0.1.39 问卷维度别名映射表
v0.1.40 关系枚举与字段注册表
v0.1.41 关系记忆衰减与模式阈值规则
```

因此，后续代码任务从 `v0.1.42` 开始，不再使用旧编号 `v0.1.33-v0.1.38`。

## 后续代码任务顺序

```text
v0.1.42 relationship_state_aggregator.py 原型
v0.1.43 aggregator 关键裁决测试补全
v0.1.44 relationship_interpretation.py 接入 aggregator
v0.1.45 冲突沟通事件接入 aggregator
v0.1.46 社会交换/公平轻量接入 aggregator
v0.1.47 问卷补 4 个沟通表露题
```

## 通用边界

- 不做 UI。
- 不接 AI API。
- 不做大规模重构。
- 不破坏当前 14 天控制台原型。
- 新增代码必须有对应测试。
- 代码任务完成后需要更新 README 版本说明。
- 问卷题接入时必须通过维度 ID 检查。

## 重要设计文档

```text
docs/design/34_relationship_state_aggregator_implementation_plan.md
docs/design/35_relationship_event_template_library.md
docs/design/36_questionnaire_expansion_candidate_pool.md
docs/design/37_relationship_report_tag_dictionary.md
docs/design/38_relationship_system_logic_audit_and_optimization_notes.md
docs/design/39_questionnaire_dimension_alias_mapping.md
docs/design/40_relationship_enum_and_field_registry.md
docs/design/41_relationship_memory_decay_and_pattern_rules.md
```

## v0.1.42：relationship_state_aggregator.py 原型

目标文件：

```text
if_game/relationship_state_aggregator.py
tests/relationship_state_aggregator_test.py
README.md
```

最低要求：

- 新增 `RelationshipStateDelta`。
- 新增 `aggregate_relationship_event()`。
- 输出必须保留 `source_id` 和 `target_id`。
- 输出字段至少包含：`trust_delta`、`satisfaction_delta`、`intimacy_delta`、`stability_delta`、`repair_chance_delta`、`old_wound_memory_delta`、`safety_delta`、`excitement_delta`、`fairness_delta`、`dependence_delta`、`report_tags`、`memory_notes`、`debug_reasons`。
- `safety_delta`、`excitement_delta`、`fairness_delta`、`dependence_delta` 第一版可以默认为 0。
- 支持基础输入：事实伤害、欺骗、证据强度、解释准确度、回应性、冲突升级、感受确认、石墙、修复质量、奖赏变化、代价变化、模式键、重复次数、修复状态。

验收重点：

- 普通轻微信任波动不会一次性大扣信任。
- 高欺骗与高伤害会降低信任。
- 石墙会降低修复机会并写入旧伤摘要。
- 高质量修复会提高修复机会。
- 同一欺骗事件不会重复扣信任到过大。
- 输出包含方向字段和预留字段。

## v0.1.43：aggregator 关键裁决测试补全

必须覆盖：

```text
沉默不一定是石墙
石墙是高伤害沟通
吵架但成功修复
怀疑是准确警觉
怀疑是误会/焦虑
隐私不等于欺骗
低痛苦不等于高快乐
高快乐不等于安全
公平不是五五分
同一事件不能重复扣 trust
```

测试以方向断言为主，不要过度依赖精确数值。

## v0.1.44：relationship_interpretation.py 接入 aggregator

目标：

- 保持现有解释原型测试通过。
- 新增轻量转换函数，将解释结果转为 aggregator 输入。
- 不重写现有解释模型。
- 验证准确警觉、误会/焦虑、真实欺骗三种路径。

建议接口：

```text
interpretation_to_aggregator_input(result: dict) -> dict
```

## v0.1.45：冲突沟通事件接入 aggregator

建议事件：

```text
E-CON-01 对方抱怨你迟到
E-CON-02 玩家请求暂停争吵
E-CON-03 一方用嘲讽回应脆弱表达
```

验收重点：

- 精确表达和道歉修复提高修复机会。
- 反向抱怨或防卫降低满意度或修复机会。
- 有效暂停不是石墙。
- 嘲讽脆弱表达增加旧伤记忆。

## v0.1.46：社会交换/公平轻量接入 aggregator

建议支持字段：

```text
relationship_rewards_delta
relationship_costs_delta
approach_reward_delta
avoidance_cost_pressure_delta
boredom_delta
perceived_equity_delta
underbenefit_feeling_delta
taken_for_granted_delta
dependence_delta
```

验收重点：

- 低痛苦不等于高快乐。
- 高快乐不等于安全。
- 安全但沉闷可生成 `safe_but_bored_pattern`。
- 长期获益不足会降低满意度。
- 公平不是五五分。

## v0.1.47：问卷补 4 个沟通表露题

优先题目：

```text
Q-COM-01 自我表露意愿
Q-COM-05 回应性需求
Q-COM-06 哪些事情可以保留不说
Q-COM-10 自己表露 vs 希望对方表露
```

要求：

- 只使用现有 runner/scoring 已支持题型。
- `dimensions` 和 `dimension_effects` 必须使用 16 号 128 维正式 ID。
- 不要直接把 36 号候选别名写进 `dimensions`。
- 必须参考 `39_questionnaire_dimension_alias_mapping.md`。
- 更新 loader、scoring、reporting、runner 相关测试。

## 一句话总结

```text
后续代码从 v0.1.42 开始，优先实现 relationship_state_aggregator.py 原型。
```

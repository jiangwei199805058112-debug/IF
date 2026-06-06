# 2026-06-07 IF 关系系统文档后续任务清单

本文档用于整理 IF 当前已经完成的关系系统文档、后续代码任务、验收重点和交接提示。它不是新系统设计，而是后续执行索引。

---

## 1. 当前状态

当前仓库已经完成并推送以下关系系统设计与交接文档：

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
docs/design/38_relationship_system_logic_audit_and_optimization_notes.md
docs/design/39_questionnaire_dimension_alias_mapping.md
docs/design/40_relationship_enum_and_field_registry.md
docs/design/41_relationship_memory_decay_and_pattern_rules.md
docs/context/codex_task_prompts.md
```

README 已更新文档阅读顺序和 `v0.1.25-v0.1.41` 说明。

当前原则：

```text
代码交给 Codex 恢复额度后做。
当前文档层已经完成一轮闭环。
后续代码任务必须从 v0.1.42 开始，避免与 v0.1.38-v0.1.41 文档任务冲突。
```

---

## 2. 当前系统链路

现阶段关系系统应按以下顺序理解：

```text
25：行为如何被解释
26：伴侣认知是否准确
27：双方如何交换真实信息
28：前期调查如何测沟通和表露
29：冲突中如何表达和修复
30：为什么满意、为什么依赖、为什么离开或留下
31：25-30 的第一轮一致性规则
32：关系是否有快乐、安全、新鲜感，以及如何度过动荡期
33：关系是交换还是共有，付出和结果是否被感到公平
34：将 25-33 收束成 relationship_state_aggregator 的实施方案
35：关系事件模板库
36：问卷扩展候选题池
37：关系报告标签词典
38：25-37 的第二轮逻辑审查与优化清单
39：问卷候选维度到 128 维正式 ID 的别名映射
40：关系枚举、字段和标签注册表
41：重复事件、旧伤记忆、时间衰减和模式阈值规则
```

核心代码实现方向：

```text
relationship_interpretation.py
    ↓
relationship_state_aggregator.py
    ↓
relationship memory / pattern update
    ↓
事件报告 / 关系状态变化 / 后续问卷扩展
```

---

## 3. 后续代码任务顺序

旧计划中的 `v0.1.33-v0.1.38` 代码任务编号已经失效。当前应使用以下顺延版本：

```text
v0.1.42 relationship_state_aggregator.py 原型
v0.1.43 aggregator 关键裁决测试补全
v0.1.44 relationship_interpretation.py 接入 aggregator
v0.1.45 冲突沟通事件接入 aggregator
v0.1.46 社会交换/公平轻量接入 aggregator
v0.1.47 问卷补 4 个沟通表露题
```

---

## 4. v0.1.42：relationship_state_aggregator.py 原型

目标文件：

```text
if_game/relationship_state_aggregator.py
tests/relationship_state_aggregator_test.py
README.md
```

最低目标：

- 新增 `RelationshipStateDelta`。
- 新增 `aggregate_relationship_event()`。
- 支持 dict 输入，避免过度工程化。
- 输出保留 `source_id`、`target_id`，避免玩家/NPC 状态被误写成完全对称。
- 输出包含：
  - `trust_delta`
  - `satisfaction_delta`
  - `intimacy_delta`
  - `stability_delta`
  - `repair_chance_delta`
  - `old_wound_memory_delta`
  - `safety_delta`
  - `excitement_delta`
  - `fairness_delta`
  - `dependence_delta`
  - `report_tags`
  - `memory_notes`
  - `debug_reasons`
- `safety_delta`、`excitement_delta`、`fairness_delta`、`dependence_delta` 第一版可以默认 0，但字段必须存在。
- 支持基础输入：事实伤害、欺骗、证据强度、解释准确度、回应性、冲突升级、感受确认、石墙、修复质量、奖赏变化、代价变化、模式键、重复次数、修复状态。

验收重点：

```text
同一事件不能被多个系统重复扣 trust。
普通事件不能一次性摧毁关系。
输出要可测试、可读、可解释。
输出必须有方向性和预留字段。
```

---

## 5. v0.1.43：aggregator 关键裁决测试

目标文件：

```text
tests/relationship_state_aggregator_test.py
if_game/relationship_state_aggregator.py
README.md
```

必须覆盖：

1. 沉默不一定是石墙；
2. 石墙是高伤害沟通；
3. 吵架但成功修复；
4. 怀疑是准确警觉；
5. 怀疑是误会/焦虑；
6. 隐私不等于欺骗；
7. 低痛苦不等于高快乐；
8. 高快乐不等于安全；
9. 公平不是五五分；
10. 同一事件不能重复扣 `trust_delta`。

测试应以方向断言为主，不要过度依赖具体数值。

---

## 6. v0.1.44：relationship_interpretation.py 接入 aggregator

目标：

- 保持 `relationship_interpretation.py` 现有测试通过。
- 新增轻量转换函数，将解释结果转为 aggregator 输入。
- 不重写整个解释系统。
- 不接完整主流程。

建议接口：

```text
interpretation_to_aggregator_input(result: dict) -> dict
```

验收重点：

```text
现有 relationship_interpretation_test.py 不破。
aggregator 新测试通过。
解释层与聚合层职责分离。
准确警觉、误会/焦虑、真实欺骗三种路径可被聚合器正确处理。
```

---

## 7. v0.1.45：冲突沟通事件轻量接入

目标：

- 增加 2-3 个冲突沟通事件样例。
- 能体现：
  - 暂停不是石墙；
  - 精确表达可修复；
  - 蔑视/人格攻击高伤害。
- 接入 aggregator 结算。
- 暂不做复杂剧情树。

建议事件：

```text
E-CON-01：对方抱怨你迟到
E-CON-02：玩家请求暂停争吵
E-CON-03：一方用嘲讽回应脆弱表达
```

---

## 8. v0.1.46：社会交换/公平轻量接入

目标：

- 增加社会交换和公平的轻量计算。
- 区分：
  - 满意度；
  - 稳定性；
  - 依赖度；
  - 公平感；
  - 安全感；
  - 新鲜感/刺激感。
- 不实现完整 CL/CLalt 大系统，只做原型。

必须覆盖：

```text
低痛苦不等于高快乐。
高快乐不等于安全。
安全但沉闷可生成 safe_but_bored_pattern。
长期获益不足会降低满意度。
公平不是五五分。
```

---

## 9. v0.1.47：问卷补 4 个沟通表露题

优先从 `36_questionnaire_expansion_candidate_pool.md` 中选择：

```text
Q-COM-01：自我表露意愿
Q-COM-05：回应性需求
Q-COM-06：哪些事情可以保留不说
Q-COM-10：自己表露 vs 希望对方表露
```

要求：

- 只轻量加入。
- 不一次性扩展到 40-60 题。
- `dimensions` 和 `dimension_effects` 必须使用 16 号 128 维正式 ID。
- 不要直接使用 36 号候选别名作为问卷维度。
- 必须参考 `39_questionnaire_dimension_alias_mapping.md`。
- 更新 loader/scoring/reporting/runner 测试。
- 保持当前 MVP 可运行。

---

## 10. 已完成的非代码任务

以下非代码任务已经完成，不应再作为待办重复提出：

```text
docs/design/35_relationship_event_template_library.md
docs/design/36_questionnaire_expansion_candidate_pool.md
docs/design/37_relationship_report_tag_dictionary.md
docs/design/38_relationship_system_logic_audit_and_optimization_notes.md
docs/design/39_questionnaire_dimension_alias_mapping.md
docs/design/40_relationship_enum_and_field_registry.md
docs/design/41_relationship_memory_decay_and_pattern_rules.md
docs/context/codex_task_prompts.md
README 索引与版本说明更新
```

---

## 11. 后续 Codex 执行总规则

每次代码任务都必须：

```text
1. 先同步远程 main。
2. 不使用 force push。
3. 不大规模重构。
4. 不接 AI API。
5. 不做 UI。
6. 不破坏当前 14 天控制台原型。
7. 新增代码必须有测试。
8. 文档-only 任务不要求跑 Python 测试。
9. 代码任务至少跑相关测试和文档格式检查。
10. 完成后提交并推送。
```

---

## 12. 一句话总结

```text
当前 IF 已经完成关系系统理论层和代码前置文档层的主体搭建；下一阶段重点是从 v0.1.42 开始，把 relationship_state_aggregator 做成可测试代码原型。
```

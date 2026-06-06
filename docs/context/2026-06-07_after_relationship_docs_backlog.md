# 2026-06-07 IF 关系系统文档后续任务清单

本文档用于在 Codex 额度暂时不可用时，整理 IF 当前已经完成的设计文档、后续代码任务、非代码任务、验收标准和交接提示。它不是新系统设计，而是后续执行索引。

---

## 1. 当前状态

当前仓库已经完成并推送以下关系系统设计文档：

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
```

README 已更新文档阅读顺序和 v0.1.25-v0.1.32 说明。

当前原则：

```text
代码交给 Codex 恢复额度后做；
当前阶段优先完成设计整理、任务拆分、验收标准、测试用例草案和交接文档。
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
31：以上系统如何避免冲突和重复扣分
32：关系是否有快乐、安全、新鲜感，以及如何度过动荡期
33：关系是交换还是共有，付出和结果是否被感到公平
34：将 25-33 收束成 relationship_state_aggregator 的实施方案
```

核心代码实现方向：

```text
relationship_interpretation.py
    ↓
relationship_state_aggregator.py
    ↓
事件报告 / 关系状态变化 / 后续问卷扩展
```

---

## 3. 后续代码任务顺序

### 3.1 v0.1.33：relationship_state_aggregator.py 原型

目标文件：

```text
if_game/relationship_state_aggregator.py
tests/relationship_state_aggregator_test.py
```

最低目标：

- 新增 `RelationshipStateDelta`；
- 新增 `aggregate_relationship_event()`；
- 支持最小输入字段：
  - `truth_harm_level`
  - `deception_level`
  - `evidence_chain_strength`
  - `interpretation_accuracy`
  - `perceived_responsiveness`
  - `conflict_escalation_risk`
  - `validation_skill`
  - `stonewalling_level`
  - `repair_attempt_quality`
  - `relationship_rewards_delta`
  - `relationship_costs_delta`
- 输出：
  - `trust_delta`
  - `satisfaction_delta`
  - `intimacy_delta`
  - `stability_delta`
  - `repair_chance_delta`
  - `old_wound_memory_delta`
  - `report_tags`
  - `debug_reasons`

验收重点：

```text
同一事件不能被多个系统重复扣 trust。
普通事件不能一次性摧毁关系。
输出要可测试、可读、可解释。
```

---

### 3.2 v0.1.34：aggregator 关键裁决测试

新增或补充：

```text
tests/relationship_state_aggregator_test.py
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

---

### 3.3 v0.1.35：relationship_interpretation.py 接入 aggregator

目标：

- 保持 `relationship_interpretation.py` 现有测试通过；
- 新增一个转换函数，将解释结果转为 aggregator 输入；
- 不重写整个解释系统；
- 不接 AI API；
- 不接完整主流程。

建议接口：

```python
def interpretation_to_aggregator_input(result: dict) -> dict:
    ...
```

验收重点：

```text
现有 relationship_interpretation_test.py 不破。
aggregator 新测试通过。
解释层与聚合层职责分离。
```

---

### 3.4 v0.1.36：冲突沟通事件轻量接入

目标：

- 增加 2-3 个冲突沟通事件样例；
- 能体现：
  - 暂停不是石墙；
  - 精确表达可修复；
  - 蔑视/人格攻击高伤害；
- 接入 aggregator 结算；
- 暂不做复杂剧情树。

---

### 3.5 v0.1.37：社会交换/公平轻量接入

目标：

- 增加社会交换和公平的轻量计算；
- 区分：
  - 满意度；
  - 稳定性；
  - 依赖度；
  - 公平感；
- 不实现完整 CL/CLalt 大系统，只做原型。

---

### 3.6 v0.1.38：问卷补 4 个沟通表露题

优先从 `28_questionnaire_communication_disclosure_module.md` 中选择：

```text
Q-COM-01：自我表露意愿
Q-COM-05：回应性需求
Q-COM-06：哪些事情可以保留不说
Q-COM-10：自己表露 vs 希望对方表露
```

要求：

- 只轻量加入；
- 不一次性扩展到 40-60 题；
- 更新 loader/scoring/reporting/runner 测试；
- 保持当前 MVP 可运行。

---

## 4. 非代码任务清单

当前不用 Codex 也能继续做的事：

### 4.1 事件模板库整理

建议新增：

```text
docs/design/35_relationship_event_template_library.md
```

内容按系统归类：

- 认知误读事件；
- 表露与回应事件；
- 秘密与隐私事件；
- 冲突修复事件；
- 社会交换事件；
- 沉闷与新鲜感事件；
- 公平与家务照料事件。

### 4.2 问卷补题候选池

建议新增：

```text
docs/design/36_questionnaire_expansion_candidate_pool.md
```

内容：

- 沟通表露 10 题；
- 冲突修复 10 题；
- 社会交换/替代选择 10 题；
- 新鲜感/沉闷 10 题；
- 公平/共有关系 10 题。

这只是候选池，不直接修改 `questionnaire_mvp.json`。

### 4.3 报告标签词典

建议新增：

```text
docs/design/37_relationship_report_tag_dictionary.md
```

内容：

- 标签 ID；
- 中文标签；
- 正面写法；
- 风险写法；
- 禁止写法；
- 来源系统；
- 触发条件草案。

### 4.4 Codex 任务提示词库

建议新增：

```text
docs/context/codex_task_prompts.md
```

内容：

- v0.1.33 聚合器原型任务提示；
- v0.1.34 测试任务提示；
- v0.1.35 接入任务提示；
- v0.1.38 问卷补题任务提示。

---

## 5. 当前优先级

如果继续做非代码文档，建议顺序：

```text
1. docs/design/35_relationship_event_template_library.md
2. docs/design/37_relationship_report_tag_dictionary.md
3. docs/context/codex_task_prompts.md
4. docs/design/36_questionnaire_expansion_candidate_pool.md
```

理由：

- 事件模板库能直接服务代码实现和剧情设计；
- 报告标签词典能避免输出伤人、诊断化或道德审判；
- Codex 提示词库能让后续代码任务直接开始；
- 问卷候选池可以晚一点，因为当前 25 题 MVP 已经可运行。

---

## 6. 后续 Codex 执行总规则

每次代码任务都必须：

```text
1. 先 git pull --rebase origin main
2. 不 force push
3. 不大规模重构
4. 不接 AI API
5. 不做 UI
6. 不破坏当前 14 天控制台原型
7. 新增代码必须有测试
8. 文档-only 任务不要求跑 Python 测试
9. 代码任务至少跑相关测试和 git diff --check
10. 完成后提交并推送
```

---

## 7. 一句话总结

```text
当前 IF 已经完成关系系统理论层的主体搭建；下一阶段重点不是继续无限加理论，而是把这些文档整理成事件模板、报告标签、Codex 工单和 relationship_state_aggregator 的可测试代码实现。
```

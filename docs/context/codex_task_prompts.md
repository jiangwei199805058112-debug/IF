# Codex 任务提示词库

本文档用于在 Codex 额度恢复后，直接复制给 Codex 执行后续代码任务。所有任务均基于当前 IF 仓库状态：

```text
D:\youxi\IF
```

当前重要设计文档：

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
docs/design/37_relationship_report_tag_dictionary.md
```

---

## 1. 通用执行规则

每次给 Codex 的任务都必须遵守：

```text
1. 先执行 git status --short。
2. 如果工作区不干净，先汇报，不要直接覆盖。
3. 执行 git pull --rebase origin main。
4. 禁止 force push。
5. 不接 AI API。
6. 不做 UI。
7. 不大规模重构。
8. 不破坏当前 14 天控制台原型。
9. 不删除既有文档和测试。
10. 新增代码必须新增或更新测试。
11. 文档-only 任务不需要跑 Python 测试，但要跑 git diff --check。
12. 代码任务至少跑相关测试和 git diff --check。
13. 完成后提交并推送。
14. 最后汇报 commit SHA、修改文件、测试结果、git status --short。
```

---

## 2. 任务 v0.1.33：relationship_state_aggregator.py 原型

### 2.1 可直接复制给 Codex 的提示词

```text
当前仓库：D:\youxi\IF

任务：实现 v0.1.33 relationship_state_aggregator.py 原型。

开始前请执行：
1. git status --short
2. git pull --rebase origin main

禁止：
- 禁止 force push
- 禁止接 AI API
- 禁止做 UI
- 禁止大规模重构
- 禁止破坏当前 14 天控制台原型
- 禁止修改问卷 JSON

请先阅读：
- docs/design/31_system_integration_consistency_rules.md
- docs/design/34_relationship_state_aggregator_implementation_plan.md
- docs/design/35_relationship_event_template_library.md
- docs/design/37_relationship_report_tag_dictionary.md

目标文件：
- 新增 if_game/relationship_state_aggregator.py
- 新增 tests/relationship_state_aggregator_test.py
- 更新 README.md，增加 v0.1.33 简短说明

MVP 要求：
1. 新增 RelationshipStateDelta dataclass，至少包含：
   - trust_delta
   - satisfaction_delta
   - intimacy_delta
   - stability_delta
   - repair_chance_delta
   - old_wound_memory_delta
   - report_tags
   - debug_reasons
2. 新增 aggregate_relationship_event(...) 函数。
3. 函数先支持 dict 输入即可，不要过度工程化。
4. 支持以下输入字段：
   - truth_harm_level
   - deception_level
   - evidence_chain_strength
   - interpretation_accuracy
   - perceived_responsiveness
   - conflict_escalation_risk
   - validation_skill
   - stonewalling_level
   - repair_attempt_quality
   - relationship_rewards_delta
   - relationship_costs_delta
5. 实现基础裁决规则：
   - 隐私不等于欺骗；
   - 有效修复能提高 repair_chance_delta；
   - 石墙降低 trust/satisfaction/repair_chance，并提高 old_wound_memory_delta；
   - 真实伤害和欺骗由 trust_delta 主责，不要被其他系统重复扣到过大；
   - 普通事件单项 delta 控制在 -10 到 +10；重大事件可到 -20。
6. 输出必须包含 debug_reasons，说明每个主要变化来自什么规则。

测试要求：
至少覆盖：
1. 普通轻微信任波动不会一次性大扣 trust；
2. 高欺骗 + 高伤害会降低 trust；
3. 石墙会降低 repair_chance 并写旧伤；
4. 高质量修复会提高 repair_chance；
5. 同一欺骗事件不会重复扣 trust 到过大。

运行测试：
- python tests/relationship_state_aggregator_test.py
- python tests/relationship_interpretation_test.py
- python tests/smoke_test.py
- git diff --check

提交：
- git add README.md if_game/relationship_state_aggregator.py tests/relationship_state_aggregator_test.py
- git commit -m "feat: 增加关系状态聚合器原型"
- git push origin main

完成后汇报：
- commit SHA
- 修改文件列表
- 测试结果
- git status --short
```

---

## 3. 任务 v0.1.34：aggregator 关键裁决测试补全

### 3.1 可直接复制给 Codex 的提示词

```text
当前仓库：D:\youxi\IF

任务：实现 v0.1.34 aggregator 关键裁决测试补全。

开始前请执行：
1. git status --short
2. git pull --rebase origin main

禁止：
- 禁止 force push
- 禁止接 AI API
- 禁止做 UI
- 禁止大规模重构
- 禁止修改问卷 JSON

请先阅读：
- docs/design/34_relationship_state_aggregator_implementation_plan.md
- docs/design/35_relationship_event_template_library.md
- docs/design/37_relationship_report_tag_dictionary.md
- if_game/relationship_state_aggregator.py
- tests/relationship_state_aggregator_test.py

目标：
补全 tests/relationship_state_aggregator_test.py 中的关键裁决测试。

必须覆盖以下 10 个用例：
1. 沉默不一定是石墙；
2. 石墙是高伤害沟通；
3. 吵架但成功修复；
4. 怀疑是准确警觉；
5. 怀疑是误会/焦虑；
6. 隐私不等于欺骗；
7. 低痛苦不等于高快乐；
8. 高快乐不等于安全；
9. 公平不是五五分；
10. 同一事件不能重复扣 trust。

如果当前 aggregator 还没有部分字段，可以用轻量方式补充输入字段和输出字段，但不要大重构。

重点：
- 测试要表达规则，而不是只追求覆盖率。
- 如果补充字段，保持向后兼容。
- 不要把测试写得太脆弱，避免依赖过多具体数值；可以用方向断言，例如 > 0、< 0、包含/不包含标签。

运行测试：
- python tests/relationship_state_aggregator_test.py
- python tests/relationship_interpretation_test.py
- python tests/smoke_test.py
- git diff --check

提交：
- git add if_game/relationship_state_aggregator.py tests/relationship_state_aggregator_test.py README.md
- git commit -m "test: 补充关系状态聚合器裁决用例"
- git push origin main

完成后汇报：
- commit SHA
- 修改文件列表
- 测试结果
- git status --short
```

---

## 4. 任务 v0.1.35：relationship_interpretation.py 接入 aggregator

### 4.1 可直接复制给 Codex 的提示词

```text
当前仓库：D:\youxi\IF

任务：实现 v0.1.35 relationship_interpretation.py 接入 aggregator。

开始前请执行：
1. git status --short
2. git pull --rebase origin main

禁止：
- 禁止 force push
- 禁止接 AI API
- 禁止做 UI
- 禁止重写整个解释系统
- 禁止破坏现有 relationship_interpretation_test.py
- 禁止修改问卷 JSON

请先阅读：
- docs/design/25_attribution_memory_belief_system.md
- docs/design/31_system_integration_consistency_rules.md
- docs/design/34_relationship_state_aggregator_implementation_plan.md
- if_game/relationship_interpretation.py
- if_game/relationship_state_aggregator.py

目标：
让 relationship_interpretation.py 的解释结果可以转换为 relationship_state_aggregator 的输入。

建议新增函数：

```python
def interpretation_to_aggregator_input(result: dict) -> dict:
    ...
```

或使用现有结构做等价轻量实现。

要求：
1. 保持现有解释原型测试通过。
2. 不重写现有解释模型。
3. 新增 2-3 个测试，验证：
   - 准确警觉能传入 aggregator 并生成合适标签；
   - 误会/焦虑不会大幅扣 trust；
   - 真实欺骗能让 aggregator 产生 trust_delta 下降。
4. README 增加 v0.1.35 简短说明。

运行测试：
- python tests/relationship_interpretation_test.py
- python tests/relationship_state_aggregator_test.py
- python tests/smoke_test.py
- git diff --check

提交：
- git add README.md if_game/relationship_interpretation.py if_game/relationship_state_aggregator.py tests/relationship_interpretation_test.py tests/relationship_state_aggregator_test.py
- git commit -m "feat: 接入关系解释与状态聚合器"
- git push origin main

完成后汇报：
- commit SHA
- 修改文件列表
- 测试结果
- git status --short
```

---

## 5. 任务 v0.1.36：冲突沟通事件接入 aggregator

### 5.1 可直接复制给 Codex 的提示词

```text
当前仓库：D:\youxi\IF

任务：实现 v0.1.36 冲突沟通事件轻量接入 aggregator。

开始前请执行：
1. git status --short
2. git pull --rebase origin main

禁止：
- 禁止 force push
- 禁止接 AI API
- 禁止做 UI
- 禁止复杂剧情树
- 禁止大规模重构
- 禁止修改问卷 JSON

请先阅读：
- docs/design/29_conflict_communication_repair_system.md
- docs/design/34_relationship_state_aggregator_implementation_plan.md
- docs/design/35_relationship_event_template_library.md
- if_game/relationship_state_aggregator.py

目标：
增加 2-3 个冲突沟通事件样例，并通过 aggregator 结算。

建议事件：
1. E-CON-01：对方抱怨你迟到；
2. E-CON-02：玩家请求暂停争吵；
3. E-CON-03：一方用嘲讽回应脆弱表达。

实现方式：
- 可以新增轻量模块 if_game/conflict_event_samples.py，或在测试中用事件 dict 表示；
- 不需要完整事件引擎；
- 重点是让事件样例可以转换为 aggregator 输入，并验证输出方向。

测试要求：
1. 精确表达 + 道歉修复 → repair_chance_delta > 0；
2. 反向抱怨/防卫 → satisfaction_delta 或 repair_chance_delta 下降；
3. 有效暂停不是石墙；
4. 嘲讽脆弱表达 → old_wound_memory_delta 上升。

运行测试：
- python tests/relationship_state_aggregator_test.py
- python tests/relationship_interpretation_test.py
- python tests/smoke_test.py
- git diff --check

提交：
- git add README.md if_game/relationship_state_aggregator.py tests/relationship_state_aggregator_test.py
- 如新增样例模块也加入 git add
- git commit -m "feat: 增加冲突沟通事件聚合样例"
- git push origin main

完成后汇报：
- commit SHA
- 修改文件列表
- 测试结果
- git status --short
```

---

## 6. 任务 v0.1.37：社会交换/公平轻量接入 aggregator

### 6.1 可直接复制给 Codex 的提示词

```text
当前仓库：D:\youxi\IF

任务：实现 v0.1.37 社会交换与公平系统轻量接入 aggregator。

开始前请执行：
1. git status --short
2. git pull --rebase origin main

禁止：
- 禁止 force push
- 禁止接 AI API
- 禁止做 UI
- 禁止完整 CL/CLalt 大系统
- 禁止大规模重构
- 禁止修改问卷 JSON

请先阅读：
- docs/design/30_social_exchange_dependency_system.md
- docs/design/32_approach_avoidance_turbulence_system.md
- docs/design/33_communal_exchange_equity_system.md
- docs/design/34_relationship_state_aggregator_implementation_plan.md
- docs/design/35_relationship_event_template_library.md
- if_game/relationship_state_aggregator.py

目标：
在 aggregator 中轻量支持社会交换、公平、沉闷和高刺激风险的输入字段。

建议新增或支持字段：
- relationship_rewards_delta
- relationship_costs_delta
- approach_reward_delta
- avoidance_cost_pressure_delta
- boredom_delta
- perceived_equity_delta
- underbenefit_feeling_delta
- taken_for_granted_delta
- dependence_delta 可选

必须验证：
1. 低痛苦不等于高快乐；
2. 高快乐不等于安全；
3. 安全但沉闷可生成 safe_but_bored_pattern；
4. 长期获益不足会降低 satisfaction_delta；
5. 公平不是五五分。

运行测试：
- python tests/relationship_state_aggregator_test.py
- python tests/smoke_test.py
- git diff --check

提交：
- git add README.md if_game/relationship_state_aggregator.py tests/relationship_state_aggregator_test.py
- git commit -m "feat: 轻量接入社会交换与公平聚合规则"
- git push origin main

完成后汇报：
- commit SHA
- 修改文件列表
- 测试结果
- git status --short
```

---

## 7. 任务 v0.1.38：问卷补 4 个沟通表露题

### 7.1 可直接复制给 Codex 的提示词

```text
当前仓库：D:\youxi\IF

任务：实现 v0.1.38 问卷补 4 个沟通表露题。

开始前请执行：
1. git status --short
2. git pull --rebase origin main

禁止：
- 禁止 force push
- 禁止接 AI API
- 禁止做 UI
- 禁止一次性扩展到 40-60 题
- 禁止重写完整问卷系统

请先阅读：
- docs/design/28_questionnaire_communication_disclosure_module.md
- docs/design/37_relationship_report_tag_dictionary.md
- if_game/data/questionnaire_mvp.json
- if_game/questionnaire/loader.py
- if_game/questionnaire/scoring.py
- if_game/questionnaire/reporting.py
- if_game/questionnaire/runner.py

目标：
在当前 25 题 MVP 问卷基础上，轻量新增 4 个沟通表露题。

优先题目：
1. Q-COM-01：自我表露意愿；
2. Q-COM-05：回应性需求；
3. Q-COM-06：哪些事情可以保留不说；
4. Q-COM-10：自己表露 vs 希望对方表露。

要求：
1. 题目 ID 使用当前项目规则，避免与既有题号冲突。
2. 只使用现有 runner/scoring 已支持题型：
   - forced_single
   - primary_with_secondary
   - multi_with_primary
   - slider
   - axis_2d
3. 更新测试中题目数量断言。
4. 更新报告输出，至少能在关键维度摘要或风险提示中体现部分新维度。
5. README 增加 v0.1.38 简短说明。

运行测试：
- python scripts/check_questionnaire_dimension_ids.py
- python tests/questionnaire_loader_test.py
- python tests/questionnaire_scoring_test.py
- python tests/questionnaire_reporting_test.py
- python tests/questionnaire_runner_test.py
- python tests/smoke_test.py
- git diff --check

提交：
- git add README.md if_game/data/questionnaire_mvp.json if_game/questionnaire/scoring.py if_game/questionnaire/reporting.py tests/questionnaire_loader_test.py tests/questionnaire_scoring_test.py tests/questionnaire_reporting_test.py tests/questionnaire_runner_test.py
- 如有其他必要文件也加入
- git commit -m "feat: 补充沟通表露问卷题"
- git push origin main

完成后汇报：
- commit SHA
- 修改文件列表
- 测试结果
- git status --short
```

---

## 8. 文档-only 任务：README 更新

### 8.1 可直接复制给 Codex 的提示词

```text
当前仓库：D:\youxi\IF

任务：文档-only，更新 README 设计文档索引。

开始前请执行：
1. git status --short
2. git pull --rebase origin main

目标：
把以下文档加入 README 的文档阅读顺序和版本说明：
- docs/design/34_relationship_state_aggregator_implementation_plan.md
- docs/design/35_relationship_event_template_library.md
- docs/design/37_relationship_report_tag_dictionary.md
- docs/context/2026-06-07_after_relationship_docs_backlog.md
- docs/context/codex_task_prompts.md

要求：
- 只改 README.md
- 不修改 Python 代码
- 不跑 Python 测试
- 运行 git diff --check

提交：
- git add README.md
- git commit -m "docs: 更新README后续设计文档索引"
- git push origin main

完成后汇报：
- commit SHA
- 修改文件列表
- git diff --check 结果
- git status --short
```

---

## 9. 一句话总结

```text
本文件的作用是把 IF 后续代码任务变成可复制给 Codex 的执行工单，避免额度恢复后重新解释上下文、重新拆任务或一次性大改。
```

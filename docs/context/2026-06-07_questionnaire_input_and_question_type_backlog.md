# 问卷题型与输入校验待办

本文档记录一次真实问卷试玩中发现的问题：部分问卷题目当前被设计为单选，但玩家实际体验中可能存在多个选项同时成立；同时，控制台输入校验对字母、逗号和异常输入的处理需要更清晰。

本文件作为后续 Codex 额度恢复后的待处理项。处理前应先读取：

```text
docs/context/current_task_ledger.md
docs/context/2026-06-07_questionnaire_game_integration_backlog.md
if_game/data/questionnaire_mvp.json
if_game/questionnaire/runner.py
if_game/questionnaire/scoring.py
if_game/questionnaire/reporting.py
tests/questionnaire_loader_test.py
tests/questionnaire_scoring_test.py
tests/questionnaire_reporting_test.py
tests/questionnaire_runner_test.py
```

---

## 1. 发现的问题：Q024 不应强制单选

试玩题目：

```text
第 22/29 题 Q024：被别人依赖
如果伴侣经常依赖你、需要你安慰和帮忙，你通常会怎么感受？
1. A 会觉得被信任，愿意承担。
2. B 可以接受，但希望有边界。
3. C 一开始愿意，久了会累。
4. D 压力很大，会想逃开。
5. E 会觉得对方离不开我，关系更稳。
```

玩家输入：

```text
1,5
```

当前系统反馈：

```text
输入有误：该题只能选择一个选项 请重新输入。
```

玩家反馈：

```text
这种问题我觉得可以选两个都是有可能的。
```

判断：玩家反馈成立。Q024 中：

```text
A 会觉得被信任，愿意承担
E 会觉得对方离不开我，关系更稳
```

两者可以同时成立，并不互斥。一个人可以既愿意承担，也从被依赖中获得安全感或关系稳定感。

---

## 2. 建议调整

### 2.1 Q024 改为主选项 + 次选项

建议把 Q024 从强制单选改为：

```text
selection_mode: primary_with_secondary
```

玩家可以输入：

```text
1
1,5
2,3
```

其中第一个为主反应，后续为次反应。

理由：

```text
被依赖后的感受通常不是单一情绪，而是混合体验：被信任、压力、稳定感、疲惫、边界需求可以同时存在。
```

### 2.2 不建议直接改成普通多选

不建议把 Q024 改成纯 `multi_with_primary`，因为它仍需要一个主反应，否则后续计分会失去方向。

更合适的是：

```text
primary_with_secondary
```

---

## 3. 可能影响的计分维度

Q024 当前若支持次选项，建议：

```text
主选项：完整权重
次选项：较低权重，例如 0.4 或 0.5
```

可能涉及维度：

```text
attachment_closeness_need
attachment_independence_need
emotion_caretaking_tendency
relationship_dependency_comfort
power_control_need
emotion_overload_sensitivity
```

如果部分维度不在 128 维正式表中，必须参考：

```text
docs/design/16_questionnaire_dimension_table.md
docs/design/39_questionnaire_dimension_alias_mapping.md
```

不要直接把未注册候选别名写进 `dimensions`。

---

## 4. 同次试玩中观察到的输入体验问题

### 4.1 字母输入与数字提示不一致

部分题提示：

```text
输入一个选项序号，例如：1
```

但玩家输入了：

```text
A
```

系统没有明显报错，似乎可以接受字母选项。

建议统一说明：

```text
请输入选项序号或字母，例如：1 或 A
```

如果系统实际不支持字母，则应明确报错。

### 4.2 多选输入的异常逗号

试玩中出现：

```text
1,2,3,4,,7
,4
,2
```

系统部分情况下继续进入下一题。建议确认当前 runner 是否会自动忽略空项。

可接受策略有两种：

```text
A. 宽容输入：自动忽略空项，但提示“已忽略空输入”。
B. 严格输入：出现空项时报错并要求重新输入。
```

建议当前控制台 MVP 使用宽容输入，但要避免悄悄误解玩家输入。

---

## 5. 建议后续版本

建议作为小修任务：

```text
v0.1.56 问卷题型与输入校验修正
```

如果 `current_task_ledger.md` 中已有新的版本号安排，以账本为准。

---

## 6. Codex 任务提示词草案

```text
当前仓库：D:\youxi\IF

任务：修正问卷 Q024 题型与控制台输入提示。

开始前：
1. git status --short
2. git pull --ff-only origin main
3. 读取 docs/context/current_task_ledger.md
4. 读取 docs/context/2026-06-07_questionnaire_input_and_question_type_backlog.md

禁止：
- 禁止 force push
- 禁止 reset --hard
- 禁止接 AI API
- 禁止做 UI
- 禁止扩展大型问卷题库
- 禁止重写问卷系统

目标：
1. 将 Q024 从强制单选调整为主选项 + 次选项，允许如 1,5 这类输入。
2. 保持第一个选项为主反应，后续选项为次反应。
3. 更新 runner 提示，使玩家知道可以输入数字或字母；如果不支持字母，就改为明确只支持数字。
4. 检查多余逗号输入，如 `1,2,,4`、`,4`，决定宽容处理或严格报错，并写测试固定行为。
5. 更新 scoring/reporting/runner 相关测试。

必须测试：
python scripts/check_questionnaire_dimension_ids.py
python tests/questionnaire_loader_test.py
python tests/questionnaire_scoring_test.py
python tests/questionnaire_reporting_test.py
python tests/questionnaire_runner_test.py
python tests/questionnaire_initial_modifiers_test.py
python tests/smoke_test.py
git diff --check

README：
追加简短说明：问卷 Q024 支持主反应 + 次反应，控制台输入提示更明确。

current_task_ledger.md：
记录该小修已完成、测试结果和下一步建议。

提交：
git add README.md docs/context/current_task_ledger.md docs/context/2026-06-07_questionnaire_input_and_question_type_backlog.md if_game/data/questionnaire_mvp.json if_game/questionnaire/runner.py if_game/questionnaire/scoring.py tests/questionnaire_loader_test.py tests/questionnaire_scoring_test.py tests/questionnaire_reporting_test.py tests/questionnaire_runner_test.py
实际修改文件按 git status --short 调整。
git commit -m "fix: 调整问卷题型与输入校验"
git push origin main
```

---

## 7. 当前结论

Q024 当前强制单选不够自然。玩家反馈合理，应改为“主选项 + 次选项”。

这不是大系统问题，而是问卷题型精细化问题。后续应作为小修处理，不需要大改问卷结构。

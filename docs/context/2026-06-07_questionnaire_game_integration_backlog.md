# 问卷系统未接入互动开局待办

本文档记录一次真实试玩后发现的问题：问卷系统已经有独立入口、计分、报告和初始倾向修正，但尚未接入“互动运行 14 天”的开局流程。

本文件作为后续 Codex 额度恢复后的待处理项。进入下一步前，应先读取：

```text
docs/context/current_task_ledger.md
README.md
if_game/main.py
if_game/engine.py
if_game/questionnaire/runner.py
if_game/questionnaire/scoring.py
if_game/questionnaire/reporting.py
if_game/questionnaire/initial_modifiers.py
```

---

## 1. 问题描述

当前运行：

```powershell
python -m if_game.main
```

主菜单显示：

```text
1. 互动运行 14 天
2. 运行内置场景测试摘要
3. 回答问卷 MVP 快速版
```

实际逻辑是：

```text
选择 1：直接进入 14 天互动运行。
选择 3：只运行独立问卷 MVP。
```

因此，问卷系统没有自动参与 14 天互动开局。

玩家直观感受是：

```text
为什么调查系统 / 问卷系统没有接入这个游戏？
```

---

## 2. 当前已完成但尚未串联的能力

### 2.1 已完成

当前项目已经具备：

```text
问卷入口
问卷配置读取
问卷计分
问卷报告
问卷初始倾向修正
14 天互动流程
relationship_state_aggregator 接入 14 天报告路径
RelationshipMemory MVP
NPC 反应与试玩观察旁路样例
```

其中 `if_game/questionnaire/initial_modifiers.py` 已经提供：

```text
build_initial_relationship_modifiers(score_result)
apply_initial_modifiers(base_state, modifiers)
format_initial_modifier_summary(modifiers)
```

可以生成：

```text
trust_baseline_delta
intimacy_need_delta
conflict_repair_tendency_delta
privacy_boundary_sensitivity_delta
reassurance_need_delta
suspicion_sensitivity_delta
disclosure_willingness_delta
```

### 2.2 尚未完成

尚未完成的是最后一段接线：

```text
开局先答问卷
→ 生成 score_result
→ 生成 initial_modifiers
→ 注入 14 天互动运行
→ transcript / report 开头显示“本局开局倾向”
→ 后续事件继续覆盖问卷自述
```

---

## 3. 设计原则

后续接入时必须保持以下原则：

```text
问卷结果 = 初始倾向
游戏行为 = 动态证据
重复行为 > 单题自述
关键事件 > 抽象自评
```

禁止把问卷结果当成永久人格定论。

问卷可以影响开局倾向，但不能覆盖后续事件选择、NPC 反应和关系记忆。

---

## 4. 建议版本

建议作为下一轮小修版本：

```text
v0.1.55 开局问卷接入 14 天互动流程
```

如果 `current_task_ledger.md` 中已有新的版本号安排，应以账本为准，但任务名称建议保留：

```text
开局问卷接入 14 天互动流程
```

---

## 5. 建议实现方案

### 5.1 main.py 交互改动

在选择：

```text
1. 互动运行 14 天
```

之后，增加提示：

```text
是否先回答问卷，生成本局初始倾向？
1. 是
2. 否
直接回车使用第 2 项：
```

如果选择否，保持当前旧流程完全不变。

如果选择是：

```text
运行问卷 MVP
生成 score_result
调用 build_initial_relationship_modifiers(score_result)
调用 format_initial_modifier_summary(modifiers)
把 modifiers 或 summary 传入 run_14_day_simulation
```

### 5.2 runner.py 改动建议

当前 `run_questionnaire()` 主要面向独立控制台输出。后续可新增一个可复用函数，例如：

```python
def collect_questionnaire_result() -> dict:
    ...
```

或者让 `run_questionnaire()` 可选返回：

```python
return_result=True
```

要求：

```text
不要破坏当前独立问卷入口。
```

### 5.3 engine.py 改动建议

轻量扩展：

```python
def run_14_day_simulation(..., initial_modifiers: dict | None = None):
    ...
```

在 transcript 开头加入：

```text
本局开局倾向：
- 遇到不确定回应时，开局更需要明确安抚和说明。
- 手机、私人信息和个人空间边界会更早影响相处感受。
- 这些只是开局倾向，后续关键事件和重复行为会继续修正。
```

如果不传 `initial_modifiers`，不显示该段，保持旧行为。

---

## 6. 测试要求

后续实现至少补充以下测试：

```text
1. 不答问卷时，14 天互动流程仍保持旧兼容。
2. 传入 initial_modifiers 时，transcript 包含“本局开局倾向”或等价文本。
3. 问卷独立入口仍可运行。
4. initial_modifiers 摘要不包含诊断式语言。
5. 问卷修正不会覆盖后续事件行为。
```

建议运行：

```powershell
python scripts/check_questionnaire_dimension_ids.py
python tests/questionnaire_loader_test.py
python tests/questionnaire_scoring_test.py
python tests/questionnaire_reporting_test.py
python tests/questionnaire_runner_test.py
python tests/questionnaire_initial_modifiers_test.py
python tests/relationship_state_aggregator_test.py
python tests/relationship_interpretation_test.py
python tests/relationship_memory_test.py
python tests/smoke_test.py
python tests/scenario_test.py
python tests/reporting_test.py
git diff --check
```

---

## 7. README 更新建议

实现后在 README 追加说明：

```markdown
## v0.1.55 开局问卷接入 14 天互动流程

互动运行 14 天时，现在可以选择先回答问卷，并将问卷结果转成本局初始关系倾向修正。问卷独立入口仍保留。问卷结果只作为开局倾向，不作为永久人格定论；后续事件选择、NPC 反应和关系记忆仍会继续修正关系状态。
```

---

## 8. Codex 任务提示词草案

```text
当前仓库：D:\youxi\IF

任务：实现开局问卷接入 14 天互动流程。

开始前：
1. git status --short
2. git pull --ff-only origin main
3. 读取 docs/context/current_task_ledger.md
4. 读取 docs/context/2026-06-07_questionnaire_game_integration_backlog.md

禁止：
- 禁止 force push
- 禁止 reset --hard
- 禁止接 AI API
- 禁止做 UI
- 禁止大规模重构
- 禁止删除当前独立问卷入口
- 禁止破坏当前 14 天控制台原型

目标：
让互动运行 14 天时，可以选择先回答问卷，并把问卷结果转成初始关系倾向修正。

实现要求：
1. 保留主菜单第 3 项“回答问卷 MVP 快速版”作为独立入口。
2. 在选择“互动运行 14 天”后，增加是否先回答问卷的提示。
3. 如果选择是，调用问卷流程，得到 score_result。
4. 调用 build_initial_relationship_modifiers(score_result)。
5. 调用 format_initial_modifier_summary(modifiers)。
6. 把 modifiers 或 summary 传给 run_14_day_simulation。
7. transcript 开头显示“本局开局倾向”。
8. 如果选择否，旧流程不变。
9. 玩家可见文本不使用心理诊断式语言。

测试：
python scripts/check_questionnaire_dimension_ids.py
python tests/questionnaire_loader_test.py
python tests/questionnaire_scoring_test.py
python tests/questionnaire_reporting_test.py
python tests/questionnaire_runner_test.py
python tests/questionnaire_initial_modifiers_test.py
python tests/relationship_state_aggregator_test.py
python tests/relationship_interpretation_test.py
python tests/relationship_memory_test.py
python tests/smoke_test.py
python tests/scenario_test.py
python tests/reporting_test.py
git diff --check

README：
追加对应版本说明。

current_task_ledger.md：
记录本待办已处理、测试结果和下一步建议。

提交：
git add README.md docs/context/current_task_ledger.md if_game/main.py if_game/engine.py if_game/questionnaire/runner.py tests/smoke_test.py tests/scenario_test.py tests/reporting_test.py tests/questionnaire_runner_test.py
实际修改文件按 git status --short 调整。
git commit -m "feat: 接入开局问卷初始倾向"
git push origin main
```

---

## 9. 当前结论

当前不是“问卷系统没做”，而是：

```text
问卷入口、计分、报告、初始修正都已存在。
但问卷初始修正尚未注入 14 天互动开局。
```

因此后续应优先做“开局问卷接入 14 天互动流程”，而不是继续扩问卷题库或大改底层结构。

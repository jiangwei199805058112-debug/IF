# 问卷 Q007 公开程度选项待补

本文档记录一次开局问卷真实试玩中发现的问题：`Q007：公开程度` 当前覆盖了“对方公开、自己不一定想公开”的不对称情况，但缺少相反方向，即“自己想公开，但对方不想公开”。

本文件作为后续 Codex 额度恢复后的待处理项。处理前应先读取：

```text
docs/context/current_task_ledger.md
if_game/data/questionnaire_mvp.json
if_game/questionnaire/scoring.py
if_game/questionnaire/reporting.py
tests/questionnaire_loader_test.py
tests/questionnaire_scoring_test.py
tests/questionnaire_reporting_test.py
tests/questionnaire_runner_test.py
```

---

## 1. 发现的问题

当前题目：

```text
Q007：公开程度
如果你们进入或已经处在恋爱关系中，你更倾向于多公开？
1. A 希望自然公开，朋友知道也没关系。
2. B 希望重要朋友知道，但不必发朋友圈。
3. C 先低调，等稳定再公开。
4. D 不太想公开，关系是两个人的事。
5. E 希望对方公开，但自己不一定想公开。
```

玩家反馈：

```text
希望再加一个：自己想公开，但对方不想公开。
```

判断：反馈成立。当前选项 `E` 表达的是：

```text
希望对方公开，但自己不一定想公开
```

它覆盖的是“要求对方承担公开成本，但自己保留低调”的方向。

但真实关系中还存在另一种不对称：

```text
自己愿意公开 / 希望公开
但对方不愿意公开 / 对方要求低调
```

这类情况对关系体验影响不同，通常更容易触发：

```text
被隐藏感
关系不被承认感
安全感下降
对对方诚意的怀疑
公开程度冲突
```

---

## 2. 建议调整

在 Q007 中新增一个选项：

```text
F 我希望公开或至少被重要圈子知道，但对方更想低调或不公开。
```

或者更短：

```text
F 我想公开，但对方不太想公开。
```

建议优先使用完整表达，避免误解为“当前事实”而不是“倾向/担忧”。

---

## 3. 计分建议

新增选项不应简单等同于“自己爱公开”。它重点表达的是公开意愿不对称和被隐藏风险。

建议影响维度：

```text
public_status_need +
relationship_recognition_need +
attachment_closeness_need +
trust_suspicion_sensitivity +
boundary_double_standard 可视情况轻微调整，但不应直接判定双标
```

如果其中部分维度不在正式 128 维表中，必须参考：

```text
docs/design/16_questionnaire_dimension_table.md
docs/design/39_questionnaire_dimension_alias_mapping.md
```

不要直接写未注册候选别名。

---

## 4. 报告建议

如果玩家选择该项，报告可提示：

```text
你可能更在意关系是否被承认。若对方长期要求低调，需要区分“现实阶段暂时不公开”和“关系被隐藏”。
```

不要写成：

```text
对方一定不认真
你一定没有安全感
```

---

## 5. 建议后续版本

建议作为小修任务：

```text
v0.1.57 问卷公开程度选项补充
```

如果 `current_task_ledger.md` 已有新的版本号安排，以账本为准。

---

## 6. Codex 任务提示词草案

```text
当前仓库：D:\youxi\IF

任务：补充问卷 Q007 公开程度选项。

开始前：
1. git status --short
2. git pull --ff-only origin main
3. 读取 docs/context/current_task_ledger.md
4. 读取 docs/context/2026-06-07_questionnaire_public_status_option_backlog.md

禁止：
- 禁止 force push
- 禁止 reset --hard
- 禁止接 AI API
- 禁止做 UI
- 禁止扩展大型问卷题库
- 禁止重写问卷系统

目标：
1. 在 Q007 中新增选项：自己想公开，但对方不想公开。
2. 更新 questionnaire_mvp.json 中 Q007 的选项、维度影响和必要计分。
3. 保持现有 Q007 选项含义不被破坏。
4. 更新 loader/scoring/reporting/runner 相关测试。
5. 报告中如涉及该项，应表达“关系公开程度不对称 / 被承认需求”，不要诊断化。

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
追加简短说明：Q007 新增“自己想公开但对方不想公开”的公开程度不对称选项。

current_task_ledger.md：
记录该小修已完成、测试结果和下一步建议。

提交：
git add README.md docs/context/current_task_ledger.md docs/context/2026-06-07_questionnaire_public_status_option_backlog.md if_game/data/questionnaire_mvp.json if_game/questionnaire/scoring.py if_game/questionnaire/reporting.py tests/questionnaire_loader_test.py tests/questionnaire_scoring_test.py tests/questionnaire_reporting_test.py tests/questionnaire_runner_test.py
实际修改文件按 git status --short 调整。
git commit -m "fix: 补充问卷公开程度不对称选项"
git push origin main
```

---

## 7. 当前结论

Q007 当前缺少“自己想公开，但对方不想公开”的不对称公开场景。该场景与现有 `E 希望对方公开，但自己不一定想公开` 含义不同，应单独作为选项保留，并在计分与报告中体现“公开程度冲突 / 被承认需求 / 被隐藏感风险”。

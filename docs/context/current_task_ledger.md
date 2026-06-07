# Current Task Ledger

## 1. 当前任务版本号

- 当前账本任务：v0.1.49-v0.1.51 连续任务防丢协议已初始化。
- 仓库当前 HEAD：`c0e3afd docs: 增加当前任务防丢账本`。
- 重要版本号修正：README 已存在 `v0.1.48 关系系统代码落地复盘`，因此后续三个代码阶段统一顺延：
  - v0.1.49：aggregator 接入 14 天主流程。
  - v0.1.50：问卷结果转初始关系/人格修正。
  - v0.1.51：长期 RelationshipMemory 系统。

## 2. 当前阶段

- 阶段：账本初始化已提交，等待进入 v0.1.49。
- 尚未进入阶段 A、阶段 B 或阶段 C 的代码实现。
- 下一步代码阶段：v0.1.49 aggregator 接入 14 天主流程。
- 任意后续任务开始前，必须先读取 `docs/context/current_task_ledger.md`，再继续判断当前阶段和下一步动作。
- 因当前对话已有上下文压缩摘要，已执行恢复流程中的必要读取动作：
  - 已读取 README.md。
  - 已读取 docs/context/codex_task_prompts.md。
  - 已执行 `git status --short`。
  - 已执行 `git log --oneline --decorate -8`。
  - `docs/context/current_task_ledger.md` 原先不存在，本次创建。

## 3. 已完成事项

- 读取 `C:/Users/xu/Downloads/if_codex_v0_1_48_to_v0_1_50_tasks.md`。
- 确认下载任务表包含三个后续阶段：
  - 阶段 A / v0.1.49：aggregator 接入 14 天主流程。
  - 阶段 B / v0.1.50：问卷结果转初始关系/人格修正。
  - 阶段 C / v0.1.51：长期 RelationshipMemory 系统。
- 已提交并推送账本初始化：
  - `c0e3afdf829b808bea10c84c93ecb84434e0d592 docs: 增加当前任务防丢账本`
- 确认工作区在创建本文件前是干净的。
- 确认最近提交：
  - `c0e3afd docs: 增加当前任务防丢账本`
  - `7195783 docs: 增加关系系统代码落地复盘`
  - `f9b6d01 feat: 补充沟通表露问卷题`
  - `41f9347 feat: 轻量接入社会交换与公平聚合规则`
  - `5b7c440 feat: 增加冲突沟通事件聚合样例`
  - `04df9da feat: 接入关系解释与状态聚合器`
  - `31eb16a test: 补充关系状态聚合器裁决用例`
  - `cfc6929 docs: 更新README v0.1.42 聚合器原型说明`
  - `6c241ed docs: 记录README v0.1.42待补说明`

## 4. 未完成事项

- 尚未执行下载任务表要求的 `git pull --ff-only origin main`。
- 尚未阅读阶段 A/B/C 所需全部设计文档和代码文件。
- 尚未实现阶段 A / v0.1.49：aggregator 接入 14 天主流程。
- 尚未实现阶段 B / v0.1.50：问卷结果转初始关系/人格修正。
- 尚未实现阶段 C / v0.1.51：长期 RelationshipMemory 系统。
- 尚未为阶段 A/B/C 新增或更新测试。
- 尚未更新 README 的阶段 A/B/C 版本说明。
- 尚未提交任何 v0.1.49-v0.1.51 代码阶段实现。

## 5. 禁止事项

- 禁止不读本账本就继续长任务。
- 禁止上下文压缩后凭记忆继续。
- 禁止多个大阶段混成一个 commit。
- 禁止没跑对应测试就提交实现代码。
- 禁止为了通过测试删除旧断言。
- 禁止 `reset --hard`。
- 禁止 force push。
- 禁止删除已有文档和测试。
- 禁止接 AI API。
- 禁止做 UI。
- 禁止大规模重构。
- 禁止破坏当前 14 天控制台原型。
- 禁止一次性重写所有事件系统。
- 禁止把问卷 JSON 扩成大题库。

## 6. 上下文压缩后恢复步骤

如果看到“上下文已自动压缩”，必须停止继续写代码，先执行恢复流程：

1. 读取 `docs/context/current_task_ledger.md`。
2. 读取 `README.md`。
3. 读取 `docs/context/codex_task_prompts.md`。
4. 执行 `git status --short`。
5. 执行 `git log --oneline --decorate -8`。
6. 对照任务表确认当前阶段。
7. 如果不能确认下一步，停止并汇报，不要猜。

恢复流程禁止：

- 禁止不读 `current_task_ledger.md` 就继续。
- 禁止压缩后凭记忆继续。
- 禁止在阶段不明确时写代码、改测试或提交。

## 7. 必须运行的测试

### 阶段 A / v0.1.49：aggregator 接入 14 天主流程

```powershell
python tests/relationship_state_aggregator_test.py
python tests/relationship_interpretation_test.py
python tests/smoke_test.py
python tests/scenario_test.py
python tests/reporting_test.py
git diff --check
```

### 阶段 B / v0.1.50：问卷结果转初始关系/人格修正

```powershell
python scripts/check_questionnaire_dimension_ids.py
python tests/questionnaire_loader_test.py
python tests/questionnaire_scoring_test.py
python tests/questionnaire_reporting_test.py
python tests/questionnaire_runner_test.py
python tests/questionnaire_initial_modifiers_test.py
python tests/smoke_test.py
git diff --check
```

### 阶段 C / v0.1.51：长期 RelationshipMemory 系统

```powershell
python tests/relationship_memory_test.py
python tests/relationship_state_aggregator_test.py
python tests/relationship_interpretation_test.py
python tests/smoke_test.py
git diff --check
```

### 三阶段全部完成后的最终验证

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
git status --short
```

## 8. 已运行测试结果

- 当前账本初始化阶段尚未运行业务测试。
- 已运行提交前检查：
  - `git diff --check`：通过，无输出。
- 已运行只读检查：
  - `git status --short`：创建账本前无输出，工作区干净。
  - `git log --oneline --decorate -8`：账本初始化提交后，HEAD 位于 `c0e3afd`。
- 已知账本初始化提交后，`git status --short` 为干净状态。
- 本次状态修正文档需要重新运行 `git diff --check`；最终结果以完成汇报为准。

## 9. 已提交 commit

- 本账本创建前的最新已提交 commit：
  - `71957834e4da508d2cd5610255169dce1dfda6c9 docs: 增加关系系统代码落地复盘`
- 本账本初始化已提交：
  - `c0e3afdf829b808bea10c84c93ecb84434e0d592 docs: 增加当前任务防丢账本`
- 阶段 A/B/C 尚无新提交。

## 10. 下一步动作

1. 开始 v0.1.49 前先执行 `git status --short`。
2. 执行 `git pull --ff-only origin main`。
3. 再读取 `docs/context/current_task_ledger.md`。
4. 然后进入 v0.1.49 aggregator 接入 14 天主流程。
5. 进入 v0.1.49 前必须确认：
   - `git status --short`
   - `git pull --ff-only origin main`
   - `git status -sb`
6. 若工作区不干净，停止并汇报，不要覆盖、不要 reset、不要 stash。
7. 进入 v0.1.49 前再次阅读任务表列出的阶段 A 必读设计文档、主流程代码和相关测试。

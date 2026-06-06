# IF 项目对话交接摘要 2026-06-07

本文档用于给新的 ChatGPT 对话、Codex 或其他开发助手快速读取当前 IF 项目进度，避免上下文丢失。

本文件是交接摘要，不是正式规则母版。正式设计仍以 `README.md`、`docs/design/` 和实际代码为准。

## 1. 项目定位

IF 是一个现实向亲密关系模拟游戏，重点模拟：

- 已经认识；
- 正在聊天；
- 暧昧期；
- 刚恋爱；
- 分手复联；
- 关系中的误会、隐瞒、边界、信任、旧账、修复和现实压力。

当前核心目标不是 UI 或 AI API，而是先把这条链路做扎实：

```text
问卷建档 → 人格/关系倾向 → 事件解释 → 信任变化 → 关系报告
```

## 2. 已完成的重要文档

### 2.1 问卷与维度体系

已完成：

- `docs/design/15_full_questionnaire_upgrade_plan.md`
  - 完整调查问卷升级方案；
  - 四档问卷：快速版、标准版、深度版、超级真实版；
  - 统一口径：128维主表 + 36-72核心启用 + 160扩展预留。

- `docs/design/16_questionnaire_dimension_table.md`
  - 128维主表；
  - 16个大类，每类8个维度；
  - 覆盖基础人格、自我认知、情绪压力、社交、依恋、信任、信息管理、冲突、边界、欲望、责任、价值观、现实稳定性、数字生活、家庭成长、危机模式。

- `docs/design/17_question_type_schema.md`
  - 问卷题型结构；
  - 不把所有题固定成单选；
  - 支持主选项+次选项、多选并标主因、排序、权重分配、滑条、二维坐标、NPC视角题、反向验证题、开放文本题。

### 2.2 超级真实版题库 Q001-Q150

已完成第一版超级真实题库，共 Q001-Q150：

- `docs/design/18_super_realistic_question_bank.md`
  - Q001-Q030；
  - 基础资料、恋爱经历、依恋与亲密。

- `docs/design/18_super_realistic_question_bank_part2.md`
  - Q031-Q070；
  - 信任与怀疑、占有欲与边界、诚实/隐瞒、双标检测、自我美化与反向验证。

- `docs/design/18_super_realistic_question_bank_part3.md`
  - Q071-Q110；
  - 冲突沟通、欲望忠诚、道德责任。

- `docs/design/18_super_realistic_question_bank_part4.md`
  - Q111-Q150；
  - 社交网络、现实压力、数字生活、家庭成长、综合反向验证。

当前结论：Q001-Q150 已足够支撑第一版超级真实问卷，不建议继续盲目加题。

### 2.3 报告、计分、覆盖率与 JSON 设计

已完成：

- `docs/design/19_relationship_report_templates.md`
  - 玩家可读问卷报告模板；
  - 主画像、可信度、关键维度摘要、模块报告、高风险场景、适合/不适合相处模式、游戏内标签。

- `docs/design/22_questionnaire_scoring_rules.md`
  - 0-100维度计分；
  - 初始基准值50；
  - 各题型权重；
  - 维度可信度、证据数量、自我美化、双标、标签生成、游戏行为修正规则。

- `docs/design/23_questionnaire_dimension_coverage.md`
  - Q001-Q150 对128维覆盖率检查；
  - 覆盖强：依恋、信任、信息管理、冲突、边界、欲望、道德、数字生活；
  - 覆盖不足：基础人格、自我认知部分、普通社交、生活自理/一致性、部分危机模式；
  - 明确空缺或接近空缺：`social_energy_level`；
  - 给出 Q151-Q180 定向补题建议，但不是必须立即补。

- `docs/design/24_questionnaire_json_schema.md`
  - 未来问卷 JSON 配置草案；
  - 题目、选项、维度影响、题型、报告标签、反向题、配对题、MVP字段和扩展字段。

### 2.4 归因、记忆、关系信念系统

已完成：

- `docs/design/25_attribution_memory_belief_system.md`
  - 归因理论；
  - 内部/外部归因；
  - 稳定/易变归因；
  - 普遍/特殊归因；
  - 幸福伴侣与痛苦伴侣的不同归因模式；
  - 自利归因；
  - 行动者/观察者效应；
  - 记忆重构；
  - 关系信念；
  - 事件解释、旧账、信任、关系满意度和修复机会。

当前重要待补：该文档还应补充“真实原因层与解释可信度系统”，见第 7 节。

## 3. 已完成的代码链路

当前已经从文档推进到问卷 MVP 可运行链路。

### 3.1 维度 ID 一致性检查

已完成：

- `scripts/check_questionnaire_dimension_ids.py`

作用：

- 从 `docs/design/16_questionnaire_dimension_table.md` 提取 128 个合法维度 ID；
- 扫描题库、计分、覆盖率、JSON schema 文档里的反引号维度引用；
- 检查是否存在未识别维度 ID。

最近一次 Codex 报告结果：

```text
合法维度ID：128
扫描维度引用：655
未识别维度ID：0
```

### 3.2 问卷 MVP JSON 配置

已完成：

- `if_game/data/questionnaire_mvp.json`

当前落地 10 道 MVP 问卷题：

```text
Q001, Q004, Q017, Q018, Q019, Q020, Q021, Q023, Q026, Q030
```

### 3.3 loader / scoring / reporting / runner

已完成：

- `if_game/questionnaire/loader.py`
  - 读取 `questionnaire_mvp.json`；
  - 校验基础字段、题目 ID 唯一、`selection_mode` 合法、`dimensions` 存在、`scoring.dimension_effects` 存在。

- `if_game/questionnaire/scoring.py`
  - 提供 `score_questionnaire(config, answers)`；
  - 支持 MVP 题型：`forced_single`、`primary_with_secondary`、`multi_with_primary`、`slider`、`axis_2d`；
  - 输出：`dimension_scores`、`evidence_count`、`answered_questions`、`total_questions`、`completion_rate`。

- `if_game/questionnaire/reporting.py`
  - 提供 `render_questionnaire_report(config, answers, score_result) -> str`；
  - 输出中文 MVP 问卷报告。

- `if_game/questionnaire/runner.py`
  - 支持命令：

```bash
python -m if_game.questionnaire.runner
```

  - 可以真实填写 10 道 MVP 问卷；
  - 支持单选、主选+次选、多选并标主因、滑条、二维坐标；
  - 错误输入会提示重试；
  - 最后生成中文报告。

### 3.4 当前测试命令

最近一次 Codex 报告中，以下测试均通过：

```bash
python scripts/check_questionnaire_dimension_ids.py
python tests/questionnaire_loader_test.py
python tests/questionnaire_scoring_test.py
python tests/questionnaire_reporting_test.py
python tests/questionnaire_runner_test.py
python tests/smoke_test.py
python tests/scenario_test.py
python tests/reporting_test.py
```

并且做过一次：

```bash
python -m if_game.questionnaire.runner
```

管道输入完整运行通过。

## 4. 重要提交记录

近期关键提交包括：

```text
1b34eb6 docs: 增加问卷JSON配置草案
402cad8 tools: 增加问卷维度ID一致性检查
3b20cb2 feat: 增加问卷MVP配置加载
edb2286 feat: 增加问卷MVP计分引擎
5208135 feat: 增加问卷MVP报告生成器
ac5f741 feat: 增加问卷MVP控制台入口
4f7a3be docs: 增加归因记忆与关系信念系统设计
```

用户反馈这些任务完成后，工作区均为干净状态。

## 5. 当前明确设计原则

### 5.1 问卷原则

- 问卷不是心理诊断；
- 不用单题给严重标签；
- 不把高低值简单等同好坏；
- 自评题权重低于情境题；
- 游戏行为后续可以覆盖问卷自述；
- 反向验证题只提示差异，不道德审判玩家。

### 5.2 关系模拟原则

IF 不应该是：

```text
玩家做了某行为 → NPC 固定扣分
```

而应该是：

```text
玩家做了某行为
→ NPC 根据当前信任、旧记忆、归因风格、关系信念、预期和可见线索解释该行为
→ 解释影响情绪、信任、旧账、冲突和修复机会
```

### 5.3 不要把所有怀疑心理学化洗白

这是本轮对话中非常重要的原则：

```text
解释偏差不等于事实不存在。
怀疑不一定错误，信任也不一定正确。
```

现实中确实存在：

- 对方不是忙，而是不想回；
- 对方心里优先级下降；
- 对方知道你不会离开，所以不急着回；
- 对方在和别人见面；
- 对方在暧昧或出轨；
- 对方在圆谎；
- 对方故意冷处理或操控。

所以 IF 必须同时模拟：

```text
真实原因层 truth layer
解释层 interpretation layer
证据层 evidence layer
```

而不是只模拟“你是不是焦虑”。

## 6. 当前不能忘的现实例子

### 6.1 晚回消息

同样是 5 小时没回，真实原因可能是：

- 真的忙；
- 睡着或手机没电；
- 看到了但觉得不急；
- 心里优先级下降；
- 回避冲突；
- 故意冷处理；
- 在做不想让对方知道的事；
- 和别人见面；
- 暧昧或出轨；
- 故意测试或操控。

### 6.2 社交媒体更新但不回消息

如果对方说“没看手机”，但出现：

- 发朋友圈；
- 点赞；
- 评论；
- 群聊发言；
- 在线状态；
- 已读不回；

那么“完全没看手机”的解释可信度下降。

这不一定直接证明出轨，但至少说明：

```text
对方对别人可用，对你不可用。
```

可以形成：

- `selective_availability`；
- `priority_neglect_signal`；
- `behavior_explanation_gap`。

### 6.3 半夜 3 点异常电话

例如对方说：

```text
半夜 3 点是妈妈打电话。
```

系统不应写死“绝不可能”，因为现实有急事、时差、疾病等例外。

但基础可信度较低，需要上下文支持。

如果无细节、反复出现、解释变动、删记录，则证据链增强。

## 7. 当前最重要的待办：补充真实原因层与解释可信度系统

用户刚刚要求生成了 Codex 指令，但尚未反馈完成。

目标：更新 `docs/design/25_attribution_memory_belief_system.md`，新增或补强：

```text
真实原因层与解释可信度系统
```

核心字段草案：

### truth layer

- `truth_type`
- `truth_reason`
- `truth_intention`
- `truth_harm_level`
- `truth_priority_signal`
- `truth_moral_severity`

### claim / explanation layer

- `explanation_claim`
- `explanation_specificity`
- `explanation_consistency`
- `explanation_plausibility`
- `behavior_explanation_gap`
- `excuse_repetition_count`

### observable traces

- `online_but_no_reply`
- `social_media_updated_but_no_reply`
- `message_seen_but_ignored`
- `selective_availability`
- `late_night_implausible_call`
- `explanation_timing_conflict`
- `deleted_chat_trace`
- `third_party_witness`
- `payment_or_location_trace`

### evidence / calibration

- `evidence_chain_strength`
- `exposure_risk`
- `interpretation_accuracy`
- `trust_calibration`
- `suspicion_accuracy_history`
- `misplaced_trust_history`
- `accurate_alertness_tag`
- `over_suspicion_tag`
- `selective_blindness_tag`

四象限必须保留：

| 判断 | 事实 | 类型 |
| --- | --- | --- |
| 怀疑有问题 | 真的有问题 | 准确警觉 |
| 怀疑有问题 | 实际没问题 | 误会/焦虑 |
| 相信没问题 | 实际没问题 | 稳定信任 |
| 相信没问题 | 真的有问题 | 被欺骗/低估风险 |

这部分做完后，归因系统才不会把真实失信误写成单纯心理偏差。

## 8. 建议下一步路线

### 优先级 1：完成真实原因层文档补充

路径：

```text
docs/design/25_attribution_memory_belief_system.md
```

提交建议：

```text
docs: 补充真实原因与解释可信度系统
```

### 优先级 2：扩展问卷 MVP 到快速版 25 题

当前 runner 只有 10 题，适合技术验证，不适合真实玩家体验。

下一步可扩展：

```text
if_game/data/questionnaire_mvp.json
```

从 Q001-Q030 中扩到 25 题快速版，重点覆盖：

- 基础关系入口；
- 联系频率；
- 现实距离；
- 依恋；
- 信任；
- 隐瞒；
- 冲突；
- 边界；
- 修复。

### 优先级 3：把问卷入口挂到主菜单

暂时不急。

当前问卷 runner 已可独立运行，不必马上接入 14 天主流程。

### 优先级 4：做 relationship_interpretation 原型

未来可以新增原型：

```text
if_game/relationship_interpretation.py
```

目标：同一行为根据归因、记忆、信任、证据和真实原因产生不同解释。

但这一步应等 `25` 文档补全真实原因层后再做。

## 9. 给新对话的工作建议

如果新的对话继续这个项目，优先说：

```text
请先读取 docs/context/2026-06-07_if_project_handoff.md。
```

然后根据当前目标选择：

1. 继续 Codex 文档补充：真实原因层与解释可信度系统；
2. 扩展问卷 JSON 到 25 题快速版；
3. 把问卷 runner 接入主菜单；
4. 做关系解释原型。

不要再从头讨论 Q001-Q150 题库，除非是为了修复、配置化或补低覆盖维度。

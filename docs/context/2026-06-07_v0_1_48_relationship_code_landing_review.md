# v0.1.48 关系系统代码落地复盘与下一阶段待办

本文档复盘 v0.1.42-v0.1.47 已经落地到代码与测试中的关系系统内容，并明确下一阶段接入主流程前的边界。

## 1. v0.1.42-v0.1.47 已完成内容总览

### v0.1.42 关系状态聚合器原型

- 新增 `if_game/relationship_state_aggregator.py`。
- 新增 `RelationshipStateDelta`，输出信任、满意度、亲密、稳定、修复机会、旧伤记忆、安全感、刺激感、公平感、依赖度等方向性变化。
- 新增 `aggregate_relationship_event(event)`，支持 dict 输入，先把单次事件结算为轻量 delta。
- 第一版已覆盖隐私边界不等于欺骗、高伤害欺骗优先由信任承担、石墙损害修复、高质量修复打开修复窗口、重复事件写入记忆提示等规则。

### v0.1.43 aggregator 关键裁决测试

- 补齐 `tests/relationship_state_aggregator_test.py` 的核心裁决用例。
- 已验证沉默不一定是石墙、石墙是高伤害沟通、吵架但成功修复、准确警觉、误会/焦虑、隐私不等于欺骗、低痛苦不等于高快乐、高快乐不等于安全、公平不是五五分、同一事件不重复扣信任。
- 轻量启用了 `safety_delta`、`excitement_delta`、`fairness_delta` 等预留字段。

### v0.1.44 relationship_interpretation.py 接入 aggregator

- 在 `if_game/relationship_interpretation.py` 中新增 `interpretation_to_aggregator_input()`。
- 解释层仍保留原有 `interpret_relationship_event()` 输出结构，不重写解释模型。
- 新适配器负责把解释结果中的事实伤害、欺骗、证据链、解释准确度、隐私边界等字段转换为 aggregator 可消费的 dict。
- 已覆盖准确警觉、误会/焦虑、真实欺骗三条路径。

### v0.1.45 冲突沟通事件轻量接入 aggregator

- 新增 `if_game/conflict_event_samples.py`。
- 当前样例包括 E-CON-01 迟到抱怨、E-CON-02 有效暂停争吵、E-CON-03 嘲讽脆弱表达。
- aggregator 已能识别 `conflict_response_type`、防卫/反向抱怨、有效暂停、蔑视/嘲讽和修复质量等输入。
- 已验证精确表达与道歉修复、反向抱怨/防卫、有效暂停不是石墙、嘲讽脆弱表达写旧伤、样例事件可直接聚合。

### v0.1.46 社会交换与公平轻量接入 aggregator

- 新增 `if_game/exchange_event_samples.py`。
- 当前样例包括 E-EXC-01 安全但沉闷、E-EQU-01 长期家务/情绪劳动获益不足、E-EQU-02 主动看见并补偿付出。
- aggregator 已轻量支持关系收益/代价、接近奖赏、回避压力、沉闷、公平感、获益不足、被理所当然对待和依赖变化。
- 已验证安全但沉闷、高刺激高风险、长期获益不足、被理所当然对待、公平不是五五分、社会交换字段不重复扣信任。

### v0.1.47 问卷补 4 个沟通表露题

- `if_game/data/questionnaire_mvp.json` 从 25 题扩展为 29 题。
- 新增 Q-COM-01 自我表露意愿、Q-COM-05 回应性需求、Q-COM-06 哪些事情可以保留不说、Q-COM-10 自己表露 vs 希望对方表露。
- 题型只使用现有 runner/scoring 已支持的 `forced_single`、`primary_with_secondary`、`multi_with_primary`、`slider`、`axis_2d` 范围。
- 问卷计分和报告测试已覆盖新维度，报告层新增沟通表露摘要。

## 2. 当前代码模块之间的数据流

当前关系系统代码已经形成几个独立、可测试的数据流，但还没有接入主游戏闭环。

### 解释层到聚合器

1. 事件 dict 进入 `interpret_relationship_event()`。
2. `relationship_interpretation.py` 输出解释结果，包含事实层、解释层、可见线索、证据链强度、四象限解释准确度、关系影响和报告标签。
3. `interpretation_to_aggregator_input(result, source_id, target_id)` 把 0-100 解释层字段缩放并映射为 aggregator 支持的 0-10 输入字段。
4. `aggregate_relationship_event()` 结算为 `RelationshipStateDelta`。

### 冲突与交换样例到聚合器

1. `conflict_event_samples.py` 的 E-CON 样例直接返回 aggregator 可识别的事件 dict。
2. `exchange_event_samples.py` 的 E-EXC/E-EQU 样例直接返回 aggregator 可识别的事件 dict。
3. 测试把这些样例传入 `aggregate_relationship_event()`，验证 delta 方向和标签。

### 问卷系统当前数据流

1. `if_game/data/questionnaire_mvp.json` 提供 29 题 MVP 配置。
2. `if_game/questionnaire/loader.py` 加载配置。
3. `if_game/questionnaire/scoring.py` 根据 answer record 计算维度分数。
4. `if_game/questionnaire/reporting.py` 渲染玩家可读问卷报告。
5. `if_game/questionnaire/runner.py` 提供独立控制台问卷入口。

问卷结果目前不进入 aggregator，也不改变 14 天控制台原型的初始关系状态。

## 3. 当前还没有接入的地方

- `main.py` 主流程：主菜单和 14 天原型入口尚未把 seed event、解释结果或问卷结果传给 aggregator。
- 14 天事件流程：现有 14 天事件仍沿用原来的事件/选择/结算路径，没有逐事件生成 `RelationshipStateDelta`。
- 试玩报告：当前玩家可读关系复盘报告尚未消费 `report_tags`、`memory_notes` 或 aggregator delta。
- 长期记忆系统：`memory_notes` 仍是字符串提示，没有落到结构化 `RelationshipMemory`、衰减规则、重复模式阈值或存档。
- 问卷结果对游戏初始状态的影响：29 题问卷能生成维度分数和报告，但还没有把依恋、信任、沟通表露、隐私边界等维度转成角色初始倾向或关系初始参数。

## 4. 当前测试覆盖了什么

- `tests/relationship_state_aggregator_test.py` 覆盖 aggregator 输出结构、字段边界、关键裁决规则、重复事件、冲突样例、交换/公平样例和依赖度不等于亲密。
- `tests/relationship_interpretation_test.py` 覆盖解释层四象限、证据链、解释可信度、关系影响、解释结果到 aggregator 输入的转换，以及转换后 delta 的主要方向。
- `tests/questionnaire_loader_test.py` 覆盖 29 题数量、题目 ID 唯一、新增 Q-COM 题存在、基础字段完整。
- `tests/questionnaire_scoring_test.py` 覆盖 29 题 answer record、核心维度计分、新增沟通表露维度计分和不同答案路径分数差异。
- `tests/questionnaire_reporting_test.py` 覆盖问卷报告生成、沟通表露摘要、关键文字出现和非诊断式表达边界。
- `tests/questionnaire_runner_test.py` 覆盖控制台 runner 的输入解析、错误输入拒绝、29 题完整运行、计分和报告生成。

## 5. 当前测试还没覆盖什么

- 主流程从 `main.py` 进入 14 天原型后，是否能调用 aggregator。
- 单个 14 天 seed event 如何映射为 aggregator 输入。
- 多天、多事件累计后的关系状态快照。
- `RelationshipStateDelta` 如何应用到现有角色/关系状态对象。
- `report_tags` 如何转换为玩家试玩报告中的中文段落。
- `memory_notes` 如何升级为结构化长期记忆、旧伤衰减、重复模式和修复记忆。
- 问卷维度分数如何影响游戏初始状态、NPC反应阈值或玩家可见报告。
- 保存/读取、跨会话延续和长期模拟。
- 极端输入、缺字段输入和不同模块同时给出冲突字段时的完整兼容性。

## 6. 下一阶段推荐任务顺序

1. 先定义一个很薄的关系状态快照或应用函数，用于把 `RelationshipStateDelta` 应用到临时状态对象，不改主流程。
2. 给现有 14 天 seed event 增加 1-2 个测试专用映射函数，把老事件结果转换为 aggregator 输入。
3. 在测试中跑“事件 dict -> aggregator -> 状态快照”的小闭环，确认不会破坏当前 14 天控制台原型。
4. 挑选一条 14 天流程里的低风险事件接入 aggregator，只做旁路计算和日志，不改变玩家结局。
5. 再把 `report_tags` 和 `memory_notes` 映射到试玩报告的补充段落。
6. 在报告稳定后，再设计结构化 `RelationshipMemory` 和衰减/重复阈值。
7. 最后把问卷结果转成游戏初始状态修正，例如信任基线、修复接受度、隐私边界敏感度、沟通直接度等。

## 7. 不建议马上做什么

- 不建议立即重写 `main.py`、14 天事件引擎或现有结局判定。
- 不建议把 aggregator 一次性接入所有事件，否则很难定位规则冲突。
- 不建议马上做完整 CL/CLalt、长期经济模型或复杂权力系统。
- 不建议立即扩展到 40-60 题问卷，当前更需要先验证 29 题结果如何影响游戏。
- 不建议接 AI API、做 UI 或复杂剧情树。
- 不建议把 `memory_notes` 直接当作最终长期记忆系统，下一步应先定义结构化记忆字段。
- 不建议让单次普通事件直接摧毁关系，仍应保持 aggregator 的方向性和有界变化原则。

# IF

IF 是一个现实向亲密关系模拟游戏，重点模拟已经认识、正在聊天、暧昧、刚恋爱或分手复联后的关系变化。

当前阶段是规则母版、纸面原型和最小控制台测试原型阶段。当前只实现 14 天闭环验证用的 Python 控制台原型，不做 UI、不接入 AI API。

## 文档阅读顺序

1. `docs/canon/00_if_core_rulebook.md`
2. `docs/design/01_character_fields.md`
3. `docs/design/02_personality_questionnaire.md`
4. `docs/design/03_relationship_values.md`
5. `docs/design/04_event_card_template.md`
6. `docs/design/05_seed_events.md`
7. `docs/design/06_relationship_engine_rules.md`
8. `docs/design/07_v0_1_14_day_flow.md`
9. `docs/design/08_seed_event_branch_tables.md`
10. `docs/design/09_data_schema_blueprint.md`
11. `docs/design/10_sample_character_profiles.md`
12. `docs/design/11_playtest_case_matrix.md`
13. `docs/design/12_v0_1_mvp_implementation_plan.md`
14. `docs/design/13_psychology_framework_mapping.md`
15. `docs/design/14_playtest_report_design.md`
16. `docs/design/15_full_questionnaire_upgrade_plan.md`
17. `docs/design/16_questionnaire_dimension_table.md`
18. `docs/design/17_question_type_schema.md`
19. `docs/design/18_super_realistic_question_bank.md`
20. `docs/design/18_super_realistic_question_bank_part2.md`
21. `docs/design/18_super_realistic_question_bank_part3.md`
22. `docs/design/18_super_realistic_question_bank_part4.md`
23. `docs/design/19_relationship_report_templates.md`
24. `docs/design/22_questionnaire_scoring_rules.md`
25. `docs/design/23_questionnaire_dimension_coverage.md`
26. `docs/design/24_questionnaire_json_schema.md`
27. `docs/design/25_attribution_memory_belief_system.md`
28. `docs/design/26_partner_perception_and_impression_system.md`
29. `docs/design/27_communication_self_disclosure_system.md`
30. `docs/design/28_questionnaire_communication_disclosure_module.md`
31. `docs/design/29_conflict_communication_repair_system.md`
32. `docs/design/30_social_exchange_dependency_system.md`
33. `docs/design/31_system_integration_consistency_rules.md`
34. `docs/design/32_approach_avoidance_turbulence_system.md`
35. `docs/design/33_communal_exchange_equity_system.md`
36. `docs/design/34_relationship_state_aggregator_implementation_plan.md`
37. `docs/design/35_relationship_event_template_library.md`
38. `docs/design/36_questionnaire_expansion_candidate_pool.md`
39. `docs/design/37_relationship_report_tag_dictionary.md`
40. `docs/design/38_relationship_system_logic_audit_and_optimization_notes.md`
41. `docs/design/39_questionnaire_dimension_alias_mapping.md`
42. `docs/design/40_relationship_enum_and_field_registry.md`
43. `docs/design/41_relationship_memory_decay_and_pattern_rules.md`
44. `docs/context/2026-06-07_after_relationship_docs_backlog.md`
45. `docs/context/codex_task_prompts.md`

## v0.1 目标

建立一个 14 天暧昧/刚恋爱高密度测试版的规则基础，用少量种子事件验证真实值与感知值偏差、撒谎与破绽、压力叠加、未解决冲突和动态关系阶段。

## v0.1.1 目标

把核心规则推进为可计算、可测试的纸面原型；仍不写代码。

## v0.1.2 目标

把规则和分支表整理成可编码的数据结构、样例角色和纸面测试用例；仍不写代码。

## v0.1.3 目标

把依恋理论、大五人格、爱的五种语言、非暴力沟通、戈特曼冲突理论、爱情三角理论和需求层次正式映射到 IF 的角色、问卷、关系值、行为标签和事件设计中；仍不写代码。

## v0.1.4 控制台原型

当前已经有最小控制台原型，用于验证 14 天流程、3 个种子事件、模糊感知反馈、记忆账本和第 14 天阶段结算。

运行方式：

```bash
python -m if_game.main
```

测试方式：

```bash
python tests/smoke_test.py
```

当前原型只用于验证 14 天闭环，不是完整游戏。当前不做 UI、存档、AI、完整经济系统、完整亲密系统、完整一年模拟。

## v0.1.5 多场景测试

v0.1.5 增加了 `if_game/data/playtest_scenarios.json`，用于用同一套 14 天流程跑多条脚本路径，验证不同角色组合、事件分支和玩家选择能导向不同结局倾向。

运行多场景测试：

```bash
python tests/scenario_test.py
```

控制台入口也可以查看内置场景摘要：

```bash
python -m if_game.main
```

当前支持的脚本路径：

- 修复路径；
- 冷淡路径；
- 谎言危机路径；
- 边界协商路径；
- 分分合合路径。

v0.1.5 仍然不做 UI、AI、数据库、存档、完整一年、完整经济系统或完整亲密系统。

## v0.1.6 试玩记录与导出

v0.1.6 增加了命令行试玩辅助和 UTF-8 文本报告导出，方便真实试玩后复盘 14 天 transcript、最终阶段、反馈等级、记忆摘要和触发事件。

命令行运行：

```bash
python -m if_game.main --list-scenarios
python -m if_game.main --scenario scenario_repair
python -m if_game.main --scenario scenario_crisis_lie --export playtest_logs/crisis.txt
python -m if_game.main --run-all-scenarios
python -m if_game.main --run-all-scenarios --export playtest_logs/all_scenarios.txt
```

Windows 控制台中文乱码处理方式见：

```text
docs/troubleshooting_windows_encoding.md
```

也可以使用辅助脚本：

```bat
scripts\run_if_utf8.bat
```

测试方式：

```bash
python tests/smoke_test.py
python tests/scenario_test.py
python tests/reporting_test.py
python tests/questionnaire_loader_test.py
python tests/questionnaire_scoring_test.py
python tests/questionnaire_reporting_test.py
python tests/questionnaire_runner_test.py
python tests/relationship_interpretation_test.py
```

## 问卷 MVP JSON 配置

当前已新增最小可读取问卷配置：

```text
if_game/data/questionnaire_mvp.json
```

配置先覆盖 Q001-Q030 中的 25 道快速版题，用于验证真实 JSON 配置、基础字段校验和后续计分落地路径。当前只做配置加载，不做 UI，不接 AI API，也不接入 14 天控制台原型主流程。

加载测试：

```bash
python tests/questionnaire_loader_test.py
```

## 问卷 MVP 计分引擎

当前已新增最小问卷计分模块：

```text
if_game/questionnaire/scoring.py
```

计分引擎基于 `if_game/data/questionnaire_mvp.json` 和标准 answer record 计算核心维度分数。当前支持 MVP 配置中已经出现的 `forced_single`、`primary_with_secondary`、`multi_with_primary`、`slider` 和 `axis_2d`，输出 `dimension_scores`、`evidence_count`、`answered_questions` 和 `completion_rate`。

计分测试：

```bash
python tests/questionnaire_scoring_test.py
```

## 问卷 MVP 报告生成器

当前已新增最小问卷报告生成模块：

```text
if_game/questionnaire/reporting.py
```

报告生成器把 `score_questionnaire()` 的结果转换成玩家可读中文摘要。当前输出包含标题、完成度、已回答题数 / 总题数、关键维度摘要、亲密依恋摘要、风险提示和后续游戏行为修正提示。报告使用“很低 / 较低 / 中等 / 较高 / 很高”描述分数，不输出诊断式结论。

报告测试：

```bash
python tests/questionnaire_reporting_test.py
```

## 问卷 MVP 控制台 runner

当前已新增独立问卷控制台入口：

```bash
python -m if_game.questionnaire.runner
```

该入口会读取 `if_game/data/questionnaire_mvp.json` 中的 25 道快速版题，按顺序展示题号、标题、题干、选项或滑条/二维坐标提示，收集答案后调用 loader、scoring 和 reporting 生成中文问卷报告。当前只作为问卷 MVP 独立验证入口，不接 UI、不接 AI API，也不接入 14 天主流程。

也可以从主控制台菜单进入：

```bash
python -m if_game.main
```

runner 测试：

```bash
python tests/questionnaire_runner_test.py
```

## 问卷文档一致性检查

检查题库、计分规则、覆盖率和 JSON 配置草案中反引号包裹的维度ID是否存在于 128维主表：

```bash
python scripts/check_questionnaire_dimension_ids.py
```

该脚本会输出合法维度ID总数、扫描到的维度引用总数、未识别维度ID列表，以及未识别维度ID所在文件和行号。

导出的 `playtest_logs/` 只用于本地试玩记录，不进入版本库。

## v0.1.7 关系复盘报告

v0.1.7 把试玩报告从开发字段日志改成玩家可读的关系复盘。导出的报告现在包含：

- 主结局；
- 副标签；
- 关系概述；
- 关键转折点；
- 主要原因；
- 后续隐患；
- 修复机会。

`active_hooks`、`feedback_level`、`scenario_id` 等开发字段不再直接展示在玩家报告中，触发事件会被转换成“消息延迟”“异性饭局/神秘电话”“冲突处理”等中文说明。

本版本也调整了结局解释：重大谎言、前任隐瞒或情绪性拉黑进入危机线时，主结局优先显示“分手危机”；“分分合合倾向”更多作为副标签展示。解释敷衍、边界未清和冷战叠加但没有原则性危机时，暧昧开局可以结算为“暧昧降温”。

## v0.1.8 完整调查问卷升级方案

新增 `docs/design/15_full_questionnaire_upgrade_plan.md`，用于沉淀下一阶段问卷升级方向。该文档记录：

- 快速版、标准版、深度版、超级真实版四档问卷；
- 100-180题完整题库方向；
- 弹性题型设计；
- 主选项、次选项、原因标签和确信度；
- 128维主表方向，允许第一版只启用36-72个核心维度，并预留160维扩展；
- 自述人格与行为人格分离；
- NPC四层档案；
- 谎言证据链；
- 多层信任；
- 长期记忆、情绪分层、社交网络和现实压力。

本次仍是文档设计，不修改控制台原型运行逻辑。

## v0.1.9 128维问卷维度表

新增 `docs/design/16_questionnaire_dimension_table.md`，将完整问卷底层维度扩展为 128 维：

- 16个大类；
- 每类8个维度；
- 覆盖基础人格、自我认知、情绪压力、社交、依恋、信任、信息管理、冲突、边界、欲望、责任、价值观、现实稳定性、数字生活、家庭成长和危机模式；
- 每个维度包含ID、中文名、核心定义、高值表现、低值表现和主要用途；
- 补充与现有 `PersonalityModel` 字段的映射；
- 补充题库覆盖要求、评分报告原则和160维扩展预留。

本次仍是文档设计，不修改控制台原型运行逻辑。

## v0.1.10 问卷题型数据结构

新增 `docs/design/17_question_type_schema.md`，用于定义完整调查问卷的题型与答案结构。该文档记录：

- 不把题目简单固定为单选或多选；
- 行为题必须保留主行为；
- 心理动机、原因、担忧和底线可以多选；
- 支持主选项 + 次选项；
- 支持多选并标主因；
- 支持排序、权重分配、滑条、二维点击、NPC视角题、反向验证题和开放文本题；
- 定义 `selection_mode`、答案记录结构、原因标签、计分权重、双标检测和自我美化检测规则。

本次仍是文档设计，不修改控制台原型运行逻辑。

## v0.1.11 超级真实版题库第一批

新增 `docs/design/18_super_realistic_question_bank.md`，开始整理超级真实版题库。当前完成第一批约30题，覆盖：

- 基础资料；
- 恋爱经历；
- 依恋与亲密；
- 关系入口、认识方式、联系频率、现实距离、当前关系目标；
- 过去关系脚本、前任联系、复合态度；
- 被弃焦虑、回避亲密、亲密需求、独立需求、暴露脆弱、承诺节奏和修复接受度。

后续继续补充信任怀疑、边界占有、诚实隐瞒、冲突沟通、欲望忠诚、道德责任、社交网络、现实压力、数字生活、双标检测题和反向验证题。

本次仍是文档设计，不修改控制台原型运行逻辑。

## v0.1.12 超级真实版题库第二批

新增 `docs/design/18_super_realistic_question_bank_part2.md`，继续整理超级真实版题库第二批。当前新增约40题，覆盖：

- 信任与怀疑；
- 占有欲与边界；
- 诚实、隐瞒与信息管理；
- 双标检测配对题；
- 自我美化与反向验证题；
- 对方解释不完整、神秘电话、手机遮屏、前任联系、异性饭局、报备、手机隐私、定位共享、半真半假、删除聊天、小号、被揭穿反应、数字证据意识等场景。

后续继续补充冲突沟通、欲望忠诚、道德责任、社交网络、现实压力和数字生活剩余题。

本次仍是文档设计，不修改控制台原型运行逻辑。

## v0.1.13 超级真实版题库第三批

新增 `docs/design/18_super_realistic_question_bank_part3.md`，继续整理超级真实版题库第三批。当前新增约40题，覆盖：

- 冲突与沟通；
- 欲望、新鲜感与忠诚；
- 道德、责任与后果意识；
- 吵架当下表达、被指出问题时的反应、冷处理、拉黑/删除冲动、公共场合冲突、说重话、道歉能力、修复主动性、关系复盘、倾听能力、情绪恢复；
- 新鲜感需求、稳定偏好、诱惑抵抗、精神暧昧边界、情绪价值缺口、替代倾向、忠诚自我认同、暧昧边界；
- 责任承担、底线清晰度、后果预判、道德弹性、承诺可信度、补偿意愿、暴露后负责度、伤害觉察、自我合理化、破罐破摔和报复冲动。

后续继续补充社交网络、现实压力、数字生活剩余题和综合反向验证。

本次仍是文档设计，不修改控制台原型运行逻辑。

## v0.1.14 超级真实版题库第四批

新增 `docs/design/18_super_realistic_question_bank_part4.md`，完成超级真实版题库第四批。当前新增约40题，覆盖：

- 社交网络；
- 现实压力；
- 数字生活剩余题；
- 家庭、成长与关系脚本补充；
- 综合反向验证；
- 超级真实版最终总结题；
- 朋友意见、共同圈子、流言传播、朋友与恋人冲突、社交场合被忽略、朋友圈展示比较；
- 时间投入、时间管理、金钱压力、作息不一致、家庭压力、家庭边界、工作/学业高压、现实条件不匹配；
- 在线可得压力、点赞评论边界、朋友圈可见性、两个账号/两部手机、聊天记录透明度、数字生活自评；
- 原生冲突模板、成长安全感、默认恋爱剧本、模式重复觉察、自述人格一致性、自我美化风险和压力下真实反应。

至此，超级真实版题库已经形成 Q001-Q150 的完整第一版结构。后续建议先做问卷报告模板、计分规则和128维覆盖率检查，不建议继续盲目加题。

本次仍是文档设计，不修改控制台原型运行逻辑。

## v0.1.15 问卷报告模板

新增 `docs/design/19_relationship_report_templates.md`，用于定义超级真实版问卷的玩家可读报告模板。该文档记录：

- 报告总结构；
- 问卷完整度与可信度模板；
- 主画像模板；
- 关键维度摘要；
- 亲密依恋、信任边界、诚实信息、冲突修复、欲望忠诚、现实压力和数字生活模块报告；
- 高风险关系场景模板；
- 适合/不适合的相处模式；
- 游戏内初始标签；
- 自述人格 vs 行为人格差异；
- 完整报告样例和简短报告样例。

本次仍是文档设计，不修改控制台原型运行逻辑。

## v0.1.16 问卷计分与可信度规则

新增 `docs/design/22_questionnaire_scoring_rules.md`，用于定义超级真实版问卷的计分、可信度和标签生成规则。该文档记录：

- 0-100 维度分数范围；
- 初始基准值；
- 不同题型的基础权重；
- 主选择、次选择、原因标签的计分规则；
- 滑条、二维坐标、排序、多选、权重分配题的处理方式；
- 确信度、完整度、维度可信度和证据数量规则；
- 自我美化风险、双标风险和反向验证规则；
- 可见标签、隐藏标签、风险标签、优势标签和差异标签生成规则；
- 模块分数、报告输出规则和游戏内行为修正规则；
- `questionnaire_result` 输出结构草案和题库 JSON 化时的选项计分配置示例。

本次仍是文档设计，不修改控制台原型运行逻辑。

## v0.1.17 问卷维度覆盖率检查

新增 `docs/design/23_questionnaire_dimension_coverage.md`，用于检查 Q001-Q150 对 128维主表的覆盖情况。该文档记录：

- 覆盖等级定义：高、中、低、空缺；
- 128维逐项覆盖检查；
- 当前覆盖充足的大类和覆盖不足的大类；
- 空缺或接近空缺维度；
- 低覆盖优先补强维度；
- Q151-Q180 定向补题建议；
- 是否必须补题的判断；
- 下一步路线：先做 JSON schema，或先补 Q151-Q180。

本次仍是文档设计，不修改控制台原型运行逻辑。

## v0.1.18 问卷 JSON 配置草案

新增 `docs/design/24_questionnaire_json_schema.md`，用于设计未来题库 JSON 配置结构。该文档记录：

- 顶层 `questionnaire_meta`、`modules`、`questions` 和全局 `scoring` 结构；
- 题目字段、选项字段、`selection_mode`、`dimensions`、`dimension_effects`、`reason_tags`、`reverse_pair_id`、`perspective_pair_id`、`confidence` 和 `report_tags`；
- Q001、Q017、Q051、Q069、Q090、Q150 的 JSON 示例；
- 如何从 JSON 生成 `self_report_profile`、`dimension_scores`、`confidence_scores`、`visible_tags`、`hidden_tags` 和 `report_sections`；
- MVP 必须字段、建议支持字段和后续扩展字段边界。

本次仍是纯文档设计，不修改 Python 代码，不修改现有题库内容，也不新增真实 JSON 配置文件。

## v0.1.19 问卷 MVP 配置加载

新增 `if_game/data/questionnaire_mvp.json`，从 Q001-Q030 中抽取 25 道题作为快速版真实 JSON 配置，覆盖关系入口、认识背景、联系频率、现实距离、依恋、信任、隐瞒、冲突、边界、修复和依恋自评。

新增 `if_game/questionnaire/loader.py` 和 `tests/questionnaire_loader_test.py`，用于读取 MVP 配置并校验基本字段、题目 ID 唯一、`selection_mode` 合法、`dimensions` 存在以及每题具备 `scoring.dimension_effects`。

本次不做 UI，不接 AI API，不实现完整 Q001-Q150，也不接入或破坏现有 14 天控制台原型。

## v0.1.20 问卷 MVP 计分引擎

新增 `if_game/questionnaire/scoring.py` 和 `tests/questionnaire_scoring_test.py`，用于基于 MVP JSON 配置和模拟 answer record 计算核心维度分数。当前支持强制单选、主选项+次选项、多选并标主因、滑条和二维坐标题。

输出包含 `dimension_scores`、`evidence_count`、`answered_questions`、`total_questions` 和 `completion_rate`。所有维度从 50 起步，最终分数限制在 0-100。

本次不做 UI，不接 AI API，不实现完整 Q001-Q150，不修改题库设计文档，也不接入或破坏现有 14 天控制台原型。

## v0.1.21 问卷 MVP 报告生成器

新增 `if_game/questionnaire/reporting.py` 和 `tests/questionnaire_reporting_test.py`，用于把 MVP 计分结果转换为玩家可读中文问卷摘要。报告包含完成度、关键维度摘要、亲密依恋摘要、风险提示和后续游戏行为修正提示。

报告只使用关系行为表达，不做心理诊断，不输出“你一定会怎样”或“你就是某种人格”这类结论。当前仍不做 UI、不接 AI API、不实现完整 Q001-Q150，也不接入现有 14 天主流程。

## v0.1.22 问卷 MVP 控制台入口

新增 `if_game/questionnaire/runner.py` 和 `tests/questionnaire_runner_test.py`，用于独立运行问卷 MVP。控制台入口支持 `forced_single`、`primary_with_secondary`、`multi_with_primary`、`slider` 和 `axis_2d` 的基础输入解析，输入错误时会提示重新输入，不直接崩溃。

运行方式：

```bash
python -m if_game.questionnaire.runner
```

本次仍不做 UI、不接 AI API、不实现完整 Q001-Q150，也不接入现有 14 天主流程。

## v0.1.23 归因、记忆与关系信念系统设计

本项对应任务中的 `v0.1.19 归因、记忆与关系信念系统设计说明`。由于当前 README 已存在 `v0.1.19` 问卷 MVP 配置加载，实际版本记录顺延为 v0.1.23。

新增 `docs/design/25_attribution_memory_belief_system.md`，用于设计 IF 后续的事件解释层。该文档记录：

- 归因理论、内部/外部归因、稳定/易变归因、普遍/特殊归因在 IF 中的用途；
- 幸福伴侣与痛苦伴侣的不同归因模式；
- 自利归因、行动者/观察者效应、记忆重构和关系信念如何影响关系模拟；
- `attribution_style`、`positive_behavior_attribution`、`negative_behavior_attribution`、`actor_observer_gap`、`self_serving_bias`、`memory_reconstruction_bias`、`destiny_belief`、`growth_belief`、`mind_reading_expectation`、`conflict_destructive_belief` 等系统字段草案；
- 这些字段如何影响事件解释、关系满意度、多层信任、旧伤记忆、冲突升级、修复机会和报告标签；
- 晚回消息、神秘电话、异性饭局、争吵后冷处理、主动道歉和补偿等事件例子；
- 哪些字段未来适合加入 Q151-Q180 或后续补题。
- 补充真实原因层、解释可信度、可见线索和信任校准机制。

本次仍是纯文档设计，不修改 Python 代码，不修改现有题库 JSON，也不接入游戏运行逻辑。

## v0.1.24 关系事件解释原型

新增 `if_game/relationship_interpretation.py` 和 `tests/relationship_interpretation_test.py`，用于验证真实原因层、解释层、可见线索、证据强度、信任校准和“玩家/NPC判断 × 事实”四象限的最小计算路径。

该原型只提供纯函数计算，不接 AI API，不做复杂 UI，也不接入现有 14 天主流程。测试方式：

```bash
python tests/relationship_interpretation_test.py
```

## v0.1.25 伴侣认知准确度、形象管理与危险知觉系统设计

新增 `docs/design/26_partner_perception_and_impression_system.md`，用于补充 IF 的伴侣认知与关系解释底层机制。该文档记录：

- 伴侣认知不等于真实了解；
- 伴侣认知准确度、自信误读、投射偏差、旧印象固化和理想化；
- 形象管理随关系阶段变化，不能简单等同于“不爱了”或“更信任了”；
- 危险知觉既可能是准确警觉，也可能是误会/焦虑；
- 知觉者如何通过信任、怀疑、控制、鼓励或理想化反向塑造伴侣；
- 报告标签边界、事件模板和 `relationship_interpretation.py` 后续接口建议。

本次仍是纯文档设计，不修改 Python 代码，不修改问卷 JSON，也不接入游戏运行逻辑。

## v0.1.26 语言沟通、自我表露与秘密边界系统设计

新增 `docs/design/27_communication_self_disclosure_system.md`，用于沉淀 IF 的语言沟通、自我表露、回应性、秘密与禁忌话题机制。该文档记录：

- 自我表露的广度、深度和节奏；
- 社会渗透中的话题层级；
- 回应性、共情、情绪确认和安全表露空间；
- 正当隐私、秘密、禁忌话题和被发现后的信任影响；
- 开启者与倾听者能力；
- 依恋类型对沟通方式的影响；
- 爱意表达、言行一致和报告标签边界。

本次仍是纯文档设计，不修改 Python 代码，不修改问卷 JSON，也不接入游戏运行逻辑。

## v0.1.27 前期调查沟通表露模块设计

新增 `docs/design/28_questionnaire_communication_disclosure_module.md`，用于把沟通、自我表露、回应性、秘密边界和禁忌话题机制转化为前期问卷模块。该文档记录：

- `self_disclosure_willingness`、`disclosure_depth`、`disclosure_pacing`、`reciprocal_disclosure_need`、`privacy_boundary_strength` 等补强字段；
- 适合的题型：强制单选、多选并标主因、主次选择、滑条和二维坐标；
- 10 个核心问卷题草案；
- 自己表露程度 × 希望对方表露程度的二维题；
- 问卷报告标签和与游戏事件的接口；
- 与当前 25 题 MVP 的关系。

本次仍是纯文档设计，不直接修改 `if_game/data/questionnaire_mvp.json`。

## v0.1.28 冲突沟通与修复回应系统设计

新增 `docs/design/29_conflict_communication_repair_system.md`，用于沉淀 IF 的沟通障碍、冲突升级、积极倾听、精确表达、感受确认和修复回应机制。该文档记录：

- 偏题、旧账堆叠、读心、打断、反向抱怨；
- 批评、蔑视、防卫、石墙和交战状态；
- 行为描述、第一人称陈述和 XYZ 陈述；
- 安慰、同情、积极倾听、复述和知觉检验；
- 暂停机制、礼貌而坚定、尊重与感受确认；
- 冲突不是一律扣分，会修复的冲突可能比长期回避更健康。

本次仍是纯文档设计，不修改 Python 代码，不修改问卷 JSON，也不接入游戏运行逻辑。

## v0.1.29 社会交换、比较水平、替代选择与依赖权力系统设计

新增 `docs/design/30_social_exchange_dependency_system.md`，用于沉淀 IF 的社会交换、关系收益/代价、比较水平、替代选择、依赖度和关系权力机制。该文档记录：

- 奖赏、代价和关系结果；
- 比较水平 `CL` 与满意度；
- 替代比较水平 `CLalt` 与稳定性；
- 投入损失与离开成本；
- 依赖差异与关系权力；
- 幸福且稳定、不幸福但稳定、幸福但不稳定、不幸福且不稳定四种状态。

本次仍是纯文档设计，不把爱情简化为金钱交易，不接入游戏运行逻辑。

## v0.1.30 关系系统整合一致性规则

新增 `docs/design/31_system_integration_consistency_rules.md`，用于对 25-30 号设计文档进行横向校对，明确系统边界、优先级、数据流和冲突修正口径。该文档记录：

- 统一事件处理顺序；
- 事实层、解释层、认知层的边界；
- 自我表露与隐私边界的统一口径；
- 沉默、不回应、暂停与石墙的区别；
- 满意度、信任、依赖度、稳定性的区别；
- 避免重复扣信任、重复扣满意度和重复写旧伤；
- 后续实现建议使用 `relationship_state_aggregator` 汇总关系变化。

本次仍是纯文档设计，不修改 Python 代码，不修改问卷 JSON，也不接入游戏运行逻辑。

## v0.1.31 接近/回避动机、关系沉闷与关系动荡系统设计

新增 `docs/design/32_approach_avoidance_turbulence_system.md`，用于补充奖赏和代价的独立作用、接近动机、回避动机、关系沉闷、自我延伸和关系动荡机制。该文档记录：

- 接近奖赏和回避代价不是同一轴线的正反面；
- 高奖赏低代价、高奖赏高代价、低奖赏低代价、低奖赏高代价四种体验；
- 安全但沉闷、高刺激高风险、痛苦关系和丰盛关系的差异；
- 共同新鲜感、自我延伸、关系活力和沉闷累积；
- 亲密关系早期从随意约会过渡到严肃投入时的动荡期；
- 长期满意度轨迹不应简单线性下降。

本次仍是纯文档设计，不修改 Python 代码，不修改问卷 JSON，也不接入游戏运行逻辑。

## v0.1.32 共有关系、交换关系与公平系统设计

新增 `docs/design/33_communal_exchange_equity_system.md`，用于补充共有关系、交换关系、长期互惠、公平感、过度获益、获益不足、照顾动机和互惠规范机制。该文档记录：

- 亲密关系里既有交换，也有共有；
- 交换关系强调回报，共有关系强调关心对方幸福；
- 互惠不一定是即时对等，短期可以不对等，长期需要被珍惜和回应；
- 公平不是绝对五五分，而是贡献与结果比例的主观公平；
- 获益不足、过度获益、内疚、怨恨和被理所当然对待；
- 家务、照料、情绪劳动和关系修复是特别敏感的公平领域。

本次仍是纯文档设计，不修改 Python 代码，不修改问卷 JSON，也不接入游戏运行逻辑。

## v0.1.33 关系状态聚合器实施方案

新增 `docs/design/34_relationship_state_aggregator_implementation_plan.md`，用于把 25-33 号关系系统收束为后续可编码的统一结算层 `relationship_state_aggregator`。该文档记录：

- 聚合器目标与不做事项；
- 总体数据流；
- 输入结构和输出结构草案；
- 防止重复扣分规则；
- 隐私不等于欺骗、沉默不一定是石墙、争吵不一定扣分等关键裁决规则；
- MVP 实现范围；
- 后续测试用例和代码文件建议。

本次仍是纯文档设计，不修改 Python 代码，不修改问卷 JSON，也不接入游戏运行逻辑。

## v0.1.34 关系事件模板库

新增 `docs/design/35_relationship_event_template_library.md`，用于把 25-34 号关系系统转化为后续可写剧情、可做测试、可接入聚合器的事件母版。该文档记录：

- 统一事件模板结构；
- 认知误读事件；
- 自我表露与回应事件；
- 秘密与隐私事件；
- 冲突修复事件；
- 社会交换与依赖事件；
- 沉闷、新鲜感与动荡事件；
- 共有、交换与公平事件；
- 聚合器测试专用事件。

本次仍是纯文档设计，不修改 Python 代码，不修改问卷 JSON，也不接入游戏运行逻辑。

## v0.1.35 问卷扩展候选题池

新增 `docs/design/36_questionnaire_expansion_candidate_pool.md`，用于整理后续问卷扩展候选题。该文档记录：

- 沟通、自我表露与回应性候选题；
- 冲突沟通与修复候选题；
- 社会交换、替代选择与依赖候选题；
- 接近/回避、新鲜感与关系动荡候选题；
- 共有、交换与公平候选题；
- 轻量 4 题包、40 题快速扩展包和 60 题标准扩展包建议；
- 后续接入 `questionnaire_mvp.json` 时的计分和测试提醒。

本次仍是纯文档设计，不直接修改 `if_game/data/questionnaire_mvp.json`。

## v0.1.36 关系报告标签词典

新增 `docs/design/37_relationship_report_tag_dictionary.md`，用于统一 IF 关系报告、问卷报告、事件复盘和后续聚合器输出中的报告标签。该文档记录：

- 标签输出原则：非诊断、非羞辱、非道德审判、可行动；
- 认知与归因标签；
- 表露与回应标签；
- 秘密与边界标签；
- 冲突与修复标签；
- 社会交换与依赖标签；
- 接近/回避与关系动荡标签；
- 共有/交换/公平标签；
- 聚合器状态标签；
- 禁止标签清单和替代表达。

本次仍是纯文档设计，不修改 Python 代码，不修改问卷 JSON，也不接入游戏运行逻辑。

## v0.1.37 后续任务清单与 Codex 任务提示词库

新增 `docs/context/2026-06-07_after_relationship_docs_backlog.md` 和 `docs/context/codex_task_prompts.md`，用于整理 Codex 额度恢复后的后续任务和可直接复制的执行提示词。文档记录：

- 当前 25-37 关系系统文档状态；
- v0.1.33-v0.1.38 后续代码任务顺序；
- `relationship_state_aggregator.py` 原型任务提示；
- aggregator 关键裁决测试任务提示；
- `relationship_interpretation.py` 接入 aggregator 任务提示；
- 冲突沟通、社会交换/公平、问卷补题任务提示；
- 通用执行规则：不 force push、不接 AI API、不做 UI、不破坏当前控制台原型。

本次仍是纯文档设计，不修改 Python 代码，不修改问卷 JSON，也不接入游戏运行逻辑。

## v0.1.38 关系系统逻辑审查与优化清单

新增 `docs/design/38_relationship_system_logic_audit_and_optimization_notes.md`，用于对 25-37 号关系系统文档做第二轮横向逻辑审查。该文档记录：

- 当前系统链路总体成立，没有需要推翻重做的根本矛盾；
- 代码任务版本号应从 v0.1.38 顺延，避免与文档版本号冲突；
- 问卷候选维度需要映射到 128 维主表或建立别名表；
- 聚合器必须保留 `source_id`、`target_id` 等方向性字段；
- MVP 输出建议预留 `safety_delta`、`excitement_delta`、`fairness_delta`、`dependence_delta`；
- 后续需要统一枚举注册、结构化旧伤记忆、报告标签作用域和玩家可见/debug 边界。

本次仍是纯文档设计，不修改 Python 代码，不修改问卷 JSON，也不接入游戏运行逻辑。

## v0.1.39 问卷维度别名映射表

新增 `docs/design/39_questionnaire_dimension_alias_mapping.md`，用于把 36 号候选题池中的新系统变量映射到 16 号 128 维主表中的正式维度 ID。该文档记录：

- 问卷 JSON 的 `dimensions` 字段只能使用 128 维正式 ID；
- 36 号文档里的新变量可作为设计别名、系统变量、报告标签或聚合器字段，但不应直接写入 `dimensions`；
- 沟通表露、冲突修复、社会交换、接近/回避、共有/公平等候选变量的正式维度映射；
- 不应直接写进 `dimensions` 的运行时标签和状态；
- 后续接入 `questionnaire_mvp.json` 时的字段规则、反向计分提醒和测试要求。

本次仍是纯文档设计，不修改 Python 代码，不修改问卷 JSON，也不接入游戏运行逻辑。

## v0.1.40 关系枚举与字段注册表

新增 `docs/design/40_relationship_enum_and_field_registry.md`，用于统一 IF 关系系统中的枚举值、字段名和标签 ID。该文档记录：

- 通用强度等级；
- `event_type`、`truth_type`、`observable_trace`、`interpretation_type`、`interpretation_accuracy` 等枚举；
- 沟通回应类型和冲突回应类型；
- 聚合器输入字段注册表；
- `RelationshipStateDelta` 输出字段注册表；
- 报告标签 ID 注册表；
- `ReportTag` 和 `RelationshipMemory` 结构建议；
- 禁止/废弃字符串和替代表达。

本次仍是纯文档设计，不修改 Python 代码，不修改问卷 JSON，也不接入游戏运行逻辑。

## v0.1.41 关系记忆衰减与模式阈值规则

新增 `docs/design/41_relationship_memory_decay_and_pattern_rules.md`，用于补充 IF 的重复事件、旧伤记忆、修复记忆、时间衰减、模式阈值和长期关系信念更新规则。该文档记录：

- 关系记忆类型：正向记忆、修复记忆、旧伤记忆、模式记忆；
- `RelationshipMemory` 结构草案；
- `pattern_key`、重复事件阈值和高伤害事件一次写入旧伤的规则；
- `decay_policy`、时间衰减策略和修复质量等级；
- 旧伤再触发、正向记忆与关系韧性；
- 问卷自述与游戏行为的动态校准；
- 玩家可见报告与 debug 报告的边界。

本次仍是纯文档设计，不修改 Python 代码，不修改问卷 JSON，也不接入游戏运行逻辑。

## v0.1.42 关系状态聚合器原型

新增 `if_game/relationship_state_aggregator.py` 和 `tests/relationship_state_aggregator_test.py`，用于将单次关系事件汇总为可测试、可解释、带方向性的关系状态变化。

本版本新增 `RelationshipStateDelta`，输出字段包括：

- `source_id`、`target_id`；
- `trust_delta`、`satisfaction_delta`、`intimacy_delta`、`stability_delta`；
- `repair_chance_delta`、`old_wound_memory_delta`；
- `safety_delta`、`excitement_delta`、`fairness_delta`、`dependence_delta`；
- `report_tags`、`memory_notes`、`debug_reasons`。

新增 `aggregate_relationship_event()`，第一版支持 dict 输入，并实现以下 MVP 裁决规则：

- 隐私边界冲突不等于欺骗；
- 高欺骗和高伤害主要由 `trust_delta` 承担，避免多个系统重复扣信任；
- 石墙会降低修复机会并增加旧伤记忆；
- 高质量修复会提升修复机会；
- 重复事件和修复后再犯会写入 `memory_notes`；
- MVP 先预留 `safety_delta`、`excitement_delta`、`fairness_delta`、`dependence_delta` 字段，方便后续 v0.1.43-v0.1.46 扩展。

测试方式：

```bash
python tests/relationship_state_aggregator_test.py
```

本次仍不接 AI API，不做 UI，不接完整事件引擎，不修改问卷 JSON，也不破坏当前 14 天控制台原型。

## v0.1.43 关系状态聚合器关键裁决测试

补充 `tests/relationship_state_aggregator_test.py` 中的 aggregator 关键裁决用例，覆盖沉默/石墙、冲突修复、准确警觉、误会焦虑、隐私与欺骗、低痛苦与高快乐、高快乐与安全、公平比例以及同一事件不重复扣信任等规则。

同步轻量扩展 `if_game/relationship_state_aggregator.py`，让预留的 `safety_delta`、`excitement_delta`、`fairness_delta` 能支持本轮方向性裁决测试。

本次仍不接 AI API，不做 UI，不修改问卷 JSON，不接完整事件引擎，也不破坏当前 14 天控制台原型。

## v0.1.44 关系解释层轻量接入聚合器

新增 `interpretation_to_aggregator_input()`，让 `if_game/relationship_interpretation.py` 的解释结果可以转换为 `relationship_state_aggregator.py` 已支持的 dict 输入，并交给 `aggregate_relationship_event()` 结算。

本版本仅做轻量映射和 0-100 到 0-10 的尺度转换，覆盖准确警觉、误会/焦虑和真实欺骗路径；不接主流程，不接 AI API，不做 UI，不修改问卷 JSON，也不破坏当前 14 天控制台原型。

## v0.1.45 冲突沟通事件样例接入聚合器

新增 `if_game/conflict_event_samples.py`，提供 E-CON-01 迟到抱怨、E-CON-02 有效暂停争吵、E-CON-03 嘲讽脆弱表达等轻量事件样例，并可直接交给 `aggregate_relationship_event()` 结算。

同步轻量增强 `relationship_state_aggregator.py` 对 `conflict_response_type`、`defensive_response` 和 `contempt_signal` 的识别，覆盖修复、防卫/反向抱怨、有效暂停不是石墙、嘲讽脆弱表达写旧伤等方向性测试。本次仍不接 AI API，不做 UI，不修改问卷 JSON，也不接入复杂剧情树或完整事件引擎。

## v0.1.46 社会交换与公平轻量接入聚合器

新增 `if_game/exchange_event_samples.py`，提供安全但沉闷、长期获益不足、主动看见并补偿付出等轻量事件样例，并可直接交给 `aggregate_relationship_event()` 结算。

同步补齐 `relationship_state_aggregator.py` 对 `dependence_delta` 的轻量支持，并继续通过 `relationship_rewards_delta`、`relationship_costs_delta`、`approach_reward_delta`、`avoidance_cost_pressure_delta`、`boredom_delta`、`perceived_equity_delta`、`underbenefit_feeling_delta`、`taken_for_granted_delta` 等字段处理满意度、安全感、活力、公平感和依赖变化。本次不实现完整 CL/CLalt 大系统，不接 AI API，不做 UI，不修改问卷 JSON，也不破坏当前 14 天控制台原型。

## v0.1.47 沟通表露问卷补题

在 `if_game/data/questionnaire_mvp.json` 中新增 Q-COM-01、Q-COM-05、Q-COM-06、Q-COM-10 四道沟通表露题，MVP 问卷从 25 题扩展为 29 题。

新增题目只使用现有 runner/scoring 支持的题型，并将候选维度映射到 128 维正式 ID；报告层新增“沟通表露摘要”，用于呈现直接沟通、回应性需求、透明期待、手机隐私需求和表露规则一致性风险。本次不接 AI API，不做 UI，不扩展到 40-60 题，也不破坏当前 14 天控制台原型。

## v0.1.48 关系系统代码落地复盘

新增 `docs/context/2026-06-07_v0_1_48_relationship_code_landing_review.md`，复盘 v0.1.42-v0.1.47 中 aggregator、解释层适配器、冲突/交换事件样例和沟通表露问卷的代码落地情况。

文档明确当前模块数据流、尚未接入主流程/14 天事件/试玩报告/长期记忆/问卷初始状态的边界，以及下一阶段推荐任务顺序。本次只更新文档，不修改 Python 代码，不修改问卷 JSON，不接 UI 或 AI API。

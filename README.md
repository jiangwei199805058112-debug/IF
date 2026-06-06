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
```

## 问卷 MVP JSON 配置

当前已新增最小可读取问卷配置：

```text
if_game/data/questionnaire_mvp.json
```

配置先覆盖 Q001-Q030 中的 10 道 MVP 题，用于验证真实 JSON 配置、基础字段校验和后续计分落地路径。当前只做配置加载，不做 UI，不接 AI API，也不接入 14 天控制台原型主流程。

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

该入口会读取 `if_game/data/questionnaire_mvp.json` 中的 10 道 MVP 题，按顺序展示题号、标题、题干、选项或滑条/二维坐标提示，收集答案后调用 loader、scoring 和 reporting 生成中文问卷报告。当前只作为问卷 MVP 独立验证入口，不接 UI、不接 AI API，也不接入 14 天主流程。

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

新增 `if_game/data/questionnaire_mvp.json`，从 Q001-Q030 中抽取 10 道题作为最小真实 JSON 配置，覆盖关系入口、联系频率、依恋坐标、每日联系、个人空间、脆弱暴露、依赖求助、冲突修复和依恋自评。

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

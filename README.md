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
```

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

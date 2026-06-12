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

## 未来创意池

以下文档只记录未来方向，不代表当前阶段开始做正式 UI、正式美术、引擎迁移或 AI API 接入：

1. `docs/ideas/01_visual_life_scene_concept.md`：生活场景画面、学生/成年人信息载体、手机/电脑/书本、桌面物品、天气、车内和预设人物方向。
2. `docs/ideas/02_visual_system_code_backlog.md`：未来如需落地画面系统，代码层面和游戏底层需要新增的数据结构、服务、事件字段和测试方向。
3. `docs/ideas/03_home_tablet_speaker_extension.md`：家庭场景中平板、音箱、音乐、影音和共享计划等升级设备创意。

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

## v0.1.60 试玩体验小修

v0.1.59 已修复互动模式反馈延迟，玩家每天选择后即可看到 NPC 回应和氛围变化。v0.1.60 继续修正试玩体验细节：事件标题不再在交互提示中重复，第 12 天“约定私下把问题说清”会按修复窗口处理，普通日高频 NPC 回应加入轻量轮换，开局样例组合改名为“快速预设组合”并补充用途说明。

未来视觉生活场景、家庭平板 / 音箱和底层画面系统仍只保存在创意池文档中；当前阶段不做 UI、不迁移引擎、不接 AI API。

运行方式：

```bash
python -m if_game.main
```

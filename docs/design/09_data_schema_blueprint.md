# 数据结构蓝图 v0.1

本文件把现有规则整理成未来可编码的数据结构蓝图。本次只写文档，不创建代码、数据库或配置文件。

## 1. 设计目标

- 把角色、关系、日程、事件、分支、记忆和后果整理成稳定对象。
- 保留真实值与感知值分离。
- 保留事件卡的真实层、感知层、后果层。
- 使用方向性后果，不把事件写成固定数值加减。
- 让 v0.1 后续能先用 JSON/YAML 配置驱动控制台原型。

## 2. 总体数据对象

| 对象 | 用途 | 关键字段 | 示例 | v0.1 是否启用 | 与其他对象的关系 |
| --- | --- | --- | --- | --- | --- |
| `CharacterProfile` | 记录玩家或 NPC 的基础档案 | `id`、`display_name`、`age`、`work_status` | `player_a`、`林夏`、`24`、`上班` | 启用 | 包含 `PersonalityModel`，关联 `ScheduleState` |
| `PersonalityModel` | 记录可计算性格维度 | `security_need`、`honesty_tendency`、`double_standard_tendency` | `security_need: high` | 启用 | 被 `CharacterProfile` 引用，影响事件和 NPC 反应 |
| `RelationshipState` | 记录系统内部真实关系状态 | `stage`、`trust`、`pressure`、`breakup_thought` | `stage: ambiguous` | 启用 | 与两名角色、记忆和边界协议关联 |
| `PerceivedRelationshipState` | 记录玩家可感知状态 | `feedback_level`、`visible_summary` | `轻微不安` | 启用 | 从 `RelationshipState`、事件可见信息和玩家性格生成 |
| `ScheduleState` | 记录某天某时间段日程 | `day`、`time_block`、`status` | `day: 3`、`白天`、`上班` | 启用 | 被事件触发和压力系统读取 |
| `EventCard` | 记录事件基础定义 | `event_id`、`title`、`branches` | `MSG_001` | 启用 | 包含多个 `EventBranch` |
| `EventBranch` | 记录事件真实分支 | `branch_id`、`truth`、`npc_explanation` | `MSG_001_E` | 启用 | 属于 `EventCard`，产生 `OutcomeDelta` |
| `ChoiceOption` | 记录玩家可选行为 | `choice_id`、`label`、`behavior_tags` | `追问` | 启用 | 挂在事件或分支上，影响 NPC 反应 |
| `MemoryEntry` | 记录重要历史 | `memory_id`、`event_id`、`resolved` | `冷战未解决` | 启用 | 被阶段判定、旧账和反馈读取 |
| `BoundaryAgreement` | 记录双方边界协议 | `opposite_sex_meal_rule`、`privacy_rule` | `异性饭局需提前说明` | 启用 | 被事件严重度和记忆写入读取 |
| `PressureState` | 记录压力来源和强度 | `work`、`family`、`relationship` | `work: medium` | 启用 | 影响回复、撒谎、冷处理和情绪爆发 |
| `OutcomeDelta` | 记录方向性后果 | `trust`、`pressure`、`flaw`、`crisis` | `trust: medium_down` | 启用 | 由分支和选择产生，作用于真实/感知/记忆 |

## 3. CharacterProfile 角色档案

用途：记录玩家和 NPC 的基础身份、社会信息、关系入口和关键倾向。

| 字段 | 含义 | 示例 | v0.1 要求 |
| --- | --- | --- | --- |
| `id` | 角色唯一标识 | `npc_busy_avoidant` | 必填 |
| `display_name` | 显示姓名 | `林夏` | 必填 |
| `gender` | 性别表达 | `female` | 必填 |
| `age` | 年龄 | `24` | 必填，用于成年校验 |
| `city` | 所在城市 | `上海` | 必填 |
| `relationship_entry_mode` | 开局模式 | `ambiguous` | 必填，只允许正在聊天/暧昧中/刚恋爱 |
| `known_duration` | 认识时长 | `3_months` | 必填 |
| `education_level` | 学历 | `bachelor` | 后续扩展 |
| `work_status` | 工作/上学/求职状态 | `working` | 必填 |
| `income_level` | 收入区间 | `medium` | v0.1 部分启用 |
| `family_income_level` | 家庭收入区间 | `normal` | 后续扩展 |
| `sibling_structure` | 兄弟姐妹结构 | `only_child` | 后续扩展 |
| `living_status` | 居住方式 | `alone` | v0.1 启用 |
| `friend_count_level` | 朋友数量等级 | `medium` | v0.1 部分启用 |
| `opposite_sex_friend_level` | 异性朋友数量等级 | `high` | 必填 |
| `ex_contact_status` | 前任联系状态 | `occasional` | 必填 |
| `public_relationship_preference` | 公开关系偏好 | `private_first` | v0.1 启用 |
| `intimacy_pace` | 亲密接受节奏 | `slow` | 后续扩展，成年角色才可进入 |
| `contraception_awareness` | 避孕意识 | `high` | 后续扩展，成年角色才可进入 |
| `responsibility_level` | 责任感等级 | `medium_high` | 必填 |

关系：`CharacterProfile` 引用一个 `PersonalityModel`；在运行时与另一名角色组成 `RelationshipState`。

## 4. PersonalityModel 性格模型

用途：把性格拆成可计算维度。建议值域先用 `low`、`medium`、`high`，后续实现可映射到数值。

| 字段 | 高值表现 | 低值表现 | 影响事件 | v0.1 是否启用 |
| --- | --- | --- | --- | --- |
| `security_need` | 需要稳定回复、确认和承诺 | 能接受不确定和延迟 | `MSG_001`、`CONFLICT_001` | 启用 |
| `emotional_stability` | 情绪恢复快，较少爆发 | 易爆发、冷战或拉黑 | `CONFLICT_001` | 启用 |
| `communication_initiative` | 主动解释、主动修复 | 等对方开口或拖延 | 三个种子事件 | 启用 |
| `conflict_style` | 可取值：直接、回避、冷处理、爆发 | 不是高低值，而是风格 | `CONFLICT_001` | 启用 |
| `trust_baseline` | 更愿意先相信解释 | 容易怀疑和查证 | `MSG_001`、`SOC_001` | 启用 |
| `jealousy_tendency` | 异性社交容易触发吃醋 | 对异性朋友较开放 | `SOC_001` | 启用 |
| `boundary_sensitivity` | 对隐私、异性和亲密边界敏感 | 对边界较宽松 | `SOC_001`、`CONFLICT_001` | 启用 |
| `romance_need` | 需要仪式感和情绪表达 | 更重视日常稳定 | 餐厅/礼物钩子 | 部分启用 |
| `money_sensitivity` | 消费差异容易形成压力 | 对消费不敏感 | 餐厅/礼物钩子 | 部分启用 |
| `future_planning_need` | 需要明确关系方向 | 能接受慢慢看 | 第14天结算 | 部分启用 |
| `family_dependency` | 家庭意见影响强 | 独立决策 | 家庭压力钩子 | 暂缓 |
| `social_openness` | 社交多，异性接触机会多 | 社交圈较小 | `SOC_001` | 启用 |
| `independence_level` | 重视个人空间和自主 | 更依赖关系互动 | 消息、边界、隐私 | 启用 |
| `responsibility` | 愿意承担后果和修复 | 容易逃避责任 | 撒谎、修复、危机 | 启用 |
| `honesty_tendency` | 更倾向坦白 | 更容易隐瞒或模糊 | `SOC_001` | 启用 |
| `avoidance_tendency` | 压力下容易拖延和回避 | 倾向当场处理 | `MSG_001`、`CONFLICT_001` | 启用 |
| `double_standard_tendency` | 自己可做但限制对方 | 规则一致性更高 | `SOC_001` | 启用 |
| `test_tendency` | 喜欢试探和考验 | 更直接表达需求 | `MSG_001`、修复事件 | 启用 |
| `material_need` | 礼物和消费影响被重视感 | 物质要求低 | 餐厅/礼物钩子 | 部分启用 |
| `social_display_need` | 需要公开展示关系或面子 | 不重视外部展示 | 公共场合、公开关系 | 启用 |

## 5. RelationshipState 关系状态

用途：记录系统内部真实关系状态，玩家不能直接看到。

关键字段：

- `relationship_id`：关系唯一标识。
- `player_id`：玩家角色 ID。
- `npc_id`：NPC 角色 ID。
- `stage`：当前阶段，例如 `chatting`、`ambiguous`、`new_relationship`、`cold`、`breakup_crisis`。
- `affection`：真实好感方向状态。
- `trust`：真实信任方向状态。
- `security`：真实安全感方向状态。
- `pressure`：真实关系压力方向状态。
- `conflict`：真实矛盾方向状态。
- `disappointment`：真实失望方向状态。
- `physical_attraction`：生理吸引方向状态。
- `psychological_liking`：心理喜欢方向状态。
- `breakup_thought`：分手念头方向状态。
- `guilt`：愧疚感方向状态。
- `flaw_level`：当前破绽等级。
- `satisfaction`：关系满意度方向状态。
- `unresolved_conflict_count`：未解决冲突数量等级。
- `active_hooks`：待触发后续钩子列表。

示例：

```text
relationship_id: rel_A_001
stage: ambiguous
trust: medium
security: slightly_low
pressure: medium_high
active_hooks: [SOC_001, conflict_followup]
```

v0.1 启用：启用核心字段；`guilt` 和 `satisfaction` 可先作为方向状态保留。

## 6. PerceivedRelationshipState 感知关系状态

用途：记录玩家看到的模糊状态，而不暴露真实值。

关键字段：

- `feedback_level`：`stable`、`slight_unease`、`obvious_abnormal`、`strong_suspicion`、`relationship_crisis`。
- `visible_summary`：玩家可见一句话总结。
- `uncertainty_sources`：不确定来源，例如回复延迟、解释含糊、朋友圈线索。
- `suspected_hooks`：玩家怀疑的方向，不等于真实钩子。
- `last_visible_event_id`：最近影响感知的事件。

示例：

```text
feedback_level: slight_unease
visible_summary: 你感觉对方可能只是忙，但解释比平时少。
uncertainty_sources: [reply_delay, vague_explanation]
```

v0.1 启用：启用。

## 7. ScheduleState 日程状态

用途：记录每天四个时间段的日程和压力来源。

关键字段：

- `day`：第几天。
- `time_block`：`morning`、`daytime`、`evening`、`late_night`。
- `character_id`：角色 ID。
- `status`：`working`、`school`、`job_hunting`、`resting`、`overtime`、`exam`、`interview`、`family_matter`、`social_plan`。
- `reply_availability`：回复可用性，`low`、`medium`、`high`。
- `pressure_sources`：压力来源列表。
- `possible_event_hooks`：可能触发的事件钩子。

示例：`day: 3`、`time_block: daytime`、`status: working`、`reply_availability: low`。

v0.1 启用：启用。

## 8. EventCard 事件卡

用途：定义一个事件的稳定信息和三层结构。

关键字段：

- `event_id`：例如 `MSG_001`。
- `title`：事件名。
- `enabled_in_v0_1`：是否启用。
- `applicable_stages`：适用阶段。
- `trigger_conditions`：触发条件。
- `participants`：参与角色类型。
- `truth_layer`：真实层基础字段。
- `perception_layer`：感知层基础字段。
- `outcome_layer`：后果层基础字段。
- `branches`：分支 ID 列表。

三层结构必须保留：

- 真实层：真实发生了什么、真实对象、真实目的、是否撒谎、是否有破绽。
- 感知层：玩家看到什么、不知道什么、可能误判什么、可用选项、模糊提示。
- 后果层：真实后果、感知反馈、破绽变化、压力变化、记忆、钩子、阶段变化。

v0.1 启用：启用 `MSG_001`、`SOC_001`、`CONFLICT_001`。

## 9. EventBranch 事件分支

用途：表达同一事件下不同真实情况。

关键字段：

- `branch_id`：例如 `MSG_001_E`。
- `event_id`：所属事件。
- `truth`：真实情况。
- `player_visible_info`：玩家看到的信息。
- `npc_explanation_style`：NPC 解释方式。
- `available_choices`：玩家可选行为。
- `behavior_tags`：主要行为标签。
- `real_outcome`：真实后果方向。
- `perceived_feedback`：玩家看到的反馈。
- `flaw_delta`：破绽变化。
- `memory_write_rule`：记忆写入规则。
- `followup_hooks`：后续钩子。

示例：

```text
branch_id: MSG_001_E
truth: 正在隐瞒异性社交
npc_explanation_style: 隐瞒重点
behavior_tags: [隐瞒重点, 查证, 强硬质问]
flaw_delta: medium_up
memory_write_rule: write_if_questioned_or_repeated
```

v0.1 启用：启用。

## 10. ChoiceOption 玩家选项

用途：把玩家看到的选项转成行为标签。

关键字段：

- `choice_id`：选项唯一标识。
- `label`：显示文本，例如“温和确认”。
- `description`：玩家行为说明。
- `behavior_tags`：行为标签列表。
- `tone_strength`：表达强度，`low`、`medium`、`high`。
- `information_gain`：是否可能获得更多信息。
- `risk_notes`：风险说明。

示例：`choice_id: ask_softly`、`behavior_tags: [温和确认, 追问]`、`tone_strength: low`。

v0.1 启用：启用。

## 11. MemoryEntry 记忆账本

用途：记录会影响后续事件的关系历史。

关键字段：

- `memory_id`。
- `event_id`。
- `branch_id`。
- `day`。
- `summary`。
- `truth_summary`。
- `perceived_summary`。
- `behavior_tags`。
- `resolved`：是否解决。
- `emotional_residue`：情绪残留等级。
- `future_trigger_conditions`：旧账触发条件。
- `long_term_effects`：长期方向影响。

示例：`summary: 异性饭局半真半假`、`resolved: false`、`future_trigger_conditions: [similar_social_event, late_night_conflict]`。

v0.1 启用：启用。

## 12. BoundaryAgreement 边界协议

用途：记录双方已经说清或默认存在的关系边界。

关键字段：

- `public_relationship_rule`：是否公开关系。
- `opposite_sex_meal_rule`：异性饭局规则。
- `ex_contact_rule`：前任联系规则。
- `privacy_rule`：手机、聊天记录、定位等隐私规则。
- `late_reply_rule`：延迟回复是否需要解释。
- `conflict_resolution_rule`：吵架后处理规则。
- `intimacy_pace_rule`：亲密节奏规则，成年角色才可进入。
- `money_rule`：餐厅、礼物、AA 或请客规则。

示例：`opposite_sex_meal_rule: need_prior_notice`。

v0.1 启用：启用异性饭局、隐私、延迟回复和冲突处理边界；亲密和金钱规则部分启用或暂缓。

## 13. PressureState 压力状态

用途：记录双方当前压力，解释非恶意冷淡，也影响撒谎和冲突。

关键字段：

- `work_pressure`。
- `school_pressure`。
- `job_hunting_pressure`。
- `family_pressure`。
- `money_pressure`。
- `relationship_pressure`。
- `social_pressure`。
- `body_pressure`。
- `intimacy_pressure`。
- `sleep_debt`。
- `overload_level`。

示例：`work_pressure: high`、`relationship_pressure: medium`、`sleep_debt: low`。

v0.1 启用：启用工作/学校/求职、关系、社交、睡眠压力；家庭、金钱和亲密压力作为钩子保留。

## 14. OutcomeDelta 后果方向

用途：记录后果方向，不直接写固定数值。

允许值：

```text
none
slight_up
medium_up
large_up
slight_down
medium_down
large_down
crisis_trigger
conditional
```

说明：

- 这只是方向描述。
- 未来实现时可以映射成数值区间。
- 玩家仍然不直接看到内部变化。
- `crisis_trigger` 表示可绕过慢性累积，直接进入危机判定。
- `conditional` 表示需要根据性格、压力、记忆或边界再判断。

常见字段：

- `affection_delta`。
- `trust_delta`。
- `security_delta`。
- `pressure_delta`。
- `conflict_delta`。
- `disappointment_delta`。
- `breakup_thought_delta`。
- `flaw_delta`。
- `memory_delta`。
- `stage_weight_delta`。

## 15. v0.1 启用字段与暂缓字段

v0.1 必须启用：

- 角色基础档案：姓名、年龄、城市、开局模式、认识时长、工作状态、异性朋友、前任联系、责任感。
- 性格模型：安全感、情绪稳定、沟通主动、信任基线、吃醋、边界、诚实、回避、双标、试探。
- 关系状态：阶段、好感、信任、安全感、压力、矛盾、失望、分手念头、破绽、未解决冲突。
- 感知状态：反馈级别、可见总结、不确定来源。
- 日程：天数、时间段、状态、回复可用性、压力来源。
- 事件：`MSG_001`、`SOC_001`、`CONFLICT_001`。
- 记忆：写入、是否解决、情绪残留、后续触发条件。
- 后果：方向性 `OutcomeDelta`。

v0.1 暂缓：

- 完整经济资产。
- 完整亲密和同居数据。
- 意外怀孕详细流程。
- 双重账号完整追踪。
- 大规模社交网络。
- AI 自然语言解析。
- 数据库表结构。
- UI 状态结构。

## 16. 心理学扩展字段建议

以下字段是后续扩展建议，不直接修改 v0.1 已启用对象字段。进入 MVP 前需要再确认是否加入配置文件和数据模型。

| 字段 | 含义 | 来源理论 | 影响系统 | v0.1 是否启用 | 后续是否建议加入 MVP |
| --- | --- | --- | --- | --- | --- |
| `attachment_style` | 角色在亲密关系中的安全、焦虑、回避或恐惧/混乱倾向 | 成人依恋理论 | `MSG_001` 敏感度、冷战/拉黑、复联、分分合合倾向 | 暂不作为独立字段启用，现由多个维度间接表达 | 建议加入，但只作为倾向，不输出诊断 |
| `primary_love_language` | 最主要的被重视方式 | 爱的五种语言 | 礼物、陪伴、安慰、服务行动、亲密节奏反馈 | 暂不启用 | 建议后续加入样例角色 |
| `secondary_love_language` | 次要被重视方式 | 爱的五种语言 | 当主要需求无法满足时提供替代修复路径 | 暂不启用 | 可在扩展礼物/陪伴事件时加入 |
| `communication_pattern` | 常见沟通模式，例如温和确认、强硬质问、回避、冷处理 | 非暴力沟通、戈特曼冲突理论 | 玩家选项、NPC 反应、冲突升级 | 由行为标签间接表达 | 建议加入 MVP 配置 |
| `gottman_risk_flags` | 批评、鄙视、辩护、冷战/筑墙等高风险沟通标记 | 戈特曼四骑士 | 未解决冲突、记忆写入、分手危机权重 | 暂不作为独立字段启用 | 建议加入测试用例，不直接展示给玩家 |
| `repair_willingness` | 冲突后愿意主动修复的倾向 | 戈特曼修复尝试、非暴力沟通、大五宜人性 | 道歉、私下沟通、补偿、设边界 | 由责任感和沟通主动性间接表达 | 建议加入 MVP |
| `commitment_intent` | 对公开关系、长期规划、同居、求婚等承诺行为的意愿 | 斯滕伯格爱情三角理论：承诺 | 第14天阶段结算、确认关系、长期稳定 | 暂不启用 | 建议在 v0.2 或承诺系统前加入 |
| `need_alignment` | 双方需求和爱的语言是否匹配 | 爱的五种语言、马斯洛需求层次 | 被重视感、失望、修复效果 | 暂不启用 | 可在礼物/陪伴事件扩展时加入 |
| `self_awareness_gap` | 自评和实际行为之间的差距 | 认知失调、自我认知偏差 | 问卷复盘、结局复盘、行为预测误差 | 暂不启用 | 可作为纸面测试和后续复盘字段 |

设计限制：

- 这些字段不能用于诊断玩家或现实人物。
- 不能把 `attachment_style` 或任何心理字段写成固定命运。
- 玩家可见文本只描述行为和关系感受，不直接输出心理学标签。
- 如果字段加入 MVP，也应通过事件、选项、行为标签和反馈文本间接体现。

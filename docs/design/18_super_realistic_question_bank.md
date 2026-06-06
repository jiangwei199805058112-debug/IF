# 超级真实版题库 v0.1

本文档用于整理 IF 完整调查问卷的“超级真实版”题库。它承接：

- `docs/design/15_full_questionnaire_upgrade_plan.md`
- `docs/design/16_questionnaire_dimension_table.md`
- `docs/design/17_question_type_schema.md`

当前文件完成第一批题库：**基础资料 + 恋爱经历 + 依恋亲密**。超级真实版题库后续批次已拆分到：

- `docs/design/18_super_realistic_question_bank_part2.md`：信任怀疑、边界占有、诚实隐瞒、双标检测；
- `docs/design/18_super_realistic_question_bank_part3.md`：冲突沟通、欲望忠诚、道德责任；
- `docs/design/18_super_realistic_question_bank_part4.md`：社交网络、现实压力、数字生活、家庭成长、综合反向验证。

本文档只做题库设计，不修改控制台原型运行逻辑。

## 1. 题库总体目标

超级真实版目标题量：100-180题。第一版以 Q001-Q150 为完整结构。

| 批次 | 模块 | 目标题量 | 状态 |
| --- | --- | ---: | --- |
| 第一批 | 基础资料、恋爱经历、依恋亲密 | 约30题 | 本文档已完成 |
| 第二批 | 信任怀疑、边界占有、诚实隐瞒 | 约40题 | 已完成，见 `18_super_realistic_question_bank_part2.md` |
| 第三批 | 冲突沟通、欲望忠诚、道德责任 | 约40题 | 已完成，见 `18_super_realistic_question_bank_part3.md` |
| 第四批 | 社交网络、现实压力、数字生活、双标/反向验证 | 约40题 | 已完成，见 `18_super_realistic_question_bank_part4.md` |

## 2. 题目格式说明

每道题尽量包含：

| 字段 | 含义 |
| --- | --- |
| `题型` | 对应 `17_question_type_schema.md` 的 `selection_mode` |
| `题目` | 玩家看到的问题正文 |
| `选项/结构` | 选项、滑条、排序或权重内容 |
| `影响维度` | 对应128维主表中的维度ID |
| `备注` | 设计用途、反向验证、报告标签等 |

题库不是一次性把玩家定型。每个维度应由多题、反向题和后续行为共同确认。

## 3. 第一批题库：基础资料

### Q001 关系入口

- 题型：`forced_single`
- 题目：你们当前的关系更接近哪一种？
- 选项：
  - A. 刚认识，还在普通聊天。
  - B. 已经频繁聊天，有一点暧昧。
  - C. 暧昧明显，但还没有正式确认关系。
  - D. 刚确认恋爱关系。
  - E. 已经分手，但最近又开始联系。
- 影响维度：`attachment_commitment_pace`、`values_belonging_need`
- 备注：用于确定初始关系阶段，不直接判断人格。

### Q002 认识方式

- 题型：`forced_single`
- 题目：你们最初是怎么认识的？
- 选项：
  - A. 学校或课程。
  - B. 工作、兼职或项目。
  - C. 朋友介绍或共同圈子。
  - D. 社交软件或网络平台。
  - E. 线下偶遇、吃饭、逛街或搭讪。
  - F. 前任复联或旧关系重新联系。
- 影响维度：`social_circle_overlap_need`、`digital_alt_account_tendency`、`social_reputation_sensitivity`
- 备注：用于后续社交网络、共同朋友和暴露路径。

### Q003 认识时长

- 题型：`forced_single`
- 题目：你们认识了多久？
- 选项：
  - A. 少于一周。
  - B. 一周到一个月。
  - C. 一到三个月。
  - D. 三个月到一年。
  - E. 一年以上。
- 影响维度：`trust_baseline`、`attachment_repair_receptivity`
- 备注：用于调整信任建立速度和事件严重度。

### Q004 联系频率

- 题型：`forced_single`
- 题目：你们现在通常多久联系一次？
- 选项：
  - A. 几乎全天都有消息。
  - B. 每天都会聊，但不是一直聊。
  - C. 一两天聊一次。
  - D. 想起来才聊，不固定。
  - E. 最近明显变少。
- 影响维度：`digital_response_norm`、`attachment_closeness_need`、`social_dependency`
- 备注：用于消息延迟、冷淡感知和关系阶段判断。

### Q005 现实距离

- 题型：`forced_single`
- 题目：你们现实中的距离更接近哪种？
- 选项：
  - A. 同城，见面比较方便。
  - B. 同城，但学习/工作节奏很难约。
  - C. 不同城市，但可以偶尔见面。
  - D. 异地，见面成本很高。
  - E. 主要是网络联系。
- 影响维度：`stability_resource_availability`、`stability_adaptability`、`digital_response_norm`
- 备注：用于现实压力和消息依赖。

### Q006 当前生活重心

- 题型：`multi_with_primary`
- 题目：你现在生活中最占精力的事情有哪些？可以多选，并标出最主要的一项。
- 选项：
  - A. 学业或考试。
  - B. 工作、实习或兼职。
  - C. 家庭压力。
  - D. 赚钱、债务或经济压力。
  - E. 身体状态或作息问题。
  - F. 社交、人际关系。
  - G. 这段关系本身。
- 影响维度：`stability_environmental_pressure`、`values_achievement_need`、`family_obligation_pressure`、`stability_resource_availability`
- 备注：用于压力来源和关系投入能力。

### Q007 公开程度

- 题型：`forced_single`
- 题目：如果你们进入或已经处在恋爱关系中，你更倾向于多公开？
- 选项：
  - A. 希望自然公开，朋友知道也没关系。
  - B. 希望重要朋友知道，但不必发朋友圈。
  - C. 先低调，等稳定再公开。
  - D. 不太想公开，关系是两个人的事。
  - E. 希望对方公开，但自己不一定想公开。
- 影响维度：`digital_social_media_display`、`social_reputation_sensitivity`、`boundary_double_standard`
- 备注：E 可用于双标检测。

### Q008 当前关系目标

- 题型：`ranked_multi`
- 题目：你现在最希望这段关系往哪些方向发展？请选择最多三项并排序。
- 选项：
  - A. 稳定恋爱。
  - B. 慢慢了解，不急着定性。
  - C. 更多陪伴和联系。
  - D. 更明确的未来规划。
  - E. 保持轻松，不要太有压力。
  - F. 重新修复过去的问题。
  - G. 只是看看还有没有感觉。
- 影响维度：`attachment_commitment_pace`、`values_security_need`、`values_freedom_need`、`attachment_repair_receptivity`
- 备注：用于关系阶段目标和后续报告。

## 4. 第一批题库：恋爱经历

### Q009 恋爱经验

- 题型：`forced_single`
- 题目：你过去的恋爱经验更接近哪种？
- 选项：
  - A. 几乎没有正式恋爱经验。
  - B. 有过短期恋爱或暧昧。
  - C. 有过一段较认真关系。
  - D. 有过多段关系。
  - E. 有过分分合合或复杂关系。
- 影响维度：`family_relationship_script`、`risk_repeat_pattern`、`attachment_repair_receptivity`
- 备注：不判断好坏，只用于关系脚本。

### Q010 上一段关系结束原因

- 题型：`multi_with_primary`
- 题目：如果你有过上一段重要关系，它结束的主要原因是什么？可以多选，并标出最主要原因。
- 选项：
  - A. 沟通方式不合。
  - B. 异地、时间或现实压力。
  - C. 信任问题、隐瞒或背叛。
  - D. 家庭或未来规划不一致。
  - E. 新鲜感消失或感情变淡。
  - F. 控制欲、边界或自由问题。
  - G. 没有重要关系经验。
- 影响维度：`trust_old_wound_memory`、`stability_environmental_pressure`、`values_family_orientation`、`boundary_control_need`
- 备注：用于旧伤记忆和反复模式。

### Q011 分手后的联系模式

- 题型：`forced_single`
- 题目：分开后，你通常如何处理和前任的联系？
- 选项：
  - A. 基本断干净。
  - B. 偶尔礼貌联系。
  - C. 会保留联系方式，但不主动。
  - D. 情绪低落时容易联系。
  - E. 容易分分合合。
- 影响维度：`desire_alternative_seeking`、`attachment_repair_receptivity`、`risk_repeat_pattern`
- 备注：用于前任事件和复联机制。

### Q012 被伤害后的信任恢复

- 题型：`slider`
- 题目：如果对方曾经隐瞒过重要事情，之后你有多容易重新相信？
- 滑条：0 = 几乎很难再信；100 = 如果对方修复得好，可以重新相信。
- 影响维度：`trust_explanation_acceptance`、`trust_old_wound_memory`、`attachment_repair_receptivity`
- 备注：用于信任修复成本。

### Q013 最难接受的关系问题

- 题型：`ranked_multi`
- 题目：以下问题中，你最难接受哪些？请选择最多五项并排序。
- 选项：
  - A. 出轨或明确背叛。
  - B. 长期撒谎。
  - C. 和前任纠缠不清。
  - D. 冷暴力、失联、拉黑。
  - E. 强控制、查手机、限制社交。
  - F. 没有未来规划。
  - G. 公共场合羞辱。
  - H. 经济上不负责任。
- 影响维度：`moral_line_clarity`、`trust_loyalty_sensitivity`、`boundary_respect`、`communication_cruelty_under_conflict`
- 备注：用于底线和危机严重度。

### Q014 过去关系中的自己

- 题型：`multi_with_primary`
- 题目：回看过去的亲密关系，你觉得自己最常出现的问题是什么？可以多选，并标出最主要的一项。
- 选项：
  - A. 太敏感、太容易不安。
  - B. 不太会表达真实感受。
  - C. 容易冷处理或逃避。
  - D. 容易说重话。
  - E. 太迁就对方。
  - F. 太需要自由，不喜欢被束缚。
  - G. 容易隐瞒或说一半。
  - H. 暂时想不出来。
- 影响维度：`self_reflection_capacity`、`attachment_abandonment_anxiety`、`communication_conflict_avoidance`、`info_concealment_tendency`
- 备注：用于自我反省与自我美化对照。

### Q015 过去关系中的对方

- 题型：`multi_with_primary`
- 题目：你过去关系中，对方最让你难受的模式是什么？可以多选，并标出最主要的一项。
- 选项：
  - A. 忽冷忽热。
  - B. 不解释、不沟通。
  - C. 异性边界不清。
  - D. 控制欲强。
  - E. 说谎或隐瞒。
  - F. 不承担责任。
  - G. 情绪攻击或羞辱。
  - H. 没有明显模式。
- 影响维度：`trust_old_wound_memory`、`trust_suspicion_sensitivity`、`boundary_possessiveness`、`moral_harm_awareness`
- 备注：用于旧伤触发点。

### Q016 复合态度

- 题型：`primary_with_secondary`
- 题目：如果曾经很重要的人回来找你，你更可能怎么反应？
- 选项：
  - A. 直接拒绝，不想回头。
  - B. 会听解释，但不会马上相信。
  - C. 会心软，但会要求改变。
  - D. 很容易重新陷进去。
  - E. 看当时是否有新的关系或更好选择。
- 影响维度：`attachment_repair_receptivity`、`risk_repeat_pattern`、`desire_alternative_seeking`
- 备注：可记录次要冲动，例如“想拒绝但会心软”。

## 5. 第一批题库：依恋与亲密

### Q017 对方长时间不回消息

- 题型：`primary_with_secondary`
- 题目：你发了重要消息，对方几个小时没回，也没有提前说忙。你第一反应更接近哪种？
- 选项：
  - A. 先默认对方在忙。
  - B. 有点不舒服，但先忍住。
  - C. 想追问为什么不回。
  - D. 表面不问，但自己开始冷淡。
  - E. 想去看朋友圈、共同好友或其他线索。
- 影响维度：`attachment_abandonment_anxiety`、`trust_checking_impulse`、`emotion_reassurance_need`
- 备注：v0.1 题1的升级版，允许次要冲动和原因标签。

### Q018 关系变亲近后的反应

- 题型：`axis_2d`
- 题目：当关系变得越来越亲近时，你更接近哪个位置？
- 横轴：0 = 更安心；100 = 更担心失去。
- 纵轴：0 = 更愿意靠近；100 = 更想保持距离。
- 影响维度：`attachment_abandonment_anxiety`、`attachment_intimacy_avoidance`、`attachment_closeness_need`、`attachment_independence_need`
- 备注：依恋核心坐标。

### Q019 每天联系需求

- 题型：`slider`
- 题目：在一段稳定关系里，你对每天联系的需求有多强？
- 滑条：0 = 不需要每天联系；100 = 希望每天频繁联系。
- 影响维度：`attachment_closeness_need`、`digital_response_norm`、`social_dependency`
- 备注：用于联系频率和被冷落感。

### Q020 个人空间需求

- 题型：`slider`
- 题目：即使很喜欢对方，你对个人空间和独处时间的需求有多强？
- 滑条：0 = 几乎希望生活高度融合；100 = 很需要私人空间。
- 影响维度：`attachment_independence_need`、`values_freedom_need`、`boundary_autonomy_assertion`
- 备注：不要把高值直接视为冷漠。

### Q021 暴露脆弱

- 题型：`primary_with_secondary`
- 题目：当你很不安、很难过或很需要对方时，你更可能怎么做？
- 选项：
  - A. 直接告诉对方自己的感受。
  - B. 暗示一下，希望对方察觉。
  - C. 假装没事，不想显得脆弱。
  - D. 变冷淡，等对方主动来问。
  - E. 找别人倾诉，不告诉对方。
- 影响维度：`attachment_vulnerability_fear`、`communication_directness`、`emotion_reassurance_need`、`desire_emotional_validation_hunger`
- 备注：用于亲密暴露和第三方情绪价值。

### Q022 被需要感

- 题型：`slider`
- 题目：你有多希望自己在对方生活中是“很重要、不可替代”的人？
- 滑条：0 = 不太需要这种感觉；100 = 非常需要。
- 影响维度：`self_validation_need`、`attachment_closeness_need`、`values_belonging_need`
- 备注：用于被重视感、占有欲和关系满意度。

### Q023 依赖别人

- 题型：`forced_single`
- 题目：当你遇到现实困难时，你对向伴侣求助的态度更接近哪种？
- 选项：
  - A. 很自然，亲密关系本来可以互相依靠。
  - B. 会求助，但不想太麻烦对方。
  - C. 只有撑不住时才会说。
  - D. 不太喜欢求助，怕欠人情或被看低。
  - E. 表面说不需要，但心里希望对方主动发现。
- 影响维度：`attachment_reliance_comfort`、`attachment_vulnerability_fear`、`self_face_sensitivity`
- 备注：用于依赖舒适度、暴露脆弱恐惧和面子敏感。

### Q024 被别人依赖

- 题型：`forced_single`
- 题目：如果伴侣经常依赖你、需要你安慰和帮忙，你通常会怎么感受？
- 选项：
  - A. 会觉得被信任，愿意承担。
  - B. 可以接受，但希望有边界。
  - C. 一开始愿意，久了会累。
  - D. 压力很大，会想逃开。
  - E. 会觉得对方离不开我，关系更稳。
- 影响维度：`attachment_reliance_comfort`、`stability_resource_availability`、`boundary_dominance_need`
- 备注：E 可能关联支配感和被需要感。

### Q025 关系推进节奏

- 题型：`ranked_multi`
- 题目：关系变认真时，你认为哪些步骤最重要？请选择并排序。
- 选项：
  - A. 明确关系名分。
  - B. 稳定见面和联系。
  - C. 公开给朋友知道。
  - D. 了解彼此家庭和未来规划。
  - E. 经济和生活节奏能互相适应。
  - F. 保留彼此个人空间。
- 影响维度：`attachment_commitment_pace`、`values_family_orientation`、`digital_social_media_display`、`values_freedom_need`
- 备注：用于关系阶段推进。

### Q026 冲突后靠近

- 题型：`slider`
- 题目：吵架后，如果对方主动解释并修复，你有多容易重新靠近？
- 滑条：0 = 很难靠近；100 = 如果态度真诚，可以较快靠近。
- 影响维度：`attachment_repair_receptivity`、`trust_explanation_acceptance`、`emotion_recovery_speed`
- 备注：用于修复路线。

### Q027 亲密中的不安来源

- 题型：`multi_with_primary`
- 题目：关系越认真时，你最容易担心什么？可以多选，并标出最主要的一项。
- 选项：
  - A. 对方以后变心。
  - B. 自己失去自由。
  - C. 暴露真实缺点后不被喜欢。
  - D. 现实条件不合适。
  - E. 付出不对等。
  - F. 关系推进太快。
  - G. 对方不愿给明确承诺。
- 影响维度：`attachment_abandonment_anxiety`、`attachment_intimacy_avoidance`、`attachment_vulnerability_fear`、`values_security_need`
- 备注：可生成关系风险标签。

### Q028 安抚方式偏好

- 题型：`ranked_multi`
- 题目：当你关系里不安时，哪些方式最能安抚你？请选择最多三项并排序。
- 选项：
  - A. 对方明确解释发生了什么。
  - B. 对方主动表达在意和喜欢。
  - C. 对方用行动证明，例如来见你或补偿。
  - D. 对方给你一点空间，不逼你立刻好。
  - E. 对方公开你们的关系或边界。
  - F. 对方承诺下次具体怎么做。
- 影响维度：`emotion_reassurance_need`、`communication_repair_initiative`、`moral_compensation_willingness`、`digital_social_media_display`
- 备注：用于爱的语言和修复事件。

### Q029 亲密中的退缩

- 题型：`primary_with_secondary`
- 题目：如果对方突然对你非常认真、频繁表达未来规划，你更可能怎么反应？
- 选项：
  - A. 感到安心，也愿意回应。
  - B. 开心，但需要慢慢适应。
  - C. 有压力，会想放慢一点。
  - D. 会怀疑对方是不是太快了。
  - E. 会想后退，避免被绑定。
- 影响维度：`attachment_commitment_pace`、`attachment_intimacy_avoidance`、`values_freedom_need`
- 备注：用于承诺节奏。

### Q030 依恋自我描述

- 题型：`multi_with_primary`
- 题目：以下描述中，哪些比较像你在亲密关系里的状态？可以多选，并标出最像的一项。
- 选项：
  - A. 我需要稳定回应，不然容易不安。
  - B. 我喜欢亲密，但也怕自己太依赖。
  - C. 我需要很多个人空间。
  - D. 我不太会表达需要，容易装没事。
  - E. 我吵架后需要对方主动修复。
  - F. 我通常比较稳定，不太会被小事影响。
  - G. 我会在亲密和退缩之间摇摆。
- 影响维度：`attachment_abandonment_anxiety`、`attachment_intimacy_avoidance`、`attachment_closeness_need`、`attachment_independence_need`、`self_discrepancy_awareness`
- 备注：作为自评题，后续需要用情境题验证。

## 6. 第一批覆盖说明

第一批主要覆盖：

- 基础关系入口；
- 现实距离和生活压力；
- 过去关系脚本；
- 前任和复联倾向；
- 被弃焦虑；
- 回避亲密；
- 亲密需求；
- 独立需求；
- 暴露脆弱恐惧；
- 依赖舒适度；
- 承诺节奏；
- 修复接受度。

第一批尚未覆盖或覆盖不足的模块，已经在后续文件中补齐：

- 信任怀疑、占有欲与边界、诚实/隐瞒、双标检测：见 `18_super_realistic_question_bank_part2.md`；
- 冲突沟通、欲望忠诚、道德责任：见 `18_super_realistic_question_bank_part3.md`；
- 社交网络、现实压力、数字生活、家庭成长、综合反向验证：见 `18_super_realistic_question_bank_part4.md`。

## 7. 后续建议

超级真实版题库第一版已经在 Q001-Q150 范围内完成。后续不建议继续盲目加题，而应优先：

```text
docs/design/19_relationship_report_templates.md
docs/design/22_questionnaire_scoring_rules.md
docs/design/23_questionnaire_dimension_coverage.md
docs/design/24_questionnaire_json_schema.md
```

其中 19 和 22 已完成，下一步应优先做 23 维度覆盖率检查，再决定是否需要补充 Q151-Q180。

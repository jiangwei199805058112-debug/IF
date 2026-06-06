# 超级真实版题库 第三批 v0.1

本文档是 `docs/design/18_super_realistic_question_bank.md` 的续写文件，用于整理超级真实版题库第三批。

第三批覆盖：

- 冲突与沟通；
- 欲望、新鲜感与忠诚；
- 道德、责任与后果意识；
- 冲突升级、冷处理、修复尝试、诱惑抵抗、暧昧边界、承诺可信度和暴露后负责度。

本文档只做题库设计，不修改控制台原型运行逻辑。

## 1. 第三批题库：冲突与沟通

### Q071 吵架当下表达

- 题型：`primary_with_secondary`
- 题目：当你明显不满时，你最可能怎么表达？
- 选项：
  - A. 直接说清楚自己哪里不舒服。
  - B. 先忍住，等情绪稳定再说。
  - C. 用暗示、语气或冷淡让对方察觉。
  - D. 情绪上来会直接质问。
  - E. 不想说，觉得说了也没用。
- 影响维度：`communication_directness`、`communication_conflict_avoidance`、`emotion_suppression_tendency`
- 备注：用于冲突入口和未解决冲突累积。

### Q072 被指出问题时的第一反应

- 题型：`primary_with_secondary`
- 题目：当对方指出你做错了一件事，你第一反应更接近哪种？
- 选项：
  - A. 先听完对方感受。
  - B. 会解释自己的原因。
  - C. 会指出对方也有问题。
  - D. 会觉得被攻击，开始防御。
  - E. 会沉默或退出对话。
- 影响维度：`communication_defensiveness`、`self_reflection_capacity`、`communication_listening_capacity`
- 备注：用于防御性和反击倾向。

### Q073 冷处理倾向

- 题型：`slider`
- 题目：吵架后你有多可能长时间不回复、冷处理或故意不解释？
- 滑条：0 = 基本不会；100 = 很容易。
- 影响维度：`emotion_shutdown_tendency`、`communication_conflict_avoidance`、`risk_avoidant_disappearance`
- 备注：用于冷战、失联和分手危机。

### Q074 拉黑/删除冲动

- 题型：`slider`
- 题目：情绪很激烈时，你有多可能拉黑、删除、取消关注或说出分手？
- 滑条：0 = 基本不会；100 = 很可能。
- 影响维度：`emotion_impulsivity`、`risk_sabotage_tendency`、`risk_breakdown_tendency`
- 备注：用于情绪性分手和自毁/破坏倾向。

### Q075 公共场合冲突

- 题型：`primary_with_secondary`
- 题目：如果对方在朋友面前说了让你尴尬的话，你更可能怎么做？
- 选项：
  - A. 当场轻轻提醒，避免升级。
  - B. 忍住，回去私下说。
  - C. 当场反击，不想吃亏。
  - D. 直接离开现场。
  - E. 表面没事，但之后会记很久。
- 影响维度：`self_face_sensitivity`、`communication_cruelty_under_conflict`、`trust_old_wound_memory`
- 备注：v0.1 题6升级版。

### Q076 说重话倾向

- 题型：`slider`
- 题目：吵架时，你有多可能说出“你一直都这样”“你根本不在乎我”“那就分手”这类重话？
- 滑条：0 = 基本不会；100 = 很容易说出口。
- 影响维度：`communication_cruelty_under_conflict`、`emotion_anger_control`、`risk_sabotage_tendency`
- 备注：用于关系伤口和长期记忆。

### Q077 道歉能力

- 题型：`forced_single`
- 题目：如果你意识到自己确实伤害了对方，你更可能怎么道歉？
- 选项：
  - A. 承认具体行为，也承认对对方造成的影响。
  - B. 会道歉，但主要解释自己不是故意的。
  - C. 会说“对不起”，但不想继续讨论。
  - D. 会等对方先缓和再说。
  - E. 很难道歉，除非对方也承认问题。
- 影响维度：`communication_apology_capacity`、`moral_harm_awareness`、`moral_accountability_under_exposure`
- 备注：用于修复质量。

### Q078 修复主动性

- 题型：`slider`
- 题目：冲突后，如果你还在乎对方，你有多可能主动发起修复？
- 滑条：0 = 基本等对方先来；100 = 会主动修复。
- 影响维度：`communication_repair_initiative`、`moral_compensation_willingness`、`attachment_repair_receptivity`
- 备注：用于和解机会。

### Q079 关系复盘能力

- 题型：`forced_single`
- 题目：冲突过去后，你更倾向于怎样处理“为什么我们会这样吵”？
- 选项：
  - A. 会认真复盘模式和下次做法。
  - B. 会简单说一下，但不想太深入。
  - C. 只想翻篇，不想再提。
  - D. 觉得主要是对方的问题。
  - E. 害怕复盘又吵起来，所以回避。
- 影响维度：`communication_meta_discussion`、`self_reflection_capacity`、`communication_conflict_avoidance`
- 备注：用于长期改善能力。

### Q080 倾听能力

- 题型：`reverse_check`
- 题目：当对方表达委屈时，你最常见的反应是什么？
- 选项：
  - A. 先确认对方为什么委屈。
  - B. 会听，但也想解释自己。
  - C. 会觉得对方太敏感。
  - D. 会马上指出对方也有问题。
  - E. 会沉默，不知道怎么接。
- 影响维度：`communication_listening_capacity`、`moral_harm_awareness`、`communication_defensiveness`
- 备注：与自评成熟沟通类题目对照。

### Q081 情绪恢复速度

- 题型：`slider`
- 题目：一次明显争吵后，你通常需要多久才能恢复到愿意正常沟通？
- 滑条：0 = 很快恢复；100 = 会持续很久。
- 影响维度：`emotion_recovery_speed`、`trust_old_wound_memory`、`emotion_reassurance_need`
- 备注：数值越高表示恢复越慢。

### Q082 冲突中最需要什么

- 题型：`ranked_multi`
- 题目：冲突发生时，哪些事最能让你降温？请选择最多三项并排序。
- 选项：
  - A. 对方承认你的感受。
  - B. 对方解释清楚事实。
  - C. 对方道歉。
  - D. 对方给你一点时间和空间。
  - E. 对方提出具体补救方法。
  - F. 对方不要再反驳。
- 影响维度：`emotion_reassurance_need`、`trust_explanation_acceptance`、`moral_compensation_willingness`
- 备注：用于修复路径。

### Q083 自评成熟沟通

- 题型：`slider`
- 题目：你认为自己在亲密关系里有多会沟通？
- 滑条：0 = 经常沟通失败；100 = 很会表达和修复。
- 影响维度：`communication_directness`、`communication_meta_discussion`、`self_discrepancy_awareness`
- 备注：需要与 Q071-Q082 情境题对照。

## 2. 第三批题库：欲望、新鲜感与忠诚

### Q084 新鲜感需求

- 题型：`slider`
- 题目：一段关系稳定后，你对新鲜感、刺激感、被重新吸引的需求有多强？
- 滑条：0 = 稳定本身就很好；100 = 很需要持续新鲜感。
- 影响维度：`desire_novelty_need`、`temperament_sensation_seeking`
- 备注：高值不直接等于不忠，只表示新鲜感需求强。

### Q085 稳定偏好

- 题型：`slider`
- 题目：你有多重视一段关系的稳定、可预期和长期安全？
- 滑条：0 = 不太喜欢固定模式；100 = 非常重视稳定。
- 影响维度：`desire_stability_preference`、`values_security_need`、`moral_commitment_credibility`
- 备注：与 Q084 形成张力，不是简单反向。

### Q086 面对主动示好

- 题型：`primary_with_secondary`
- 题目：如果有一个你不讨厌的人明显对你有好感，而你已经有暧昧对象或恋人，你更可能怎么处理？
- 选项：
  - A. 明确保持距离。
  - B. 礼貌回应，但不深入。
  - C. 会享受被喜欢，但不主动推进。
  - D. 如果现有关系不顺，会忍不住多聊。
  - E. 会隐瞒这段互动。
- 影响维度：`desire_temptation_resistance`、`desire_emotional_validation_hunger`、`info_concealment_tendency`
- 备注：用于诱惑抵抗和情绪价值饥渴。

### Q087 精神暧昧边界

- 题型：`forced_single`
- 题目：你怎么看“没有身体越界，但和别人长期分享情绪、秘密和依赖”的关系？
- 选项：
  - A. 这已经是明显越界。
  - B. 要看内容和频率。
  - C. 如果只是朋友，可以接受。
  - D. 只要没有实际出轨，就不算严重。
  - E. 我自己可能会这样，但不希望对方这样。
- 影响维度：`digital_online_flirt_boundary`、`desire_emotional_validation_hunger`、`boundary_double_standard`
- 备注：E 用于双标检测。

### Q088 情绪价值缺口

- 题型：`slider`
- 题目：当伴侣长期不能理解或安慰你时，你有多容易被另一个懂你的人吸引？
- 滑条：0 = 不太会；100 = 很容易。
- 影响维度：`desire_emotional_validation_hunger`、`desire_alternative_seeking`、`desire_temptation_resistance`
- 备注：用于精神暧昧机会窗口。

### Q089 关系不满时寻找替代

- 题型：`primary_with_secondary`
- 题目：当你对现有关系不满，但还没分开时，你更可能怎么处理？
- 选项：
  - A. 先处理现有关系，不找别人。
  - B. 会和朋友倾诉，但保持边界。
  - C. 会想认识新人转移注意力。
  - D. 会和某个有好感的人多聊。
  - E. 会先给自己留一个退路。
- 影响维度：`desire_alternative_seeking`、`moral_line_clarity`、`moral_consequence_forecast`
- 备注：用于替代倾向。

### Q090 即时满足 vs 长期后果

- 题型：`axis_2d`
- 题目：面对一件当下很想做、但可能影响关系的事，你更接近哪个位置？
- 横轴：0 = 更看重长期后果；100 = 更看重当下感受。
- 纵轴：0 = 会主动设边界；100 = 需要事情发生后再处理。
- 影响维度：`desire_instant_gratification`、`moral_consequence_forecast`、`desire_temptation_resistance`
- 备注：用于机会窗口行为概率。

### Q091 忠诚自我认同

- 题型：`slider`
- 题目：你有多把“忠诚”看作自己的人格原则，而不是只看有没有机会？
- 滑条：0 = 主要看关系状态和环境；100 = 是很核心的自我原则。
- 影响维度：`desire_loyalty_identity`、`moral_line_clarity`
- 备注：用于诱惑抵抗的稳定系数。

### Q092 外貌/身体吸引权重

- 题型：`weighted_multi`
- 题目：一个人吸引你时，以下因素大概各占多少？请分配100点。
- 选项：
  - A. 外貌和身材。
  - B. 情绪理解和聊天感觉。
  - C. 稳定可靠。
  - D. 新鲜刺激和神秘感。
  - E. 现实条件和未来可能。
- 影响维度：`desire_physical_attraction_weight`、`desire_emotional_validation_hunger`、`desire_novelty_need`、`values_status_comparison`
- 备注：用于吸引力和替代对象类型。

### Q093 暧昧边界自评

- 题型：`multi_with_primary`
- 题目：你觉得哪些行为已经算暧昧越界？可以多选，并标出最重要的一项。
- 选项：
  - A. 每天频繁聊天。
  - B. 深夜倾诉。
  - C. 开带有暧昧意味的玩笑。
  - D. 隐瞒对方存在。
  - E. 单独见面。
  - F. 对别人说自己像单身。
  - G. 删除聊天记录。
- 影响维度：`digital_online_flirt_boundary`、`moral_line_clarity`、`trust_loyalty_sensitivity`
- 备注：用于暧昧边界。

### Q094 自己暧昧 vs 对方暧昧

- 题型：`npc_perspective`
- 题目：如果同样的暧昧边界发生在你身上和对方身上，你判断严重程度是否一致？
- 选项：
  - A. 基本一致，规则应该一样。
  - B. 我会尽量一致，但情绪上可能更介意对方。
  - C. 我知道自己没想越界，但很难相信对方也一样。
  - D. 我需要更多自由，但对方最好更清楚边界。
  - E. 我自己可以解释，但对方这样做我很难接受。
- 影响维度：`boundary_double_standard`、`trust_projection_tendency`、`desire_loyalty_identity`
- 备注：核心双标配对题。

### Q095 长期稳定后的厌倦

- 题型：`slider`
- 题目：关系长期稳定后，如果生活变得重复，你有多容易觉得无聊或想逃开？
- 滑条：0 = 稳定让我安心；100 = 重复会让我很想逃开。
- 影响维度：`desire_novelty_need`、`attachment_intimacy_avoidance`、`temperament_sensation_seeking`
- 备注：用于长期阶段风险。

### Q096 诱惑中的主动刹车

- 题型：`forced_single`
- 题目：当你意识到自己和某个人的聊天开始变暧昧时，你更可能怎么做？
- 选项：
  - A. 主动减少联系并设边界。
  - B. 保持礼貌，但不再深入。
  - C. 先观察自己是不是真的心动。
  - D. 继续聊，但提醒自己不要过界。
  - E. 隐藏这段聊天，避免麻烦。
- 影响维度：`desire_temptation_resistance`、`moral_consequence_forecast`、`info_secret_management`
- 备注：用于诱惑抵抗实际策略。

## 3. 第三批题库：道德、责任与后果意识

### Q097 责任承担

- 题型：`slider`
- 题目：当你的选择造成关系伤害时，你有多愿意承担后果，而不是只希望事情快点过去？
- 滑条：0 = 更想快点翻篇；100 = 愿意承担并修复。
- 影响维度：`moral_responsibility`、`moral_compensation_willingness`
- 备注：用于修复成本和结局标签。

### Q098 底线清晰度

- 题型：`ranked_multi`
- 题目：你认为一段关系中最不能被模糊处理的底线有哪些？请选择最多五项并排序。
- 选项：
  - A. 明确出轨。
  - B. 长期隐瞒。
  - C. 精神暧昧。
  - D. 经济欺骗。
  - E. 侵犯隐私。
  - F. 情绪羞辱。
  - G. 对未来承诺反复失信。
- 影响维度：`moral_line_clarity`、`trust_loyalty_sensitivity`、`boundary_respect`
- 备注：用于底线协议。

### Q099 后果预判

- 题型：`primary_with_secondary`
- 题目：在做一件可能让对方失望的事之前，你通常会不会提前想后果？
- 选项：
  - A. 会认真预判后果，所以尽量不做。
  - B. 会想，但有时还是会做。
  - C. 只要当下觉得没问题，就不会想太多。
  - D. 觉得就算出事也可以解释。
  - E. 通常事情发生后才处理。
- 影响维度：`moral_consequence_forecast`、`desire_instant_gratification`、`self_justification_tendency`
- 备注：用于风险行为概率。

### Q100 道德弹性

- 题型：`forced_single`
- 题目：你怎么看“关系状态不好时，有些边界可以暂时放松”？
- 选项：
  - A. 不认同，关系不好也不能越界。
  - B. 情绪可以理解，但行为仍要有底线。
  - C. 要看具体情况。
  - D. 如果对方长期忽视我，我也有理由找出口。
  - E. 我可以理解自己这样，但很难接受对方这样。
- 影响维度：`moral_flexibility`、`self_justification_tendency`、`boundary_double_standard`
- 备注：用于自我合理化和双标。

### Q101 承诺可信度

- 题型：`slider`
- 题目：你说“我会改”“下次不会这样”之后，实际做到的概率有多高？
- 滑条：0 = 经常做不到；100 = 基本会做到。
- 影响维度：`moral_commitment_credibility`、`temperament_conscientiousness`
- 备注：自评题，后续应由行为验证。

### Q102 补偿意愿

- 题型：`ranked_multi`
- 题目：如果你伤害了对方，你愿意用哪些方式补偿或修复？请选择最多三项并排序。
- 选项：
  - A. 完整解释事实。
  - B. 真诚道歉并承认影响。
  - C. 改变之后的行为规则。
  - D. 用行动陪伴和补偿。
  - E. 给对方时间消化。
  - F. 接受对方短期不信任。
- 影响维度：`moral_compensation_willingness`、`communication_apology_capacity`、`communication_repair_initiative`
- 备注：用于修复路径。

### Q103 暴露后负责度

- 题型：`primary_with_secondary`
- 题目：如果你做错的事已经被发现，证据也比较明显，你更可能怎么处理？
- 选项：
  - A. 承认事实并承担影响。
  - B. 承认一部分，再慢慢解释。
  - C. 强调自己不是故意的。
  - D. 质疑对方为什么要查你。
  - E. 继续否认或转移重点。
- 影响维度：`moral_accountability_under_exposure`、`info_exposure_reaction`、`risk_escalation_under_exposure`
- 备注：用于危机线。

### Q104 伤害觉察

- 题型：`reverse_check`
- 题目：如果你觉得一件事“不严重”，但对方很受伤，你更可能怎么理解？
- 选项：
  - A. 对方受伤就说明这件事需要认真处理。
  - B. 我会理解，但也希望对方理解我的角度。
  - C. 可能是对方太敏感。
  - D. 如果我本意不是伤害，就不该被追责太多。
  - E. 我会先安抚，但心里觉得对方小题大做。
- 影响维度：`moral_harm_awareness`、`communication_listening_capacity`、`self_justification_tendency`
- 备注：用于道歉质量和共情。

### Q105 经济责任

- 题型：`forced_single`
- 题目：关系中的花费、借钱、礼物和共同开销，你更接近哪种态度？
- 选项：
  - A. 账目和能力要清楚，不能让关系变成压力。
  - B. 可以互相付出，但要大致平衡。
  - C. 重要时候愿意多花钱表达重视。
  - D. 不喜欢算太清，感情更重要。
  - E. 如果对方在意我，就应该愿意承担更多。
- 影响维度：`values_material_importance`、`stability_money_management`、`moral_responsibility`
- 备注：用于现实压力和经济责任。

### Q106 破罐破摔

- 题型：`slider`
- 题目：当你觉得关系已经很糟、自己也解释不清时，你有多可能“算了，随便吧，坏就坏到底”？
- 滑条：0 = 基本不会；100 = 很可能破罐破摔。
- 影响维度：`risk_escalation_under_exposure`、`risk_sabotage_tendency`、`risk_breakdown_tendency`
- 备注：用于危机升级。

### Q107 报复冲动

- 题型：`slider`
- 题目：如果你觉得对方伤害了你，你有多想让对方也体验同样的不安或痛苦？
- 滑条：0 = 不想报复；100 = 很想让对方也难受。
- 影响维度：`risk_revenge_tendency`、`communication_cruelty_under_conflict`、`desire_alternative_seeking`
- 备注：用于报复性暧昧、冷淡、旧账。

### Q108 自我合理化

- 题型：`multi_with_primary`
- 题目：当你做了一件可能有问题的事，你最容易用哪些理由说服自己？可以多选，并标出最主要的一项。
- 选项：
  - A. 我不是故意的。
  - B. 对方也做过类似的事。
  - C. 这件事本身没那么严重。
  - D. 如果我说实话只会更糟。
  - E. 我压力太大了。
  - F. 对方太敏感或太控制。
  - G. 我不会这样想，会直接承担。
- 影响维度：`self_justification_tendency`、`moral_flexibility`、`moral_accountability_under_exposure`
- 备注：用于报告中的自我合理化标签。

### Q109 关系成本意识

- 题型：`axis_2d`
- 题目：当你做选择时，会怎么衡量“自己舒服”和“关系代价”？
- 横轴：0 = 更看重关系代价；100 = 更看重自己当下舒服。
- 纵轴：0 = 事前会预判；100 = 事后再补救。
- 影响维度：`moral_consequence_forecast`、`desire_instant_gratification`、`moral_responsibility`
- 备注：用于机会窗口和行为预测。

### Q110 第三批总结题

- 题型：`multi_with_primary`
- 题目：在冲突、诱惑和责任这三类问题中，你最容易出现哪些风险？可以多选，并标出最主要的一项。
- 选项：
  - A. 情绪上来后说重话或冲动决定。
  - B. 不想沟通，容易冷处理或逃避。
  - C. 被理解和安慰时容易心动。
  - D. 关系不顺时容易寻找替代感。
  - E. 做错后容易先解释或合理化。
  - F. 承诺改变后执行不稳定。
  - G. 暂时没有明显风险。
- 影响维度：`communication_cruelty_under_conflict`、`risk_avoidant_disappearance`、`desire_emotional_validation_hunger`、`desire_alternative_seeking`、`self_justification_tendency`、`moral_commitment_credibility`
- 备注：用于第三批模块报告摘要。

## 4. 第三批覆盖说明

第三批主要覆盖：

- 直接沟通；
- 冲突回避；
- 防御性；
- 道歉能力；
- 修复主动性；
- 关系复盘能力；
- 倾听能力；
- 冲突伤人倾向；
- 情绪冲动；
- 冷处理和失联；
- 新鲜感需求；
- 稳定偏好；
- 诱惑抵抗；
- 即时满足；
- 替代倾向；
- 情绪价值饥渴；
- 外貌/身体吸引权重；
- 忠诚自我认同；
- 责任承担；
- 底线清晰度；
- 后果预判；
- 道德弹性；
- 承诺可信度；
- 补偿意愿；
- 暴露后负责度；
- 伤害觉察；
- 自我合理化；
- 破罐破摔和报复冲动。

## 5. 下一批建议

下一批建议继续写：

```text
社交网络 + 现实压力 + 数字生活剩余题 + 综合反向验证
```

目标约 40 题，重点包括：

- 朋友和共同圈子；
- 家庭影响和现实距离；
- 金钱、时间、作息、工作学习压力；
- 社交媒体展示；
- 在线可得压力；
- 两部手机/两个账号的更细场景；
- 朋友圈、点赞、照片、流言传播；
- 自述人格与行为人格的综合矛盾检测；
- 超级真实版最终总结题。

# 超级真实版题库 第四批 v0.1

本文档是 `docs/design/18_super_realistic_question_bank.md` 的续写文件，用于整理超级真实版题库第四批。

第四批覆盖：

- 社交网络；
- 现实压力；
- 数字生活剩余题；
- 家庭、成长与关系脚本补充；
- 综合反向验证；
- 超级真实版最终总结题。

本文档只做题库设计，不修改控制台原型运行逻辑。

## 1. 第四批题库：社交网络

### Q111 朋友对关系的影响

- 题型：`slider`
- 题目：朋友对你判断一段关系的影响有多大？
- 滑条：0 = 几乎不影响；100 = 很影响，朋友意见会明显改变你的判断。
- 影响维度：`social_reputation_sensitivity`、`social_circle_overlap_need`、`family_approval_need`
- 备注：用于朋友介入、共同圈子和流言传播。

### Q112 共同好友圈

- 题型：`forced_single`
- 题目：你更希望恋人和你的朋友处于什么关系？
- 选项：
  - A. 互相认识并能自然相处。
  - B. 重要朋友知道就可以。
  - C. 可以认识，但不需要深度融入。
  - D. 最好保持圈子分开。
  - E. 我希望进入对方圈子，但不太希望对方进入我的圈子。
- 影响维度：`social_circle_overlap_need`、`digital_social_media_display`、`boundary_double_standard`
- 备注：E 可用于双标和圈子控制检测。

### Q113 朋友提醒你对方有问题

- 题型：`primary_with_secondary`
- 题目：如果朋友提醒你“这个人可能不太靠谱”，你更可能怎么处理？
- 选项：
  - A. 认真听，但自己再观察。
  - B. 会开始明显怀疑对方。
  - C. 会为对方解释，不太愿意听。
  - D. 会直接去问对方。
  - E. 会私下查更多信息。
- 影响维度：`trust_suspicion_sensitivity`、`social_reputation_sensitivity`、`trust_checking_impulse`
- 备注：用于外部信息影响和查证路径。

### Q114 共同朋友发现异常

- 题型：`scenario_choice`
- 题目：共同朋友告诉你，对方最近和某个人走得很近，但不确定是不是暧昧。你更可能怎么做？
- 选项：
  - A. 先不下结论，等更多信息。
  - B. 问朋友具体细节。
  - C. 直接问对方。
  - D. 观察对方手机和动态。
  - E. 情绪上先冷下来。
- 影响维度：`trust_suspicion_sensitivity`、`trust_checking_impulse`、`emotion_shutdown_tendency`
- 备注：用于共同好友证据链。

### Q115 流言传播压力

- 题型：`slider`
- 题目：如果你们的关系问题被朋友、同学或同事知道，你会有多在意？
- 滑条：0 = 不太在意；100 = 非常在意，会觉得很丢脸或压力很大。
- 影响维度：`self_face_sensitivity`、`social_reputation_sensitivity`、`self_image_management`
- 备注：用于公开冲突和名声压力。

### Q116 朋友与恋人冲突

- 题型：`primary_with_secondary`
- 题目：如果你的朋友和恋人互相不喜欢，你更可能怎么处理？
- 选项：
  - A. 分开处理，尽量不让他们互相影响。
  - B. 会试着协调双方关系。
  - C. 更相信朋友的判断。
  - D. 更站在恋人这边。
  - E. 会觉得很烦，想回避这个问题。
- 影响维度：`social_circle_overlap_need`、`communication_meta_discussion`、`communication_conflict_avoidance`
- 备注：用于社交圈矛盾。

### Q117 社交开放度

- 题型：`axis_2d`
- 题目：恋爱后，你对自己和对方的社交开放度更接近哪里？
- 横轴：0 = 恋爱后社交边界应更收紧；100 = 恋爱后仍应保持原本社交自由。
- 纵轴：0 = 自己和对方规则一致；100 = 希望对方比自己更收紧。
- 影响维度：`social_initiative`、`boundary_double_standard`、`trust_loyalty_sensitivity`
- 备注：社交自由与双标坐标。

### Q118 社交场合被忽略

- 题型：`primary_with_secondary`
- 题目：如果你们一起参加聚会，对方和别人聊得很开心，忽略了你，你更可能怎么反应？
- 选项：
  - A. 不太介意，社交场合正常。
  - B. 有点不舒服，但不会当场表现。
  - C. 会主动加入他们的聊天。
  - D. 会事后表达自己被忽略。
  - E. 会冷下来，让对方自己发现。
- 影响维度：`attachment_abandonment_anxiety`、`social_dependency`、`communication_directness`
- 备注：用于社交场合安全感。

### Q119 朋友圈展示比较

- 题型：`slider`
- 题目：看到别人被伴侣公开、送礼物、发合照时，你会有多容易拿来比较自己的关系？
- 滑条：0 = 基本不会比较；100 = 很容易比较并影响心情。
- 影响维度：`values_status_comparison`、`digital_social_media_display`、`self_validation_need`
- 备注：用于社交媒体展示和被重视感。

### Q120 社交网络总结题

- 题型：`multi_with_primary`
- 题目：在朋友、共同圈子和公开展示中，你最容易在意哪些问题？可以多选，并标出最主要的一项。
- 选项：
  - A. 朋友不看好这段关系。
  - B. 对方不愿公开你。
  - C. 对方在社交场合忽略你。
  - D. 共同朋友带来流言或证据。
  - E. 对方朋友中有暧昧对象或前任。
  - F. 自己不想让圈子过度介入。
  - G. 暂时没有明显问题。
- 影响维度：`social_reputation_sensitivity`、`digital_social_media_display`、`trust_loyalty_sensitivity`、`social_circle_overlap_need`
- 备注：用于社交网络模块报告摘要。

## 2. 第四批题库：现实压力

### Q121 时间投入能力

- 题型：`slider`
- 题目：在学习、工作、兼职或生活压力下，你还能稳定投入关系的能力有多强？
- 滑条：0 = 压力大时几乎顾不上关系；100 = 压力大也会稳定投入。
- 影响维度：`stability_resource_availability`、`stability_time_management`、`emotion_stress_tolerance`
- 备注：用于现实压力下回复、约会和修复能力。

### Q122 时间管理失误

- 题型：`primary_with_secondary`
- 题目：如果你因为忙而忘记回复、忘记约定或迟到，你更可能怎么处理？
- 选项：
  - A. 主动解释并补救。
  - B. 解释自己太忙，希望对方理解。
  - C. 等对方提醒后再道歉。
  - D. 觉得对方不该因为这种事计较。
  - E. 会逃避解释，怕越说越麻烦。
- 影响维度：`stability_time_management`、`moral_responsibility`、`communication_conflict_avoidance`
- 备注：用于行动信任。

### Q123 金钱压力

- 题型：`axis_2d`
- 题目：当关系中出现消费、礼物、约会开销时，你更接近哪个位置？
- 横轴：0 = 消费应量力而行；100 = 消费和仪式感能明显代表重视。
- 纵轴：0 = 愿意提前沟通预算；100 = 不太想谈钱，怕尴尬或伤感情。
- 影响维度：`values_material_importance`、`stability_money_management`、`communication_directness`
- 备注：用于经济矛盾和仪式感落差。

### Q124 经济不稳定时的关系选择

- 题型：`forced_single`
- 题目：如果你经济压力很大，但对方希望更多约会、礼物或仪式感，你更可能怎么做？
- 选项：
  - A. 直接说明现实情况，一起调整期待。
  - B. 尽量满足，但内心有压力。
  - C. 减少见面或回避相关话题。
  - D. 觉得对方不够体谅。
  - E. 会硬撑，怕被看低。
- 影响维度：`stability_money_management`、`self_face_sensitivity`、`communication_conflict_avoidance`
- 备注：用于现实经济压力。

### Q125 作息不一致

- 题型：`primary_with_secondary`
- 题目：如果你们作息很不一样，一个人白天忙、一个人晚上活跃，你更可能怎么处理？
- 选项：
  - A. 约定固定联系时间。
  - B. 互相理解，不强求实时回复。
  - C. 会有点失落，但尽量忍。
  - D. 会觉得对方没把你放在优先级。
  - E. 容易用冷淡回应冷淡。
- 影响维度：`stability_sleep_rhythm`、`digital_response_norm`、`attachment_abandonment_anxiety`
- 备注：用于消息节奏和误会。

### Q126 家庭压力介入

- 题型：`multi_with_primary`
- 题目：家庭最可能从哪些方面影响你的亲密关系？可以多选，并标出最主要的一项。
- 选项：
  - A. 家人是否认可对方。
  - B. 经济压力或家庭责任。
  - C. 地区、文化、学历或收入期待。
  - D. 婚恋节奏和结婚压力。
  - E. 家人过度干预隐私。
  - F. 我基本不会受家庭影响。
- 影响维度：`family_parental_influence`、`family_obligation_pressure`、`family_approval_need`、`values_status_comparison`
- 备注：用于家庭事件和未来规划。

### Q127 家庭边界

- 题型：`forced_single`
- 题目：如果家人对你的恋人有意见，你更可能怎么处理？
- 选项：
  - A. 自己判断，不让家人直接干涉关系。
  - B. 会听家人意见，但保留自己的决定。
  - C. 会要求恋人做出改变让家人接受。
  - D. 会对关系产生动摇。
  - E. 会两边都瞒一点，避免冲突。
- 影响维度：`family_privacy_boundary`、`family_approval_need`、`info_concealment_tendency`
- 备注：用于家庭边界和双线压力。

### Q128 工作/学业高压期

- 题型：`primary_with_secondary`
- 题目：在考试、项目、工作爆忙期，你对恋人的需求更接近哪种？
- 选项：
  - A. 希望对方理解我少联系。
  - B. 希望对方支持我，但不要给压力。
  - C. 希望对方主动照顾我情绪。
  - D. 压力越大越需要陪伴。
  - E. 压力大时我会把关系先放一边。
- 影响维度：`emotion_stress_tolerance`、`attachment_closeness_need`、`stability_resource_availability`
- 备注：用于压力期联系频率。

### Q129 现实条件不匹配

- 题型：`ranked_multi`
- 题目：以下现实条件中，哪些最可能影响你是否继续一段关系？请选择最多五项并排序。
- 选项：
  - A. 异地距离。
  - B. 收入和消费观差异。
  - C. 学历、职业或发展方向差异。
  - D. 家庭反对。
  - E. 结婚或未来规划不同。
  - F. 作息和生活习惯不合。
  - G. 朋友或圈子不合。
  - H. 年龄阶段不同。
- 影响维度：`values_status_comparison`、`values_family_orientation`、`stability_environmental_pressure`、`stability_adaptability`
- 备注：用于现实阻力和长期结局。

### Q130 现实压力总结题

- 题型：`multi_with_primary`
- 题目：现实生活中，最容易让你关系变差的压力有哪些？可以多选，并标出最主要的一项。
- 选项：
  - A. 时间不够。
  - B. 钱不够或消费观不合。
  - C. 作息不一致。
  - D. 家庭干预。
  - E. 异地或见面成本。
  - F. 工作/学习压力。
  - G. 生活自理和情绪状态不稳定。
- 影响维度：`stability_environmental_pressure`、`stability_resource_availability`、`family_obligation_pressure`
- 备注：用于现实压力模块报告摘要。

## 3. 第四批题库：数字生活剩余题

### Q131 在线可得压力

- 题型：`slider`
- 题目：如果你看到对方在线、发了动态或点赞了别人，却没有回你，你会有多不舒服？
- 滑条：0 = 基本不在意；100 = 非常不舒服。
- 影响维度：`digital_availability_pressure`、`digital_response_norm`、`attachment_abandonment_anxiety`
- 备注：用于在线未回复事件。

### Q132 点赞和评论边界

- 题型：`forced_single`
- 题目：你怎么看恋人频繁给某个异性点赞、评论或互动？
- 选项：
  - A. 普通互动，不必过度解读。
  - B. 要看互动内容和频率。
  - C. 如果固定是同一个人，会在意。
  - D. 会认为这是暧昧信号。
  - E. 我自己可以这样互动，但不希望对方这样。
- 影响维度：`digital_online_flirt_boundary`、`trust_suspicion_sensitivity`、`boundary_double_standard`
- 备注：E 用于双标检测。

### Q133 朋友圈可见性

- 题型：`primary_with_secondary`
- 题目：如果你发现对方有些朋友圈、动态或照片没有对你可见，你更可能怎么想？
- 选项：
  - A. 可能只是分组习惯，不多想。
  - B. 会好奇，但先不问。
  - C. 会问为什么不让你看。
  - D. 会开始怀疑对方有隐瞒。
  - E. 会用自己的分组或隐藏回应。
- 影响维度：`digital_evidence_awareness`、`trust_suspicion_sensitivity`、`risk_revenge_tendency`
- 备注：用于社交媒体隐瞒。

### Q134 两个账号/两部手机细化

- 题型：`primary_with_secondary`
- 题目：如果你发现对方有另一个社交账号或另一部手机，你更可能怎么处理？
- 选项：
  - A. 先问清楚用途，不直接定性。
  - B. 会明显警觉，但听解释。
  - C. 会要求对方证明没有问题。
  - D. 会认为这是严重隐瞒。
  - E. 会自己也开始保留信息。
- 影响维度：`digital_alt_account_tendency`、`trust_suspicion_sensitivity`、`trust_checking_impulse`
- 备注：用于双账号、双重身份和证据链。

### Q135 聊天记录透明度

- 题型：`axis_2d`
- 题目：你对聊天记录透明度的期待更接近哪里？
- 横轴：0 = 聊天记录属于个人隐私；100 = 恋人之间必要时应能解释聊天内容。
- 纵轴：0 = 自己和对方规则一致；100 = 希望对方更透明，自己保留更多空间。
- 影响维度：`digital_phone_privacy_need`、`info_transparency_preference`、`boundary_double_standard`
- 备注：用于手机隐私和双标。

### Q136 社交媒体公开承诺

- 题型：`ranked_multi`
- 题目：以下哪些数字生活行为最能让你感觉关系被认真对待？请选择最多三项并排序。
- 选项：
  - A. 公开合照或朋友圈。
  - B. 在朋友面前自然介绍你。
  - C. 不隐藏和你的互动。
  - D. 主动说明容易误会的异性互动。
  - E. 重要行程提前说。
  - F. 不和暧昧对象频繁互动。
- 影响维度：`digital_social_media_display`、`info_transparency_preference`、`trust_loyalty_sensitivity`
- 备注：用于数字承诺和公开关系。

### Q137 删除、撤回和已读不回

- 题型：`multi_with_primary`
- 题目：数字聊天中，哪些行为最容易让你不安？可以多选，并标出最主要的一项。
- 选项：
  - A. 经常撤回消息。
  - B. 删除聊天记录。
  - C. 已读或在线但不回。
  - D. 聊天时突然消失。
  - E. 深夜和别人互动。
  - F. 手机总是遮着。
  - G. 朋友圈分组隐藏。
- 影响维度：`digital_evidence_awareness`、`digital_availability_pressure`、`trust_suspicion_sensitivity`
- 备注：用于数字生活风险聚合。

### Q138 数字生活自评

- 题型：`slider`
- 题目：你认为自己在数字生活中有多透明、稳定、不制造误会？
- 滑条：0 = 经常制造误会；100 = 很透明稳定。
- 影响维度：`digital_response_norm`、`info_transparency_preference`、`self_discrepancy_awareness`
- 备注：与 Q131-Q137 对照。

## 4. 第四批题库：家庭、成长与关系脚本补充

### Q139 原生冲突模板

- 题型：`forced_single`
- 题目：你成长环境中更常见的冲突处理方式是什么？
- 选项：
  - A. 有问题会说开。
  - B. 冷战或沉默。
  - C. 爆发争吵。
  - D. 表面和好，但问题不解决。
  - E. 很少看到亲密关系如何处理冲突。
- 影响维度：`family_conflict_model`、`communication_conflict_avoidance`、`emotion_anger_control`
- 备注：用于关系脚本来源。

### Q140 成长安全感

- 题型：`slider`
- 题目：从成长经历看，你有多容易相信“重要的人会稳定地在乎我”？
- 滑条：0 = 很难相信；100 = 比较容易相信。
- 影响维度：`family_attachment_history`、`attachment_abandonment_anxiety`、`trust_baseline`
- 备注：不作诊断，只用于安全感基础。

### Q141 默认恋爱剧本

- 题型：`ranked_multi`
- 题目：你默认认为一段认真关系应该逐步走向哪些事情？请选择并排序。
- 选项：
  - A. 稳定联系。
  - B. 确认关系名分。
  - C. 公开给朋友。
  - D. 见家人。
  - E. 同居或长期生活规划。
  - F. 经济上互相支持。
  - G. 保留高度个人空间。
- 影响维度：`family_relationship_script`、`attachment_commitment_pace`、`values_family_orientation`
- 备注：用于关系推进冲突。

### Q142 模式重复觉察

- 题型：`reverse_check`
- 题目：你是否发现自己在不同关系里反复遇到类似问题？
- 选项：
  - A. 很少，问题通常不同。
  - B. 偶尔会有类似模式。
  - C. 经常在信任或沟通上重复。
  - D. 经常在边界或自由上重复。
  - E. 我知道有重复，但很难改变。
- 影响维度：`family_repetition_awareness`、`risk_repeat_pattern`、`self_reflection_capacity`
- 备注：用于长期成长和报告洞察。

## 5. 第四批题库：综合反向验证与最终总结

### Q143 自述人格一致性

- 题型：`reverse_check`
- 题目：以下哪种情况最像你？
- 选项：
  - A. 我自认为怎样，实际也大多这样。
  - B. 我自认为成熟，但压力下会变得不像自己。
  - C. 我自认为尊重边界，但不安时会想控制或查证。
  - D. 我自认为诚实，但怕冲突时会说一半。
  - E. 我自认为专一，但被理解或欣赏时会动摇。
- 影响维度：`self_discrepancy_awareness`、`self_justification_tendency`、`trust_checking_impulse`、`info_concealment_tendency`、`desire_temptation_resistance`
- 备注：综合自述/情境差异。

### Q144 自我美化风险总结

- 题型：`multi_with_primary`
- 题目：如果你的答案前后不完全一致，最可能是因为什么？可以多选，并标出最主要的一项。
- 选项：
  - A. 我平时和压力下确实不一样。
  - B. 我希望自己是更成熟的人。
  - C. 有些事要看对方怎么做。
  - D. 我对自己比较宽容，对别人比较严格。
  - E. 题目太复杂，现实里很难确定。
  - F. 我没有明显矛盾。
- 影响维度：`self_discrepancy_awareness`、`self_justification_tendency`、`boundary_double_standard`
- 备注：不惩罚矛盾，记录可信度。

### Q145 压力下真实反应

- 题型：`ranked_multi`
- 题目：当你压力非常大、关系又出问题时，最可能出现哪些反应？请选择最多五项并排序。
- 选项：
  - A. 冷处理或消失。
  - B. 追问、查证、确认。
  - C. 说重话或冲动分手。
  - D. 找朋友或第三方倾诉。
  - E. 隐瞒一些细节避免吵架。
  - F. 寻找新的情绪价值。
  - G. 主动复盘和修复。
  - H. 把现实压力先处理好。
- 影响维度：`risk_avoidant_disappearance`、`trust_checking_impulse`、`communication_cruelty_under_conflict`、`info_concealment_tendency`、`desire_emotional_validation_hunger`、`communication_repair_initiative`
- 备注：用于行为人格初始预测。

### Q146 最希望对方理解你的部分

- 题型：`open_text`
- 题目：如果要让对方真正理解你，你最希望对方知道你哪一部分？
- 开放文本：建议 50-300 字。
- 影响维度：`attachment_vulnerability_fear`、`values_spiritual_resonance_need`、`self_acceptance`
- 备注：当前不自动计分，可用于玩家报告和角色设定。

### Q147 最担心被对方看见的部分

- 题型：`open_text`
- 题目：在亲密关系里，你最担心对方看见你哪一面？
- 开放文本：建议 50-300 字。
- 影响维度：`attachment_vulnerability_fear`、`self_acceptance`、`self_image_management`
- 备注：用于脆弱暴露和外显/真实人格差异。

### Q148 最不能接受对方重复的问题

- 题型：`ranked_multi`
- 题目：如果对方反复出现以下问题，哪些最可能让你彻底失望？请选择最多五项并排序。
- 选项：
  - A. 反复失联或冷处理。
  - B. 反复撒谎或说一半。
  - C. 反复异性边界不清。
  - D. 反复不守承诺。
  - E. 反复情绪攻击。
  - F. 反复逃避现实责任。
  - G. 反复不公开或不给名分。
  - H. 反复控制你。
- 影响维度：`moral_line_clarity`、`trust_old_wound_memory`、`risk_repeat_pattern`
- 备注：用于结局和长期伤口。

### Q149 最可能导致你改变的方式

- 题型：`ranked_multi`
- 题目：如果你在关系里有问题，哪些方式最可能让你真正改变？请选择最多三项并排序。
- 选项：
  - A. 对方冷静指出具体行为。
  - B. 看到对方真的受伤。
  - C. 对方给出明确边界和后果。
  - D. 关系差点失去。
  - E. 自己反复复盘后意识到。
  - F. 朋友或家人提醒。
  - G. 对方持续包容和鼓励。
- 影响维度：`self_reflection_capacity`、`moral_harm_awareness`、`moral_commitment_credibility`、`communication_meta_discussion`
- 备注：用于成长和修复路线。

### Q150 超级真实版最终总结

- 题型：`multi_with_primary`
- 题目：做完整份问卷后，你觉得自己在亲密关系里最核心的矛盾是什么？可以多选，并标出最主要的一项。
- 选项：
  - A. 想要亲密，但又害怕失去自由。
  - B. 想相信对方，但又忍不住怀疑。
  - C. 想诚实，但又害怕冲突。
  - D. 想稳定，但又需要新鲜感。
  - E. 想被理解，但不太会表达脆弱。
  - F. 想成熟沟通，但情绪上来会失控或逃避。
  - G. 想让规则公平，但现实里会双标。
  - H. 暂时没有明显核心矛盾。
- 影响维度：`attachment_intimacy_avoidance`、`trust_suspicion_sensitivity`、`info_concealment_tendency`、`desire_novelty_need`、`attachment_vulnerability_fear`、`communication_defensiveness`、`boundary_double_standard`
- 备注：用于超级真实版最终报告主画像。

## 6. 第四批覆盖说明

第四批主要覆盖：

- 社交圈影响；
- 共同好友和流言传播；
- 朋友与恋人冲突；
- 社交场合被忽略；
- 朋友圈展示比较；
- 时间投入能力；
- 时间管理失误；
- 金钱压力；
- 作息不一致；
- 家庭压力和家庭边界；
- 工作/学业高压期；
- 现实条件不匹配；
- 在线可得压力；
- 点赞评论边界；
- 朋友圈可见性；
- 两个账号/两部手机；
- 聊天记录透明度；
- 数字生活自评；
- 原生冲突模板；
- 成长安全感；
- 默认恋爱剧本；
- 模式重复觉察；
- 自述人格一致性；
- 自我美化风险；
- 压力下真实反应；
- 超级真实版最终总结。

## 7. 题库阶段性结论

截至第四批，超级真实版题库已经形成 Q001-Q150 的完整第一版结构：

- 第一批 Q001-Q030：基础资料、恋爱经历、依恋亲密；
- 第二批 Q031-Q070：信任怀疑、边界占有、诚实隐瞒、双标检测；
- 第三批 Q071-Q110：冲突沟通、欲望忠诚、道德责任；
- 第四批 Q111-Q150：社交网络、现实压力、数字生活、家庭成长、综合反向验证。

后续不建议立刻继续无限加题，而应先做：

1. `docs/design/19_relationship_report_templates.md`：问卷报告模板；
2. `docs/design/22_questionnaire_scoring_rules.md`：问卷计分和可信度规则；
3. 将 Q001-Q150 按模块整理成可配置 JSON 草案；
4. 检查每个128维度的覆盖率，标出证据不足的维度。

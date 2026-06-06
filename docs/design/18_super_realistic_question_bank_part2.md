# 超级真实版题库 第二批 v0.1

本文档是 `docs/design/18_super_realistic_question_bank.md` 的续写文件，用于整理超级真实版题库第二批。

第二批覆盖：

- 信任与怀疑；
- 占有欲与边界；
- 诚实、隐瞒与信息管理；
- 双标检测配对题；
- 自我美化和反向验证题。

本文档只做题库设计，不修改控制台原型运行逻辑。

## 1. 第二批题库：信任与怀疑

### Q031 对方解释不完整

- 题型：`primary_with_secondary`
- 题目：对方说自己晚上在外面，但解释得很模糊，没有说清楚和谁、在哪里。你更可能怎么反应？
- 选项：
  - A. 先相信对方，等之后自然说。
  - B. 有点不安，但先不追问。
  - C. 温和地问清楚细节。
  - D. 直接追问为什么说不清。
  - E. 表面不问，私下开始查线索。
- 影响维度：`trust_baseline`、`trust_suspicion_sensitivity`、`trust_checking_impulse`、`trust_explanation_acceptance`
- 备注：用于模糊解释、神秘电话、外出事件。

### Q032 怀疑细节敏感度

- 题型：`slider`
- 题目：当对方的说法出现一点点前后不一致时，你会有多在意？
- 滑条：0 = 不太在意，可能只是记错；100 = 非常在意，会反复想。
- 影响维度：`trust_suspicion_sensitivity`、`trust_old_wound_memory`
- 备注：高值不等于不信任，也可能表示观察力强。

### Q033 查证冲动

- 题型：`slider`
- 题目：当你对对方的话产生怀疑时，你有多想通过朋友圈、共同好友、定位、聊天时间线来确认？
- 滑条：0 = 基本不会查；100 = 很想查到确定答案。
- 影响维度：`trust_checking_impulse`、`digital_evidence_awareness`、`risk_boundary_violation`
- 备注：用于区分“内心怀疑”和“实际查证”。

### Q034 对方和前任联系

- 题型：`primary_with_secondary`
- 题目：你发现对方偶尔还会和前任联系，但内容看起来不算暧昧。你更可能怎么处理？
- 选项：
  - A. 可以接受，只要边界清楚。
  - B. 会不舒服，希望对方主动说明。
  - C. 要求知道他们为什么联系。
  - D. 明确要求减少或停止联系。
  - E. 表面不说，但开始记在心里。
- 影响维度：`trust_loyalty_sensitivity`、`boundary_possessiveness`、`trust_old_wound_memory`
- 备注：用于前任边界和旧伤触发。

### Q035 自己和前任联系

- 题型：`npc_perspective`
- 题目：如果是你偶尔和前任联系，但你认为内容不暧昧，你觉得这件事需要告诉现任吗？
- 选项：
  - A. 应该主动说明，避免误会。
  - B. 如果对方问起就说。
  - C. 不说也没关系，因为没做亏心事。
  - D. 看现任性格，怕麻烦就先不说。
  - E. 我不希望对方这样做，但我自己这样做问题不大。
- 影响维度：`boundary_double_standard`、`info_concealment_tendency`、`trust_projection_tendency`
- 备注：与 Q034 配对检测双标。

### Q036 神秘电话

- 题型：`primary_with_secondary`
- 题目：你看到对方接到一个电话后刻意走远，回来后只说“没什么”。你第一反应是什么？
- 选项：
  - A. 每个人都有隐私，不多问。
  - B. 会有点不舒服，但先观察。
  - C. 会问是谁打来的。
  - D. 会追问为什么要走远。
  - E. 会联想到隐瞒或暧昧。
- 影响维度：`trust_baseline`、`trust_suspicion_sensitivity`、`digital_phone_privacy_need`
- 备注：直接服务神秘电话事件。

### Q037 手机朝下/遮屏幕

- 题型：`slider`
- 题目：对方和你在一起时经常把手机屏幕朝下、消息来了也不看，你会有多在意？
- 滑条：0 = 不太在意；100 = 非常在意，会认为有问题。
- 影响维度：`trust_suspicion_sensitivity`、`digital_phone_privacy_need`、`digital_evidence_awareness`
- 备注：用于手机隐私和误会事件。

### Q038 解释接受度

- 题型：`axis_2d`
- 题目：当对方给出解释后，你通常更接近哪个位置？
- 横轴：0 = 解释合理就愿意相信；100 = 即使合理也会保留怀疑。
- 纵轴：0 = 不会继续查；100 = 仍会想确认更多细节。
- 影响维度：`trust_explanation_acceptance`、`trust_checking_impulse`、`trust_old_wound_memory`
- 备注：用于信任修复和圆谎空间。

### Q039 信任受损后的记忆

- 题型：`slider`
- 题目：如果某件事让你失望，即使后来和好了，你会有多容易在下一次冲突中想起它？
- 滑条：0 = 基本不会翻旧账；100 = 很容易联想到旧事。
- 影响维度：`trust_old_wound_memory`、`emotion_suppression_tendency`、`communication_cruelty_under_conflict`
- 备注：用于旧账和长期记忆伤口。

### Q040 反向投射

- 题型：`reverse_check`
- 题目：如果你自己曾经选择性隐瞒过一些事，你会不会因此更怀疑对方也在隐瞒？
- 选项：
  - A. 不会，我会分开看。
  - B. 偶尔会想到，但不会影响判断。
  - C. 会有一点，因为人都会保留。
  - D. 会明显更怀疑对方。
  - E. 我自己能控制，但很难相信对方也能控制。
- 影响维度：`trust_projection_tendency`、`boundary_double_standard`、`info_concealment_tendency`
- 备注：用于检测“自己会做，所以也怀疑别人”的逻辑。

## 2. 第二批题库：占有欲与边界

### Q041 对方和异性单独吃饭

- 题型：`primary_with_secondary`
- 题目：对方说要和一个异性朋友单独吃饭，你更能接受哪种情况？
- 选项：
  - A. 可以接受，只要正常说明。
  - B. 可以，但希望提前知道是谁。
  - C. 可以，但不接受临时隐瞒。
  - D. 不太能接受，除非一起去或有其他人在场。
  - E. 基本不能接受。
- 影响维度：`boundary_possessiveness`、`trust_loyalty_sensitivity`、`social_boundary_awareness`
- 备注：v0.1 题2升级版。

### Q042 自己和异性单独吃饭

- 题型：`npc_perspective`
- 题目：如果是你和异性朋友单独吃饭，你觉得需要提前告诉恋人吗？
- 选项：
  - A. 需要，避免误会。
  - B. 如果关系稳定，应该说。
  - C. 对方问起再说就可以。
  - D. 没暧昧就不必特别说。
  - E. 我希望自己自由，但对方最好提前说。
- 影响维度：`boundary_double_standard`、`info_concealment_tendency`、`boundary_rule_negotiation`
- 备注：与 Q041 配对检测双标。

### Q043 异性朋友边界排序

- 题型：`ranked_multi`
- 题目：以下异性社交行为中，你最介意哪些？请选择最多五项并排序。
- 选项：
  - A. 单独吃饭。
  - B. 深夜聊天。
  - C. 分享情绪和秘密。
  - D. 肢体接触或暧昧玩笑。
  - E. 隐瞒见面。
  - F. 和前任保持联系。
  - G. 朋友圈互动频繁。
  - H. 删除聊天记录。
- 影响维度：`trust_loyalty_sensitivity`、`digital_online_flirt_boundary`、`moral_line_clarity`
- 备注：用于边界协议和严重度排序。

### Q044 公开关系与安全感

- 题型：`slider`
- 题目：对方是否公开你们的关系，会多大程度影响你的安全感？
- 滑条：0 = 几乎不影响；100 = 非常影响。
- 影响维度：`digital_social_media_display`、`social_reputation_sensitivity`、`values_belonging_need`
- 备注：用于朋友圈、名分和公开关系事件。

### Q045 对方要求你报备

- 题型：`primary_with_secondary`
- 题目：如果恋人要求你出门前说明和谁、去哪、几点回来，你更可能怎么反应？
- 选项：
  - A. 可以接受，这是互相尊重。
  - B. 重要场合可以说，但不想事事报备。
  - C. 会觉得有点被管。
  - D. 会明确拒绝这种要求。
  - E. 我可以报备，但也要求对方同样报备。
- 影响维度：`boundary_autonomy_assertion`、`boundary_rule_negotiation`、`values_freedom_need`
- 备注：用于边界协商。

### Q046 你要求对方报备

- 题型：`npc_perspective`
- 题目：你希望恋人出门前告诉你和谁、去哪、几点回来吗？
- 选项：
  - A. 不需要，除非特殊情况。
  - B. 希望大概说一下。
  - C. 希望比较清楚地说明。
  - D. 如果不说我会明显不安。
  - E. 我不喜欢被要求报备，但希望对方报备。
- 影响维度：`boundary_control_need`、`boundary_double_standard`、`emotion_reassurance_need`
- 备注：与 Q045 配对检测双标和控制欲。

### Q047 手机隐私边界

- 题型：`axis_2d`
- 题目：你怎么看恋人之间的手机隐私？
- 横轴：0 = 手机应保持私人空间；100 = 恋人之间应该尽量透明。
- 纵轴：0 = 自己也愿意透明；100 = 自己不喜欢被查但想知道对方。
- 影响维度：`digital_phone_privacy_need`、`boundary_double_standard`、`trust_privacy_trust`
- 备注：用于手机、聊天记录、定位冲突。

### Q048 定位共享

- 题型：`forced_single`
- 题目：你对恋人之间共享实时定位怎么看？
- 选项：
  - A. 不需要，容易变成控制。
  - B. 特殊情况可以，例如夜归或旅行。
  - C. 双方都愿意时可以。
  - D. 我会更有安全感，希望可以共享。
  - E. 我希望知道对方位置，但不太想被持续看到。
- 影响维度：`digital_location_transparency`、`boundary_double_standard`、`trust_checking_impulse`
- 备注：E 用于双标检测。

### Q049 对方穿着和社交

- 题型：`primary_with_secondary`
- 题目：如果恋人的穿着或社交方式让你觉得容易被别人注意，你更可能怎么做？
- 选项：
  - A. 尊重对方，不干涉。
  - B. 会表达一点不安，但不要求改变。
  - C. 会建议对方注意分寸。
  - D. 会明确表示不喜欢。
  - E. 会用冷淡或情绪让对方自己意识到。
- 影响维度：`boundary_control_need`、`boundary_possessiveness`、`boundary_manipulation_tendency`
- 备注：用于控制欲和间接施压。

### Q050 边界协议能力

- 题型：`ranked_multi`
- 题目：如果你们因为异性朋友、手机、定位发生争执，你觉得最好的解决方式是什么？请选择最多三项并排序。
- 选项：
  - A. 直接定清楚哪些事要提前说。
  - B. 双方都保留隐私，但不能隐瞒关键事实。
  - C. 只要不出轨，就不该限制太多。
  - D. 给彼此看手机来恢复信任。
  - E. 先暂停争吵，等情绪稳定再谈。
  - F. 谁更不安，就先照顾谁的感受。
- 影响维度：`boundary_rule_negotiation`、`boundary_respect`、`communication_meta_discussion`
- 备注：用于边界协议和修复方案。

## 3. 第二批题库：诚实、隐瞒与信息管理

### Q051 做了可能让对方不高兴的事

- 题型：`primary_with_secondary`
- 题目：你做了一件可能让对方不高兴、但你觉得不算严重的事。对方问起来时，你更可能怎么说？
- 选项：
  - A. 主动完整说明。
  - B. 只说重点，不展开细节。
  - C. 等对方问到细节再说。
  - D. 模糊带过，避免吵架。
  - E. 反问对方为什么不信任自己。
- 影响维度：`info_honesty_tendency`、`info_concealment_tendency`、`info_partial_truth_tendency`、`communication_defensiveness`
- 备注：v0.1 题8升级版。

### Q052 隐瞒原因

- 题型：`multi_with_primary`
- 题目：如果你选择不全部说明，最可能是因为什么？可以多选，并标出最主要原因。
- 选项：
  - A. 怕吵架。
  - B. 觉得事情不严重。
  - C. 怕对方误会。
  - D. 想保留私人空间。
  - E. 自己也有点心虚。
  - F. 觉得对方管太多。
  - G. 想先观察对方反应。
- 影响维度：`info_concealment_tendency`、`communication_conflict_avoidance`、`self_justification_tendency`
- 备注：给 Q051 提供 `reason_tags`。

### Q053 直接撒谎压力

- 题型：`slider`
- 题目：在压力很大、又怕关系出问题时，你有多可能直接说一个不真实但能暂时解决问题的答案？
- 滑条：0 = 基本不会；100 = 很可能。
- 影响维度：`info_honesty_tendency`、`info_lie_skill`、`moral_consequence_forecast`
- 备注：高值需要反向验证，不单题判定。

### Q054 半真半假

- 题型：`forced_single`
- 题目：你怎么看“说的都是真的，但故意省略最关键的部分”？
- 选项：
  - A. 这也算欺骗。
  - B. 要看省略的内容重不重要。
  - C. 如果是避免吵架，可以理解。
  - D. 只要没有直接撒谎，就不算严重。
  - E. 我会这样做，但不希望对方这样对我。
- 影响维度：`info_partial_truth_tendency`、`moral_line_clarity`、`boundary_double_standard`
- 备注：E 为双标检测。

### Q055 删除聊天记录

- 题型：`primary_with_secondary`
- 题目：如果你和某个人的聊天容易引起误会，但你觉得自己没有越界，你会怎么处理聊天记录？
- 选项：
  - A. 不删，清清楚楚最好。
  - B. 不主动给对方看，但也不删。
  - C. 会删掉容易误会的部分。
  - D. 会把聊天隐藏起来，避免麻烦。
  - E. 会减少联系，而不是处理记录。
- 影响维度：`info_secret_management`、`digital_evidence_awareness`、`info_concealment_tendency`
- 备注：用于证据链和小号事件。

### Q056 小号和备用账号

- 题型：`forced_single`
- 题目：你怎么看恋爱中使用小号、分组可见或备用账号？
- 选项：
  - A. 没必要，容易制造不信任。
  - B. 正常隐私可以有，但不能用于暧昧。
  - C. 如果只是保护私人空间，可以接受。
  - D. 如果对方管太多，我会考虑使用。
  - E. 我自己可以有，但不太能接受对方有。
- 影响维度：`digital_alt_account_tendency`、`info_secret_management`、`boundary_double_standard`
- 备注：用于双账号和真实/外显档案差异。

### Q057 被揭穿后的第一反应

- 题型：`primary_with_secondary`
- 题目：如果你隐瞒的事被对方发现，你第一反应更接近哪种？
- 选项：
  - A. 承认事实并解释原因。
  - B. 先解释自己不是故意的。
  - C. 强调事情没那么严重。
  - D. 反问对方为什么查你。
  - E. 否认或继续圆过去。
- 影响维度：`info_exposure_reaction`、`moral_accountability_under_exposure`、`communication_defensiveness`
- 备注：用于危机线和修复机会。

### Q058 对方被揭穿后的反应

- 题型：`npc_perspective`
- 题目：如果对方隐瞒的事被你发现，你最希望对方第一时间怎么做？
- 选项：
  - A. 完整承认事实。
  - B. 解释原因，但不能继续隐瞒。
  - C. 主动拿出证据证明没有更严重问题。
  - D. 道歉并提出之后怎么避免。
  - E. 给你时间冷静。
- 影响维度：`trust_explanation_acceptance`、`moral_compensation_willingness`、`emotion_reassurance_need`
- 备注：与 Q057 对照，检测自己和对方标准差异。

### Q059 撒谎能力自评

- 题型：`slider`
- 题目：如果你真的想隐瞒一件事，你觉得自己有多能维持说法不露出破绽？
- 滑条：0 = 很容易露馅；100 = 很擅长维持说法。
- 影响维度：`info_lie_skill`、`info_secret_management`、`self_image_management`
- 备注：自评题，后续需要行为和反向题验证。

### Q060 隐瞒后的愧疚

- 题型：`slider`
- 题目：如果你隐瞒了一件会让对方难受的事，即使对方没发现，你会有多愧疚？
- 滑条：0 = 几乎不会愧疚；100 = 会明显内耗或想补偿。
- 影响维度：`info_guilt_after_deception`、`moral_harm_awareness`、`moral_compensation_willingness`
- 备注：用于补偿行为和内心矛盾。

### Q061 透明偏好

- 题型：`axis_2d`
- 题目：你希望关系中的信息透明度更接近哪里？
- 横轴：0 = 各自保留隐私；100 = 重要行程和社交都应透明。
- 纵轴：0 = 自己和对方规则一致；100 = 希望对方更透明，自己保留更多隐私。
- 影响维度：`info_transparency_preference`、`boundary_double_standard`、`digital_phone_privacy_need`
- 备注：综合测透明偏好与双标。

### Q062 数字证据意识

- 题型：`multi_with_primary`
- 题目：如果你想确认一件事的真实性，你最可能看哪些线索？可以多选，并标出最主要的一项。
- 选项：
  - A. 对方说法是否前后一致。
  - B. 朋友圈、点赞、评论时间。
  - C. 共同朋友动态。
  - D. 定位、打卡、照片背景。
  - E. 聊天记录或截图。
  - F. 付款记录、票据或行程痕迹。
  - G. 我通常不会查这些。
- 影响维度：`digital_evidence_awareness`、`trust_checking_impulse`、`risk_boundary_violation`
- 备注：用于证据链和暴露概率。

### Q063 自认为“为了关系好”的隐瞒

- 题型：`reverse_check`
- 题目：你是否认同“有些事不告诉对方，是为了避免无意义的争吵，反而是在保护关系”？
- 选项：
  - A. 基本不认同，重要事实应该说。
  - B. 小事可以不说，但关键事实不行。
  - C. 要看对方性格，太敏感就少说。
  - D. 认同，有些真话只会破坏关系。
  - E. 我可以这样想，但不希望对方这样对我。
- 影响维度：`self_justification_tendency`、`info_concealment_tendency`、`boundary_double_standard`
- 备注：检测自我合理化和双标。

### Q064 主动坦白时机

- 题型：`forced_single`
- 题目：如果你意识到自己做的事可能越界，你更可能什么时候坦白？
- 选项：
  - A. 当天就说。
  - B. 找合适时机尽快说。
  - C. 等对方情绪稳定或关系稳定时说。
  - D. 除非对方问，否则不主动说。
  - E. 能不说就不说，过去就算了。
- 影响维度：`info_honesty_tendency`、`moral_consequence_forecast`、`communication_repair_initiative`
- 备注：用于主动修复和隐瞒持续时间。

## 4. 第二批题库：双标与反向验证

### Q065 自评：我很诚实

- 题型：`slider`
- 题目：你认为自己在亲密关系中有多诚实？
- 滑条：0 = 经常保留或修饰；100 = 基本完整坦白。
- 影响维度：`info_honesty_tendency`、`self_discrepancy_awareness`
- 备注：需要与 Q051-Q064 情境题对照。

### Q066 自评与情境差异

- 题型：`reverse_check`
- 题目：如果你自认为很诚实，但在某些情况下会“说一半”或“先不说”，你觉得这更像什么？
- 选项：
  - A. 这说明我其实没有那么诚实。
  - B. 这是现实沟通策略，不代表不诚实。
  - C. 只要不是恶意，就可以理解。
  - D. 对方太敏感时，我只能这样。
  - E. 我希望对方对我诚实，但我自己需要一点空间。
- 影响维度：`self_discrepancy_awareness`、`self_justification_tendency`、`boundary_double_standard`
- 备注：用于自我美化检测。

### Q067 自评：我尊重隐私

- 题型：`slider`
- 题目：你认为自己有多尊重恋人的隐私？
- 滑条：0 = 很想知道所有细节；100 = 非常尊重对方隐私。
- 影响维度：`boundary_respect`、`trust_privacy_trust`、`self_discrepancy_awareness`
- 备注：与 Q033、Q062 对照。

### Q068 不安时的实际查证

- 题型：`reverse_check`
- 题目：即使你认为自己尊重隐私，当你非常不安时，你最可能做什么？
- 选项：
  - A. 仍然不查，直接沟通。
  - B. 先观察，不主动翻东西。
  - C. 看公开动态或共同朋友线索。
  - D. 想看聊天记录或手机。
  - E. 会找机会确认具体证据。
- 影响维度：`trust_checking_impulse`、`risk_boundary_violation`、`self_discrepancy_awareness`
- 备注：自评与实际倾向差异。

### Q069 自己自由 vs 对方自由

- 题型：`axis_2d`
- 题目：在异性朋友、前任、手机隐私这些问题上，你对自己和对方的标准更接近哪里？
- 横轴：0 = 自己和对方规则完全一样；100 = 自己需要更多自由。
- 纵轴：0 = 对方也应有同等自由；100 = 对方需要更高透明度。
- 影响维度：`boundary_double_standard`、`values_freedom_need`、`trust_loyalty_sensitivity`
- 备注：核心双标坐标。

### Q070 第二批总结题

- 题型：`multi_with_primary`
- 题目：在信任、边界和诚实这三类问题中，你最容易卡在哪些地方？可以多选，并标出最主要的一项。
- 选项：
  - A. 很难完全相信对方解释。
  - B. 很难接受对方异性边界不清。
  - C. 很难控制自己查证的冲动。
  - D. 很难做到完全坦白。
  - E. 很难接受对方也保留隐私。
  - F. 很容易觉得自己有理由，但对方不该这样。
  - G. 暂时没有明显问题。
- 影响维度：`trust_suspicion_sensitivity`、`boundary_possessiveness`、`trust_checking_impulse`、`info_concealment_tendency`、`boundary_double_standard`
- 备注：用于第二批模块报告摘要。

## 5. 第二批覆盖说明

第二批主要覆盖：

- 基础信任；
- 怀疑敏感；
- 查证冲动；
- 解释接受度；
- 旧账记忆；
- 反向投射；
- 忠诚信任敏感；
- 隐私信任；
- 控制欲；
- 占有欲；
- 边界尊重；
- 双标倾向；
- 边界协商能力；
- 诚实倾向；
- 隐瞒倾向；
- 半真半假倾向；
- 撒谎能力；
- 欺瞒后愧疚；
- 被揭穿反应；
- 秘密管理能力；
- 数字证据意识；
- 自我美化和自述/情境差异。

## 6. 下一批建议

下一批建议继续写：

```text
冲突沟通 + 欲望忠诚 + 道德责任
```

目标约 40 题，重点包括：

- 吵架当下表达；
- 冷处理、拉黑、失联；
- 防御、反击、道歉；
- 复盘和修复尝试；
- 新鲜感、诱惑抵抗、情绪价值；
- 暧昧边界；
- 承诺可信度、补偿意愿、后果预判；
- 暴露后负责度和破罐破摔倾向。

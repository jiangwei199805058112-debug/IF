# 问卷扩展候选题池

本文档用于整理 IF 后续问卷扩展候选题。它不是立即修改 `if_game/data/questionnaire_mvp.json` 的执行文件，也不是完整题库终稿，而是为后续从 25 题快速版扩展到 40 题、60 题或标准版问卷提供候选池。

核心原则：

```text
当前 25 题 MVP 先保持稳定。
本文件只沉淀候选题，不直接进入运行逻辑。
后续每次只小批量加入题目，并同步更新 loader、scoring、reporting、runner 和测试。
```

---

## 1. 设计目标

当前 MVP 问卷已经覆盖：

- 关系入口；
- 认识背景；
- 联系频率；
- 现实距离；
- 依恋；
- 信任；
- 隐瞒；
- 冲突；
- 边界；
- 修复。

后续扩展应优先补充 `25-35` 号设计文档新增的系统：

```text
伴侣认知准确度
自我表露与回应性
秘密与隐私边界
冲突沟通与修复
社会交换与替代选择
接近/回避动机与关系沉闷
共有/交换与公平感
```

---

## 2. 题型约束

后续加入 MVP 时，优先使用当前 runner/scoring 已支持的题型：

```text
forced_single
primary_with_secondary
multi_with_primary
slider
axis_2d
```

暂不优先使用：

```text
排序题
开放文本题
复杂权重分配题
NPC 多视角长题
多阶段动态题
```

---

## 3. 候选题优先级

| 优先级 | 含义 |
| --- | --- |
| P0 | 后续最适合先加入 MVP 的题 |
| P1 | 标准版问卷建议加入 |
| P2 | 深度版或后续扩展再加入 |

建议 v0.1.38 优先加入：

```text
Q-COM-01
Q-COM-05
Q-COM-06
Q-COM-10
```

---

## 4. 模块一：沟通、自我表露与回应性

来源：

```text
docs/design/27_communication_self_disclosure_system.md
docs/design/28_questionnaire_communication_disclosure_module.md
docs/design/37_relationship_report_tag_dictionary.md
```

### Q-COM-01：自我表露意愿

| 字段 | 内容 |
| --- | --- |
| 优先级 | P0 |
| 题型 | `forced_single` |
| 主要维度 | `self_disclosure_willingness`、`disclosure_pacing`、`over_disclosure_risk`、`under_disclosure_gap` |

题干：

```text
当关系逐渐亲近后，你愿意主动说出自己的不安、过去经历或真实需求吗？
```

选项：

| 选项 | 含义 |
| --- | --- |
| A. 基本不会，除非被问到 | 低表露 |
| B. 会说一部分，但会保留很多 | 中低表露 |
| C. 看对方反应，如果安全才说 | 条件表露 |
| D. 会主动分享重要经历和情绪 | 高表露 |
| E. 很容易一开始就说很多 | 过快表露风险 |

---

### Q-COM-02：表露内容范围

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `multi_with_primary` |
| 主要维度 | `disclosure_breadth`、`disclosure_depth`、`taboo_topic_avoidance` |

题干：

```text
在亲密关系中，你通常会把哪些内容告诉对方？请选择所有符合项，并标出最主要的一类。
```

选项：

```text
A. 日常生活
B. 兴趣爱好
C. 工作/学习压力
D. 家庭关系
E. 前任经历
F. 自卑或脆弱
G. 金钱压力
H. 性、欲望或边界
I. 做错过的事
J. 几乎不说深层内容
```

---

### Q-COM-03：表露节奏

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `disclosure_pacing`、`pressure_disclosure_pattern`、`reciprocal_disclosure_need` |

题干：

```text
如果你刚和一个人关系升温，你会多久开始说比较私人的事情？
```

选项：

```text
A. 很早，只要聊得来就说
B. 关系明显稳定后才说
C. 对方先说，我才跟着说
D. 很久也不太说
E. 只有吵架或崩溃时才说
```

---

### Q-COM-04：表露互惠需求

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `reciprocal_disclosure_need`、`partner_disclosure_expectation`、`trust_sensitivity` |

题干：

```text
如果你向对方说了一个比较私人的事情，而对方很少说自己的事，你通常会怎么想？
```

选项：

```text
A. 没关系，每个人节奏不同
B. 会有点失落，但能接受
C. 会觉得不公平，好像只有我在暴露
D. 会怀疑对方不信任我
E. 我本来也不想说太多
```

---

### Q-COM-05：回应性需求

| 字段 | 内容 |
| --- | --- |
| 优先级 | P0 |
| 题型 | `primary_with_secondary` |
| 主要维度 | `perceived_responsiveness_need`、`emotional_validation_need`、`privacy_boundary_strength` |

题干：

```text
当你说出一件让你难过或不安的事时，你最希望对方怎么回应？
```

选项：

```text
A. 认真听，不急着评价
B. 给我明确安慰和陪伴
C. 帮我分析解决办法
D. 只要别嘲笑我就行
E. 也分享他/她的类似经历
F. 不希望对方追问太多
```

---

### Q-COM-06：哪些事情可以保留不说

| 字段 | 内容 |
| --- | --- |
| 优先级 | P0 |
| 题型 | `multi_with_primary` |
| 主要维度 | `privacy_boundary_strength`、`secret_tolerance`、`partner_disclosure_expectation`、`taboo_topic_avoidance` |

题干：

```text
恋爱后，你认为哪些事情可以保留不说？请选择所有符合项，并标出你最坚持的一项。
```

选项：

```text
A. 和前任是否还有联系
B. 过去恋爱经历细节
C. 手机聊天内容
D. 金钱情况
E. 家庭矛盾
F. 曾经做错的事
G. 当前异性朋友情况
H. 心里对关系的不满
I. 性、欲望相关想法
J. 基本都应该坦白
```

---

### Q-COM-07：对方保留秘密时的反应

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `secret_tolerance`、`privacy_boundary_respect`、`relationship_threat_sensitivity` |

题干：

```text
如果对方说“有些事我想自己保留”，你通常会怎么反应？
```

选项：

```text
A. 能尊重，只要不伤害关系
B. 会接受，但心里有点不安
C. 会想知道到底是什么
D. 会觉得对方不信任我
E. 如果是亲密关系，就不该有秘密
```

---

### Q-COM-08：开启者能力

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `forced_single` |
| 主要维度 | `opener_skill`、`listening_quality`、`emotional_safety_signal` |

题干：

```text
别人是否经常愿意告诉你他们自己的私事或真实感受？
```

选项：

```text
A. 很少，别人通常不太跟我说深层内容
B. 偶尔会，看关系和情境
C. 比较常见，朋友会找我倾诉
D. 很多人会说我让他们放松
E. 我不太喜欢别人对我说太多
```

---

### Q-COM-09：爱意表达需求

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `verbal_affection_need`、`words_actions_consistency_sensitivity`、`reassurance_dependency` |

题干：

```text
在亲密关系中，你需要对方清楚说出喜欢、在乎或爱吗？
```

选项：

```text
A. 很需要，不说我会不安
B. 比较需要，偶尔明确表达就好
C. 行动更重要，说不说都可以
D. 我自己也不太习惯说这些
E. 说太多反而让我觉得不真实
```

---

### Q-COM-10：自己表露 vs 希望对方表露

| 字段 | 内容 |
| --- | --- |
| 优先级 | P0 |
| 题型 | `axis_2d` |
| 主要维度 | `self_disclosure_willingness`、`partner_disclosure_expectation`、`transparency_double_standard_risk` |

题干：

```text
请分别评估：你通常愿意向对方表露多少私人内容？你希望对方向你表露多少私人内容？
```

二维坐标：

```text
X 轴：自己表露程度，0 = 几乎不说，100 = 很多都愿意说
Y 轴：希望对方表露程度，0 = 对方可以保留很多，100 = 希望对方尽量坦白
```

---

## 5. 模块二：冲突沟通与修复

来源：

```text
docs/design/29_conflict_communication_repair_system.md
docs/design/35_relationship_event_template_library.md
```

### Q-CON-01：被指出问题时的第一反应

| 字段 | 内容 |
| --- | --- |
| 优先级 | P0 |
| 题型 | `forced_single` |
| 主要维度 | `defensive_response`、`validation_skill`、`repair_attempt_quality` |

题干：

```text
如果伴侣认真指出你某件事让他/她不舒服，你第一反应通常更接近哪一种？
```

选项：

```text
A. 先听完，确认对方具体不舒服在哪里
B. 先解释自己为什么这么做
C. 会有点委屈，但愿意继续谈
D. 会反问对方是不是也有类似问题
E. 会觉得对方小题大做，不想继续谈
```

---

### Q-CON-02：争吵中是否打断

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `interrupting_tendency`、`active_listening_skill`、`conflict_escalation_risk` |

题干：

```text
争吵时，如果你觉得对方说得不对，你通常会怎么做？
```

选项：

```text
A. 先让对方说完，再回应
B. 会忍不住打断纠正
C. 会先记下来，之后再说自己的想法
D. 会提高音量抢回话语权
E. 会直接不想听了
```

---

### Q-CON-03：是否容易翻旧账

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `kitchen_sinking`、`old_wound_memory_sensitivity`、`conflict_escalation_risk` |

题干：

```text
一次争吵中，你会不会把以前类似的问题也一起说出来？
```

选项：

```text
A. 基本不会，只谈当前问题
B. 如果以前重复发生过，会提到
C. 情绪上来时会忍不住一起说
D. 会觉得不翻旧账对方永远不重视
E. 我通常压着不说，之后自己消化
```

---

### Q-CON-04：第一人称表达能力

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `i_statement_skill`、`behavior_description_accuracy`、`personality_attack_level` |

题干：

```text
如果对方在你说话时一直看手机，你最可能怎么表达？
```

选项：

```text
A. 你刚才看手机，我感觉自己没有被认真听
B. 你为什么总是不尊重我
C. 算了，没事
D. 你爱看就看，我也不理你了
E. 我会先忍着，之后找机会说
```

---

### Q-CON-05：暂停争吵方式

| 字段 | 内容 |
| --- | --- |
| 优先级 | P0 |
| 题型 | `forced_single` |
| 主要维度 | `conflict_timeout_skill`、`stonewalling_level`、`repair_after_timeout` |

题干：

```text
争吵太激烈时，你通常会怎么处理？
```

选项：

```text
A. 明确说我需要冷静，约定等会儿继续谈
B. 先离开，但之后会主动回来谈
C. 直接沉默，不知道什么时候再说
D. 拉黑/删除/消失一段时间
E. 继续说，直到把情绪发泄完
```

---

### Q-CON-06：道歉后的行动

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `repair_attempt_quality`、`words_actions_consistency_sensitivity`、`responsibility_taking` |

题干：

```text
如果你知道自己确实伤到了对方，道歉后你通常会怎么做？
```

选项：

```text
A. 提出具体以后怎么改，并尽量做到
B. 会安慰对方，但不太知道怎么改
C. 会道歉，但希望这件事快点过去
D. 会觉得自己已经道歉了，对方不该再提
E. 不太会主动道歉，除非对方逼我
```

---

### Q-CON-07：被误解时的反应

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `defensive_response`、`perception_checking_skill`、`conflict_escalation_risk` |

题干：

```text
如果对方误解了你的意思，你更可能怎么做？
```

选项：

```text
A. 先确认对方理解成了什么，再解释
B. 立刻解释自己不是那个意思
C. 会很委屈，觉得对方不信任我
D. 会反过来说对方总是乱想
E. 不想解释，觉得说了也没用
```

---

### Q-CON-08：是否会用嘲讽表达不满

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `forced_single` |
| 主要维度 | `contempt_signal`、`criticism_intensity`、`old_wound_memory_risk` |

题干：

```text
当你非常不满时，你会不会用讽刺、冷笑或挖苦来表达？
```

选项：

```text
A. 基本不会，我会尽量直接说问题
B. 偶尔会，但说完会后悔
C. 情绪上来时容易这样
D. 我觉得这比直接吵架好
E. 如果对方先伤我，我会用这种方式还回去
```

---

### Q-CON-09：对方哭或崩溃时的反应

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `comfort_skill`、`emotional_validation`、`advice_overload` |

题干：

```text
如果伴侣在你面前哭了或明显崩溃，你通常会怎么做？
```

选项：

```text
A. 先陪着，让对方慢慢说
B. 立刻帮对方分析怎么解决
C. 会安慰，但有点不知道怎么办
D. 会觉得压力很大，想躲开
E. 会觉得对方反应太大
```

---

### Q-CON-10：确认感受和不同意

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `validation_skill`、`respectful_disagreement`、`dismissive_disagreement` |

题干：

```text
如果你不认同伴侣的观点，但能理解他/她为什么难受，你会怎么表达？
```

选项：

```text
A. 我理解你为什么难受，但我也想说我的看法
B. 我会先安慰，但不太会说自己的不同意见
C. 我会直接说我不同意
D. 我会觉得既然不同意，就没必要确认感受
E. 我会先表面认同，避免继续吵
```

---

## 6. 模块三：社会交换、替代选择与依赖

来源：

```text
docs/design/30_social_exchange_dependency_system.md
docs/design/35_relationship_event_template_library.md
```

### Q-EXC-01：关系期待水平

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `slider` |
| 主要维度 | `comparison_level`、`expected_relationship_standard` |

题干：

```text
你对亲密关系整体质量的期待有多高？
```

滑条：

```text
0 = 稳定、没大问题就可以
100 = 需要高投入、高表达、高质量陪伴和共同成长
```

---

### Q-EXC-02：不够感

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `high_comparison_level`、`gratitude_buffer`、`entitlement_pressure` |

题干：

```text
如果对方稳定、可靠、没有原则性问题，但你总觉得关系不够好，你会怎么理解？
```

选项：

```text
A. 说明我需要更高质量的关系
B. 可能是我期待太高，需要调整
C. 会先观察具体缺什么
D. 会压下这种感觉，毕竟对方没错
E. 会想是不是外面有更适合的人
```

---

### Q-EXC-03：替代选择意识

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `slider` |
| 主要维度 | `comparison_level_alternatives`、`alternative_sensitive`、`replacement_confidence` |

题干：

```text
如果当前关系不满意，你觉得自己找到更合适关系或过好单身生活的信心有多高？
```

滑条：

```text
0 = 几乎没有信心
100 = 很有信心
```

---

### Q-EXC-04：遇到有吸引力的新对象

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `alternative_partner_attraction`、`moral_boundary`、`current_relationship_satisfaction` |

题干：

```text
如果你在当前关系中遇到一个很有吸引力、也很懂你的人，你通常会怎么处理？
```

选项：

```text
A. 会保持边界，不让它影响当前关系
B. 会心动，但不会行动
C. 会开始比较当前伴侣和对方
D. 如果当前关系不好，我可能会靠近对方
E. 我觉得有吸引力不代表什么，不会多想
```

---

### Q-EXC-05：不幸福但难分开

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `multi_with_primary` |
| 主要维度 | `relationship_investment`、`breakup_cost_sensitivity`、`staying_due_to_cost` |

题干：

```text
如果一段关系已经不太幸福，你觉得哪些原因会让你仍然很难分开？请选择所有符合项，并标出最主要的一项。
```

选项：

```text
A. 在一起时间很久
B. 共同朋友和社交圈
C. 经济、房租或现实安排
D. 家人已经知道或认可
E. 害怕孤独
F. 不确定还能不能遇到更好的人
G. 对方其实也有很多好
H. 觉得已经投入太多
I. 不想承认关系失败
J. 我通常不太会因为这些留下
```

---

### Q-EXC-06：分手威胁

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `forced_single` |
| 主要维度 | `exit_threat_power`、`fear_of_loss_pattern`、`power_balance_sensitivity` |

题干：

```text
争吵中，如果对方说“不接受就分手”，你通常会怎么反应？
```

选项：

```text
A. 会先判断这是边界还是威胁
B. 会很害怕，可能先让步
C. 会生气，也用分手回应
D. 会冷静下来讨论具体问题
E. 我不能接受用分手威胁解决问题
```

---

### Q-EXC-07：个人空间和关系投入

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `axis_2d` |
| 主要维度 | `freedom_cost`、`relationship_investment_tendency`、`autonomy_need` |

题干：

```text
请分别评估：你愿意为关系投入多少时间？你需要保留多少个人空间？
```

二维坐标：

```text
X 轴：关系时间投入，0 = 很少，100 = 很多
Y 轴：个人空间需求，0 = 很少，100 = 很多
```

---

### Q-EXC-08：被对方需要的感觉

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `forced_single` |
| 主要维度 | `dependence_anxiety`、`neediness_signal`、`relationship_dependence` |

题干：

```text
当你感觉对方很需要你、离不开你时，你通常会怎么感受？
```

选项：

```text
A. 会觉得被重视，很安心
B. 会感到责任和压力
C. 会担心关系不平等
D. 会更有安全感和掌控感
E. 会想保持一点距离
```

---

### Q-EXC-09：关系成本容忍度

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `slider` |
| 主要维度 | `relationship_cost_tolerance`、`emotional_cost`、`practical_cost` |

题干：

```text
如果一段关系给你带来很多现实麻烦或情绪消耗，但也有很强吸引，你能承受多少？
```

滑条：

```text
0 = 很难承受
100 = 只要足够喜欢，我能承受很多
```

---

### Q-EXC-10：关系收益类型

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `multi_with_primary` |
| 主要维度 | `emotional_reward`、`practical_reward`、`romantic_reward`、`growth_reward` |

题干：

```text
你最希望亲密关系给你带来哪些东西？请选择所有符合项，并标出最重要的一项。
```

选项：

```text
A. 情绪支持
B. 稳定陪伴
C. 浪漫和激情
D. 性吸引和亲密
E. 现实协作
F. 共同成长
G. 被理解和被欣赏
H. 家庭或社会认可
I. 安全感
J. 自由和空间
```

---

## 7. 模块四：接近/回避、新鲜感与关系动荡

来源：

```text
docs/design/32_approach_avoidance_turbulence_system.md
```

### Q-TUR-01：接近动机 vs 回避动机

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `axis_2d` |
| 主要维度 | `approach_motivation`、`avoidance_motivation` |

题干：

```text
在关系里，你更重视追求快乐和新鲜感，还是更重视避免冲突和伤害？
```

二维坐标：

```text
X 轴：追求快乐、新鲜、激情和成长，0 = 很低，100 = 很高
Y 轴：避免冲突、伤害、不确定和损失，0 = 很低，100 = 很高
```

---

### Q-TUR-02：安全但沉闷的接受度

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `boredom_sensitivity`、`routine_tolerance`、`safe_but_bored_pattern` |

题干：

```text
如果一段关系很安全、很少吵架，但越来越平淡无聊，你会怎么想？
```

选项：

```text
A. 稳定就很好，平淡可以接受
B. 会有点失落，但可以一起调整
C. 会明显影响我对关系的满意度
D. 会让我更容易被外部新鲜感吸引
E. 我不太能接受长期沉闷
```

---

### Q-TUR-03：高刺激高风险关系吸引力

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `slider` |
| 主要维度 | `risk_excitement_pattern`、`relationship_excitement`、`relationship_safety_need` |

题干：

```text
强烈吸引、强烈波动、经常冲突但也很有激情的关系，对你有多大吸引力？
```

滑条：

```text
0 = 完全不想要
100 = 非常容易被吸引
```

---

### Q-TUR-04：自我延伸需求

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `self_expansion_need`、`shared_growth_level`、`novelty_repair_potential` |

题干：

```text
你希望伴侣关系带给你新的体验、成长或更大的生活可能性吗？
```

选项：

```text
A. 非常希望，这是关系重要价值
B. 比较希望，但稳定也很重要
C. 有当然好，没有也可以
D. 我更希望关系稳定，不需要太多变化
E. 太多变化会让我不安
```

---

### Q-TUR-05：关系动荡期承受度

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `forced_single` |
| 主要维度 | `turbulence_sensitive`、`interdependence_tolerance`、`future_uncertainty_tolerance` |

题干：

```text
关系从暧昧进入正式恋爱后，如果时间安排、朋友关系和个人空间都开始需要调整，你会怎么感受？
```

选项：

```text
A. 这是正常磨合，可以协商
B. 会有压力，但能接受
C. 会担心是不是关系变差了
D. 会想退回原来的轻松状态
E. 会觉得对方影响了我的生活节奏
```

---

### Q-TUR-06：新鲜感修复方式

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `multi_with_primary` |
| 主要维度 | `novelty_repair_potential`、`shared_novelty_need`、`relationship_vitality` |

题干：

```text
如果关系变得平淡，你觉得哪些方式最能让它重新有活力？请选择所有符合项，并标出最重要的一项。
```

选项：

```text
A. 一起尝试新活动
B. 旅行或换环境
C. 更认真地聊天
D. 增加身体亲密
E. 共同设定目标
F. 各自保留空间后再靠近
G. 制造仪式感
H. 解决长期矛盾
I. 我不太知道怎么修复沉闷
J. 平淡不需要修复
```

---

### Q-TUR-07：外部新鲜感拉力

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `slider` |
| 主要维度 | `external_novelty_pull`、`alternative_sensitive`、`boredom_sensitivity` |

题干：

```text
当当前关系变得平淡时，外部新朋友、新圈子或新暧昧对你的吸引会变强多少？
```

滑条：

```text
0 = 几乎不会
100 = 会明显变强
```

---

### Q-TUR-08：稳定日常偏好

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `slider` |
| 主要维度 | `routine_comfort_seeker`、`relationship_safety_need`、`routine_tolerance` |

题干：

```text
固定、熟悉、可预期的相处日常，会让你感到多大程度的安心？
```

滑条：

```text
0 = 容易觉得无聊
100 = 非常安心
```

---

### Q-TUR-09：承诺节奏带来的压力

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `forced_single` |
| 主要维度 | `role_transition_pressure`、`commitment_pacing`、`autonomy_adjustment_pressure` |

题干：

```text
如果对方希望关系快速进入更正式、更绑定的阶段，你会怎么反应？
```

选项：

```text
A. 如果我也喜欢，会愿意推进
B. 会高兴，但也需要一点时间
C. 会有压力，需要确认节奏
D. 会想后退，怕失去自由
E. 会怀疑对方是不是太急
```

---

### Q-TUR-10：蜜月期下降后的判断

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `forced_single` |
| 主要维度 | `honeymoon_decline_belief`、`growth_belief`、`relationship_vitality` |

题干：

```text
如果恋爱初期的强烈甜蜜感下降了，你通常会怎么理解？
```

选项：

```text
A. 正常变化，关系可以进入更稳定阶段
B. 需要主动创造新的连接
C. 会担心是不是不爱了
D. 会觉得关系已经没意思了
E. 会开始观察外部有没有更强吸引
```

---

## 8. 模块五：共有、交换与公平

来源：

```text
docs/design/33_communal_exchange_equity_system.md
```

### Q-EQU-01：共有倾向 vs 交换倾向

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `axis_2d` |
| 主要维度 | `communal_orientation`、`exchange_orientation` |

题干：

```text
在亲密关系中，你更倾向于自然照顾对方需要，还是更在意付出和回报是否匹配？
```

二维坐标：

```text
X 轴：自然照顾对方需要，0 = 很低，100 = 很高
Y 轴：在意付出回报匹配，0 = 很低，100 = 很高
```

---

### Q-EQU-02：短期不对等接受度

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `short_term_imbalance_tolerance`、`long_term_fairness_need` |

题干：

```text
如果伴侣最近状态很差，你需要短期多承担一些照顾、家务或情绪支持，你会怎么想？
```

选项：

```text
A. 可以，只要对方能看见和珍惜
B. 可以，但希望之后有回流
C. 会有压力，需要明确期限
D. 会很快觉得不公平
E. 我不太能接受自己承担更多
```

---

### Q-EQU-03：被理所当然对待

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `taken_for_granted_sensitive`、`felt_appreciation_need` |

题干：

```text
如果你为伴侣做了很多，但对方很少表达感谢或认为这是应该的，你会怎么反应？
```

选项：

```text
A. 会直接说我需要被看见
B. 会有点委屈，但先忍着
C. 会慢慢减少付出
D. 会开始记账，想到自己做了多少
E. 只要对方需要，我不太在意感谢
```

---

### Q-EQU-04：家务公平敏感度

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `slider` |
| 主要维度 | `household_equity_sensitivity`、`emotional_labor_sensitivity` |

题干：

```text
同居或长期相处中，家务、提醒、安排生活细节这些分工公平，对你有多重要？
```

滑条：

```text
0 = 不太重要
100 = 非常重要
```

---

### Q-EQU-05：情绪劳动公平

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `forced_single` |
| 主要维度 | `emotional_labor_sensitivity`、`underbenefit_sensitivity` |

题干：

```text
如果关系里总是你在安慰、解释、缓和气氛和推动修复，你会怎么感受？
```

选项：

```text
A. 可以接受一段时间，但不能长期只有我做
B. 会很累，希望对方也主动承担
C. 会觉得这说明我更成熟
D. 会慢慢失望，减少投入
E. 我通常不太会主动做这些
```

---

### Q-EQU-06：过度获益内疚

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `forced_single` |
| 主要维度 | `overbenefit_guilt_tendency`、`equity_repair_capable` |

题干：

```text
如果你意识到伴侣为你做了很多，而你回报很少，你通常会怎么做？
```

选项：

```text
A. 会表达感谢，并主动补偿或调整
B. 会内疚，但不太知道怎么做
C. 会觉得关系里本来就不用算这么清
D. 会有压力，反而想逃避
E. 如果对方没说，我可能不会注意到
```

---

### Q-EQU-07：开始记账后的处理

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `forced_single` |
| 主要维度 | `scorekeeping_tendency`、`fairness_restoration_drive` |

题干：

```text
当你开始觉得“我为你做了这么多，你为我做了什么”时，你通常会怎么处理？
```

选项：

```text
A. 找机会具体说出哪些地方不平衡
B. 先观察对方会不会主动意识到
C. 会减少自己的付出
D. 会在争吵时一起说出来
E. 会压下去，告诉自己别计较
```

---

### Q-EQU-08：公平不是五五分

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `forced_single` |
| 主要维度 | `perceived_equity`、`long_term_fairness_need` |

题干：

```text
你怎么看亲密关系里的“公平”？
```

选项：

```text
A. 不一定五五分，但长期要都被照顾到
B. 最好尽量平均分担
C. 谁能力强就多承担一些
D. 谁更需要就先照顾谁
E. 如果一直不平均，我会很难接受
```

---

### Q-EQU-09：感激表达需求

| 字段 | 内容 |
| --- | --- |
| 优先级 | P1 |
| 题型 | `slider` |
| 主要维度 | `felt_appreciation_need`、`gratitude_expression` |

题干：

```text
当你为伴侣付出时，你有多需要对方明确表达感谢或看见你的付出？
```

滑条：

```text
0 = 不太需要
100 = 非常需要
```

---

### Q-EQU-10：重新分工意愿

| 字段 | 内容 |
| --- | --- |
| 优先级 | P2 |
| 题型 | `forced_single` |
| 主要维度 | `equity_repair_capable`、`specific_request_clarity` |

题干：

```text
如果你觉得关系里的分工不公平，你更愿意怎么解决？
```

选项：

```text
A. 具体说清楚，希望重新分配
B. 先自己调整，少做一点
C. 等对方主动发现
D. 吵架时再说出来
E. 我通常不知道怎么开口
```

---

## 9. 推荐加入顺序

### 9.1 轻量 4 题包

适合 v0.1.38：

```text
Q-COM-01 自我表露意愿
Q-COM-05 回应性需求
Q-COM-06 哪些事情可以保留不说
Q-COM-10 自己表露 vs 希望对方表露
```

### 9.2 40 题快速扩展包

在 25 题基础上扩到约 40 题，可加入：

```text
Q-CON-01 被指出问题时的第一反应
Q-CON-05 暂停争吵方式
Q-EXC-01 关系期待水平
Q-EXC-03 替代选择意识
Q-TUR-02 安全但沉闷的接受度
Q-TUR-03 高刺激高风险关系吸引力
Q-EQU-02 短期不对等接受度
Q-EQU-03 被理所当然对待
Q-EQU-04 家务公平敏感度
Q-EQU-09 感激表达需求
```

### 9.3 60 题标准扩展包

可继续加入：

```text
Q-COM-02 表露内容范围
Q-COM-03 表露节奏
Q-COM-04 表露互惠需求
Q-COM-07 对方保留秘密时的反应
Q-COM-09 爱意表达需求
Q-CON-02 争吵中是否打断
Q-CON-03 是否容易翻旧账
Q-CON-04 第一人称表达能力
Q-CON-06 道歉后的行动
Q-CON-09 对方哭或崩溃时的反应
Q-EXC-04 遇到有吸引力的新对象
Q-EXC-05 不幸福但难分开
Q-TUR-01 接近动机 vs 回避动机
Q-TUR-04 自我延伸需求
Q-EQU-01 共有倾向 vs 交换倾向
```

---

## 10. 计分接入提醒

后续真正加入 `questionnaire_mvp.json` 时必须同步检查：

```text
1. 题目 ID 不冲突
2. selection_mode 被 runner 支持
3. dimensions 存在或已在 128维/扩展维度中定义
4. scoring.dimension_effects 完整
5. loader 测试更新题目数量
6. scoring 测试覆盖新增题型
7. reporting 能解释新增维度
8. runner 能正确输入和错误重试
9. scripts/check_questionnaire_dimension_ids.py 通过
```

---

## 11. 不做什么

本候选池暂不做：

1. 不直接修改 `if_game/data/questionnaire_mvp.json`；
2. 不强行一次加入全部 50 题；
3. 不引入当前 runner 不支持的题型；
4. 不输出诊断式标签；
5. 不把单题答案当成人格定论；
6. 不接 AI API；
7. 不上传原始截图或大段原文。

---

## 12. 一句话总结

```text
本候选池的作用，是把 IF 新增关系系统转成后续可小批量接入的问卷题目；当前只做沉淀，不直接改变 MVP 运行逻辑。
```

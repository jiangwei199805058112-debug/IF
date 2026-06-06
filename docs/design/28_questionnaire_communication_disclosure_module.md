# 前期调查：沟通、自我表露与秘密边界模块设计

本文档用于把 `docs/design/27_communication_self_disclosure_system.md` 中的沟通、自我表露、回应性、秘密边界和禁忌话题机制转化为前期问卷模块。它不是立即修改 `if_game/data/questionnaire_mvp.json` 的执行方案，而是为后续扩展快速版、标准版或深度版问卷提供题目结构、维度字段和计分方向。

核心原则：

```text
前期调查要测的不是“这个人会不会聊天”，而是：
他平常愿意表露多少、说到多深、什么时候说、希望对方如何回应、能接受对方保留多少，以及哪些话题在他看来必须坦白。
```

---

## 1. 设计目的

IF 的前期调查已经能覆盖关系入口、依恋、信任、隐瞒、冲突、边界和修复等内容。后续应增加一个独立模块：

```text
沟通与自我表露模块
```

该模块用于回答：

1. 玩家平常愿不愿意说真实想法；
2. 玩家能说到多深；
3. 玩家是慢慢说，还是很早就说很多；
4. 玩家是否要求对方也同等开放；
5. 玩家说出脆弱内容后需要怎样的回应；
6. 玩家认为哪些事情是隐私，哪些事情必须坦白；
7. 玩家能否让对方敞开心扉；
8. 玩家对秘密、前任、手机、金钱、性边界、家庭矛盾等话题的容忍度。

---

## 2. 需要新增或补强的维度字段

| 字段 ID | 含义 | 主要用途 |
| --- | --- | --- |
| `self_disclosure_willingness` | 自我表露意愿 | 判断玩家是否愿意主动说真实想法、经历和脆弱点 |
| `disclosure_depth` | 表露深度 | 判断玩家通常只说表层信息，还是愿意进入家庭、前任、创伤、欲望等深层内容 |
| `disclosure_breadth` | 表露广度 | 判断玩家愿意谈论的话题范围 |
| `disclosure_pacing` | 表露节奏 | 判断玩家是过快表露、自然推进、对方先说才说，还是长期不说 |
| `over_disclosure_risk` | 过快表露风险 | 用于处理关系早期说太深导致对方压力上升 |
| `under_disclosure_gap` | 低表露距离 | 用于处理长期不表露造成的猜测、疏远和不安全感 |
| `reciprocal_disclosure_need` | 表露互惠需求 | 判断玩家是否需要对方也说同等程度的私人信息 |
| `perceived_responsiveness_need` | 回应性需求 | 判断玩家说出脆弱后需要倾听、安慰、分析还是空间 |
| `emotional_validation_need` | 情绪确认需求 | 判断对方敷衍或否定时的伤害程度 |
| `privacy_boundary_strength` | 隐私边界强度 | 判断玩家能接受自己和对方保留多少隐私 |
| `secret_tolerance` | 秘密容忍度 | 判断玩家对伴侣保留秘密的接受程度 |
| `taboo_topic_avoidance` | 禁忌话题回避 | 判断玩家是否回避前任、金钱、家庭、性边界、承诺等敏感话题 |
| `partner_disclosure_expectation` | 伴侣表露期待 | 判断玩家希望对方告诉自己多少私人事情 |
| `opener_skill` | 开启者能力 | 判断玩家是否容易让别人敞开心扉 |
| `listening_quality` | 倾听质量 | 判断玩家在对方表露时是否能接住 |
| `verbal_affection_need` | 语言爱意需求 | 判断玩家是否需要对方清楚表达喜欢、在乎和承诺 |
| `words_actions_consistency_sensitivity` | 言行一致敏感度 | 判断玩家是否特别在意对方说了但没做到 |

---

## 3. 建议题型设计

本模块不适合全部做强制单选。建议混合使用：

| 题型 | 用途 |
| --- | --- |
| `forced_single` | 测主要倾向，如表露节奏、回应偏好 |
| `multi_with_primary` | 测可谈话题、可保留隐私、禁忌话题 |
| `primary_with_secondary` | 测主要需求和次要需求，如安慰 vs 解决方案 |
| `slider` | 测希望对方透明到什么程度 |
| `axis_2d` | 测“自己表露多少 × 希望对方表露多少”的不对称性 |
| `confidence` 扩展 | 测玩家对自述是否确定，后续可与游戏行为校验 |

---

## 4. 核心问题组

### Q-COM-01：自我表露意愿

**题干：**

当关系逐渐亲近后，你愿意主动说出自己的不安、过去经历或真实需求吗？

**题型：** `forced_single`

| 选项 | 倾向 |
| --- | --- |
| A. 基本不会，除非被问到 | 低表露 |
| B. 会说一部分，但会保留很多 | 中低表露 |
| C. 看对方反应，如果安全才说 | 条件表露 |
| D. 会主动分享重要经历和情绪 | 高表露 |
| E. 很容易一开始就说很多 | 过快表露风险 |

**主要影响：**

```text
self_disclosure_willingness
disclosure_pacing
over_disclosure_risk
under_disclosure_gap
```

---

### Q-COM-02：通常会说哪些内容

**题干：**

在亲密关系中，你通常会把哪些内容告诉对方？请选择所有符合项，并标出最主要的一类。

**题型：** `multi_with_primary`

| 选项 | 说明 |
| --- | --- |
| A. 日常生活 | 浅层表露 |
| B. 兴趣爱好 | 浅层表露 |
| C. 工作/学习压力 | 中层表露 |
| D. 家庭关系 | 中层表露 |
| E. 前任经历 | 中深层表露 |
| F. 自卑或脆弱 | 深层表露 |
| G. 金钱压力 | 深层现实表露 |
| H. 性、欲望或边界 | 深层亲密表露 |
| I. 做错过的事 | 深层道德表露 |
| J. 几乎不说深层内容 | 低深度表露 |

**主要影响：**

```text
disclosure_breadth
disclosure_depth
taboo_topic_avoidance
privacy_boundary_strength
```

---

### Q-COM-03：表露节奏

**题干：**

如果你刚和一个人关系升温，你会多久开始说比较私人的事情？

**题型：** `forced_single`

| 选项 | 倾向 |
| --- | --- |
| A. 很早，只要聊得来就说 | 过快表露风险 |
| B. 关系明显稳定后才说 | 稳定节奏 |
| C. 对方先说，我才跟着说 | 互惠依赖 |
| D. 很久也不太说 | 回避深层暴露 |
| E. 只有吵架或崩溃时才说 | 压力型表露 |

**主要影响：**

```text
disclosure_pacing
over_disclosure_risk
pressure_disclosure_pattern
reciprocal_disclosure_need
```

---

### Q-COM-04：表露互惠需求

**题干：**

如果你向对方说了一个比较私人的事情，而对方很少说自己的事，你通常会怎么想？

**题型：** `forced_single`

| 选项 | 倾向 |
| --- | --- |
| A. 没关系，每个人节奏不同 | 高包容 |
| B. 会有点失落，但能接受 | 中等互惠需求 |
| C. 会觉得不公平，好像只有我在暴露 | 互惠需求高 |
| D. 会怀疑对方不信任我 | 信任敏感 |
| E. 我本来也不想说太多 | 低表露需求 |

**主要影响：**

```text
reciprocal_disclosure_need
disclosure_balance
partner_disclosure_expectation
trust_sensitivity
```

---

### Q-COM-05：回应性需求

**题干：**

当你说出一件让你难过或不安的事时，你最希望对方怎么回应？

**题型：** `primary_with_secondary`

| 选项 | 倾向 |
| --- | --- |
| A. 认真听，不急着评价 | 倾听需求 |
| B. 给我明确安慰和陪伴 | 安抚需求 |
| C. 帮我分析解决办法 | 问题解决导向 |
| D. 只要别嘲笑我就行 | 低期待或防御 |
| E. 也分享他/她的类似经历 | 互惠表露需求 |
| F. 不希望对方追问太多 | 隐私边界高 |

**主要影响：**

```text
perceived_responsiveness_need
emotional_validation_need
privacy_boundary_strength
reciprocal_disclosure_need
```

---

### Q-COM-06：哪些事情可以保留不说

**题干：**

恋爱后，你认为哪些事情可以保留不说？请选择所有符合项，并标出你最坚持的一项。

**题型：** `multi_with_primary`

| 选项 | 说明 |
| --- | --- |
| A. 和前任是否还有联系 | 前任边界 |
| B. 过去恋爱经历细节 | 过去隐私 |
| C. 手机聊天内容 | 数字隐私 |
| D. 金钱情况 | 现实压力隐私 |
| E. 家庭矛盾 | 家庭隐私 |
| F. 曾经做错的事 | 道德秘密 |
| G. 当前异性朋友情况 | 异性边界 |
| H. 心里对关系的不满 | 关系真实想法 |
| I. 性、欲望相关想法 | 亲密隐私 |
| J. 基本都应该坦白 | 高透明期待 |

**主要影响：**

```text
privacy_boundary_strength
secret_tolerance
partner_disclosure_expectation
taboo_topic_avoidance
```

---

### Q-COM-07：对方保留秘密时的反应

**题干：**

如果对方说“有些事我想自己保留”，你通常会怎么反应？

**题型：** `forced_single`

| 选项 | 倾向 |
| --- | --- |
| A. 能尊重，只要不伤害关系 | 隐私尊重 |
| B. 会接受，但心里有点不安 | 轻度不安 |
| C. 会想知道到底是什么 | 追问倾向 |
| D. 会觉得对方不信任我 | 信任敏感 |
| E. 如果是亲密关系，就不该有秘密 | 高透明要求 |

**主要影响：**

```text
secret_tolerance
privacy_boundary_respect
partner_disclosure_expectation
relationship_threat_sensitivity
```

---

### Q-COM-08：开启者能力

**题干：**

别人是否经常愿意告诉你他们自己的私事或真实感受？

**题型：** `forced_single`

| 选项 | 倾向 |
| --- | --- |
| A. 很少，别人通常不太跟我说深层内容 | 开启者能力低 |
| B. 偶尔会，看关系和情境 | 中等 |
| C. 比较常见，朋友会找我倾诉 | 开启者能力较高 |
| D. 很多人会说我让他们放松 | 开启者能力高 |
| E. 我不太喜欢别人对我说太多 | 低接纳或高边界 |

**主要影响：**

```text
opener_skill
listening_quality
emotional_safety_signal
privacy_boundary_strength
```

---

### Q-COM-09：爱意表达需求

**题干：**

在亲密关系中，你需要对方清楚说出喜欢、在乎或爱吗？

**题型：** `forced_single`

| 选项 | 倾向 |
| --- | --- |
| A. 很需要，不说我会不安 | 高语言爱意需求 |
| B. 比较需要，偶尔明确表达就好 | 中高需求 |
| C. 行动更重要，说不说都可以 | 行动优先 |
| D. 我自己也不太习惯说这些 | 低语言表达 |
| E. 说太多反而让我觉得不真实 | 空话敏感 |

**主要影响：**

```text
verbal_affection_need
words_actions_consistency_sensitivity
reassurance_dependency
low_verbal_affection
```

---

### Q-COM-10：自己表露 vs 希望对方表露

**题干：**

请分别评估：你通常愿意向对方表露多少私人内容？你希望对方向你表露多少私人内容？

**题型：** `axis_2d`

- X 轴：自己表露程度，0 = 几乎不说，100 = 很多都愿意说；
- Y 轴：希望对方表露程度，0 = 对方可以保留很多，100 = 希望对方尽量坦白。

**主要影响：**

```text
self_disclosure_willingness
partner_disclosure_expectation
disclosure_asymmetry
transparency_double_standard_risk
```

**判定方向：**

| X/Y 状态 | 解释 |
| --- | --- |
| 自己高，对方高 | 高互相透明倾向 |
| 自己低，对方低 | 高隐私边界倾向 |
| 自己低，对方高 | 不对称透明 / 双标风险 |
| 自己高，对方低 | 容易感到对方不开放 |

---

## 5. 模块输出建议

问卷报告中可生成以下摘要：

```text
你的沟通与自我表露倾向：
- 你通常愿意说到什么程度；
- 你是否需要对方也同样开放；
- 你对隐私和秘密的边界；
- 你在脆弱表达后最需要的回应；
- 你可能适合怎样的沟通节奏。
```

### 5.1 可见标签

| 标签 ID | 说明 |
| --- | --- |
| `guarded_discloser` | 谨慎表露者 |
| `deep_discloser` | 深层表露者 |
| `fast_disclosure_pattern` | 快速表露模式 |
| `reciprocity_sensitive` | 表露互惠敏感 |
| `privacy_protective` | 隐私保护强 |
| `high_transparency_expectation` | 高透明期待 |
| `opener_type` | 开启者 |
| `high_responsiveness_need` | 高回应需求 |
| `low_verbal_affection` | 低语言爱意表达 |
| `words_actions_gap_sensitive` | 言行一致敏感 |

### 5.2 风险标签

| 标签 ID | 说明 |
| --- | --- |
| `over_disclosure_risk` | 关系早期过快表露可能给对方压力 |
| `under_disclosure_gap` | 长期低表露可能造成距离感 |
| `transparency_double_standard_risk` | 自己保留较多但要求对方透明 |
| `taboo_avoidance_risk` | 长期回避重要话题 |
| `forced_disclosure_damage_risk` | 被逼问或被发现后才说，信任损伤更大 |

---

## 6. 与游戏事件的接口

本模块问卷结果应影响以下事件：

| 事件 | 受影响字段 |
| --- | --- |
| 第一次谈过去伤害 | `disclosure_depth`、`perceived_responsiveness_need` |
| 对方问私人问题 | `privacy_boundary_strength`、`taboo_topic_avoidance` |
| 一方说很多，另一方很少说 | `reciprocal_disclosure_need`、`partner_disclosure_expectation` |
| 对方不愿谈前任 | `secret_tolerance`、`privacy_boundary_respect` |
| 手机隐私冲突 | `privacy_boundary_strength`、`partner_disclosure_expectation` |
| 说“我爱你”后对方沉默 | `verbal_affection_need`、`reassurance_dependency` |
| 对方拿你的脆弱攻击你 | `disclosure_regret`、`old_wound_memory` |
| 对方认真接住你的表露 | `safe_disclosure_space`、`vulnerability_trust_gain` |

---

## 7. 与现有 128 维和题库的关系

当前 128 维主表已覆盖冲突、边界、信任、信息管理、依恋等大类。该模块可作为后续补题方向，优先补充或映射到：

```text
信息管理
信任与怀疑
边界
冲突沟通
依恋与亲密
数字生活
现实压力
```

如果未来 128 维扩展到 160 维，可以新增或拆出：

```text
self_disclosure_willingness
reciprocal_disclosure_need
perceived_responsiveness_need
privacy_boundary_strength
partner_disclosure_expectation
opener_skill
verbal_affection_need
```

---

## 8. 与现有 MVP 的关系

当前 `if_game/data/questionnaire_mvp.json` 已经从 Q001-Q030 扩展为 25 题快速版。本文档暂不要求立即修改 MVP JSON。

建议后续顺序：

1. 先保留当前 25 题快速版稳定运行；
2. 等需要扩展到标准版或 40-60 题版本时，再加入本模块题目；
3. 若只想轻量加入，可优先加入 Q-COM-01、Q-COM-05、Q-COM-06、Q-COM-10 四题；
4. 新增题目后必须同步更新 loader、scoring、reporting、runner 测试。

---

## 9. 不做什么

本模块不做：

1. 不把高表露等同于关系能力强；
2. 不把低表露等同于冷漠；
3. 不把隐私边界强等同于有问题；
4. 不把希望对方坦白等同于控制欲；
5. 不用单题判定双标；
6. 不直接修改当前 25 题 MVP；
7. 不接 AI API；
8. 不做心理诊断。

---

## 10. 一句话总结

```text
沟通与自我表露模块要测的不是“玩家话多不多”，而是：
玩家如何管理真实信息的开放程度、如何期待对方回应、如何划定隐私边界，以及这种模式会怎样影响 IF 中的信任、亲密和冲突。
```

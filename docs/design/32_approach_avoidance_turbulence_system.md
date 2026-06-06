# 接近/回避动机、关系沉闷与关系动荡系统设计

本文档用于沉淀 IF 项目中的接近动机、回避动机、奖赏与代价的独立作用、关系沉闷、关系动荡和长期满意度轨迹。它对 `docs/design/30_social_exchange_dependency_system.md` 形成补充：社会交换系统可以用“奖赏-代价”作为概念入口，但后续实现时不能把奖赏和代价简单写成一条轴线的正反面。

核心原则：

```text
亲密关系中的快乐和痛苦不是同一枚硬币的两面。
接近奖赏和回避代价是两套相对独立的动机系统：
一段关系可以快乐但有风险，也可以安全但沉闷，也可以痛苦又不稳定，也可以既有奖赏又能降低代价。
```

本设计参考亲密关系中的接近动机、回避动机、自我延伸、关系沉闷、关系动荡、相互依赖调整和长期满意度轨迹等观点，并转译为 IF 的系统机制。本文档不收录原始截图或长篇原文，只保留可供项目使用的变量、事件模板、报告标签和落地边界。

---

## 1. 设计目的

`30_social_exchange_dependency_system.md` 已经定义了：

```text
relationship_outcome = rewards - costs
relationship_satisfaction = relationship_outcome - comparison_level
relationship_dependence = relationship_outcome - comparison_level_alternatives + investment_weight + leaving_cost_weight
```

这个公式适合作为概念入口，但它有一个实现风险：后续代码可能把“奖赏”和“代价”简单做成同一轴线的正负两端。

本文件补充一个更细的规则：

```text
追求奖赏 approach motivation
避免代价 avoidance motivation
```

两者不是完全相反的同一变量，而是两套可以同时高、同时低、相互错位的动机系统。

---

## 2. 系统一：接近动机与回避动机

### 2.1 设计原则

接近动机驱动角色追求快乐、亲密、新鲜感、性吸引、共同成长、被欣赏和自我扩展。

回避动机驱动角色避开冲突、痛苦、羞辱、焦虑、失控、被拒绝、背叛、损失和关系威胁。

两者可以同时存在。

例子：

```text
我很喜欢和他/她在一起，很有激情。
但这段关系也让我很不安，争吵很多。
```

这是：

```text
高接近奖赏 + 高回避代价压力
```

再如：

```text
这段关系很安全，几乎没有冲突。
但我觉得越来越无聊，没有新鲜感。
```

这是：

```text
低代价 + 低接近奖赏
```

### 2.2 核心变量

| 变量 ID | 含义 |
| --- | --- |
| `approach_motivation` | 追求亲密、快乐、新鲜和自我扩展的动机 |
| `avoidance_motivation` | 回避痛苦、冲突、拒绝和损失的动机 |
| `approach_reward_level` | 关系中积极奖赏的丰富程度 |
| `avoidance_cost_pressure` | 关系中需要回避的痛苦和威胁强度 |
| `positive_event_density` | 正向事件密度，如约会、惊喜、共笑、亲密体验 |
| `negative_event_density` | 负向事件密度，如争吵、冷淡、怀疑、羞辱 |
| `relationship_excitement` | 关系兴奋度和活力 |
| `relationship_safety` | 关系安全感和稳定感 |
| `relationship_stagnation` | 关系停滞和沉闷 |
| `risk_excitement_mix` | 高奖赏和高风险并存的刺激关系 |

---

## 3. 四象限关系体验

接近奖赏和回避代价可以形成四象限。

| 接近奖赏 | 回避代价压力 | 关系体验 | IF 表达 |
| --- | --- | --- | --- |
| 高 | 低 | 丰盛关系 | 快乐、亲密、安全、活力兼具 |
| 高 | 高 | 高刺激高风险关系 | 激情强、波动大、容易上瘾也容易受伤 |
| 低 | 低 | 安全但沉闷关系 | 稳定、不太痛苦，但缺乏乐趣和自我扩展 |
| 低 | 高 | 痛苦关系 | 奖赏少、代价高，容易疲惫和想逃 |

这与 `30` 文档的“幸福/不幸福、稳定/不稳定”不是冲突，而是补充：

```text
30 关注：满意度、依赖度、替代选择和稳定性。
32 关注：快乐与痛苦是否同时存在，以及关系是否有活力、沉闷或高风险刺激。
```

---

## 4. 系统二：关系沉闷与自我延伸

### 4.1 设计原则

关系不只需要少冲突，也需要正向奖赏、共同新鲜感和自我延伸。长期稳定但缺少新奇、共同成长和积极体验的关系，可能进入沉闷。

沉闷不等于关系坏，也不等于一定要分开，但它会降低接近动机，让人更容易被替代选择、外部新鲜感和自我扩展机会吸引。

### 4.2 核心变量

| 变量 ID | 含义 |
| --- | --- |
| `self_expansion_need` | 通过亲密关系扩展兴趣、经验、身份和能力的需求 |
| `shared_novelty_level` | 共同新鲜体验水平 |
| `shared_growth_level` | 双方共同成长水平 |
| `routine_saturation` | 日常重复导致的饱和感 |
| `boredom_accumulation` | 沉闷累积 |
| `novelty_repair_potential` | 通过新活动、新话题、新目标修复沉闷的潜力 |
| `external_novelty_pull` | 外部新鲜感吸引 |
| `relationship_vitality` | 关系活力 |

### 4.3 事件模板

事件：两个人已经很少吵架，但也很少有新的共同体验。

系统判断：

- `relationship_safety` 是否高；
- `shared_novelty_level` 是否低；
- `boredom_accumulation` 是否上升；
- `self_expansion_need` 是否高；
- 是否出现外部新鲜对象或新生活机会；
- 双方是否愿意主动创造共同体验。

可能结果：

| 反应 | 效果 |
| --- | --- |
| 双方尝试新活动、新旅行、新共同目标 | 活力恢复，接近奖赏上升 |
| 一方觉得“稳定就够了” | 对高自我延伸需求者不够 |
| 一方在外部寻找新鲜感 | 替代选择吸引上升 |
| 双方长期不处理沉闷 | 满意度缓慢下降 |

---

## 5. 系统三：关系动荡与相互依赖调整

### 5.1 设计原则

亲密关系开始阶段往往有快速满意度上升，但随着双方相互依赖增加，生活安排、朋友时间、习惯、边界和未来不确定性都需要重新协调。这个阶段可能出现关系动荡。

关系动荡不一定代表关系失败，它可能是从随意约会过渡到严肃投入的调整期。

### 5.2 核心变量

| 变量 ID | 含义 |
| --- | --- |
| `relationship_turbulence` | 关系动荡程度 |
| `interdependence_growth` | 相互依赖增长速度 |
| `routine_disruption` | 生活常规被关系打断的程度 |
| `autonomy_adjustment_pressure` | 自主权调整压力 |
| `friend_network_friction` | 朋友和外部社交阻力 |
| `future_uncertainty` | 对关系未来方向的不确定 |
| `role_transition_pressure` | 从暧昧/约会转入伴侣身份的压力 |
| `coordination_load` | 时间、计划、边界、生活安排的协调负荷 |
| `turbulence_repair_success` | 动荡期是否成功调整 |

### 5.3 游戏表现

关系早期可能表现为：

```text
满意度快速上升 → 进入动荡平台期 → 双方调整成功后重新上升
```

这解释了：

- 刚开始很甜，后来突然摩擦增多；
- 对方占用了太多时间，朋友开始有意见；
- 一方期待周末一起待在家，另一方期待外出约会；
- 双方都喜欢彼此，但不知道未来怎么安排；
- 不是不爱，而是相互依赖突然增加带来适应压力。

### 5.4 事件模板

事件：关系变亲密后，玩家发现自己的朋友时间被大量占用。

可能结果：

| 处理方式 | 效果 |
| --- | --- |
| 双方协商固定伴侣时间和个人时间 | 动荡下降，稳定性上升 |
| 一方认为“谈恋爱就该多陪我” | 自主压力和冲突上升 |
| 一方偷偷减少见面或冷淡 | 解释危机和信任波动 |
| 双方都不说，但开始觉得累 | 满意度缓慢下降 |

---

## 6. 系统四：长期满意度轨迹

### 6.1 设计原则

关系满意度不应设计成线性增长，也不应默认“时间越久越差”。更适合 IF 的做法是设计多种轨迹。

### 6.2 可用轨迹

| 轨迹 ID | 含义 | 游戏表现 |
| --- | --- | --- |
| `honeymoon_decline` | 蜜月期后逐渐下降 | 初期很甜，随后新鲜感下降、现实摩擦增加 |
| `turbulence_then_growth` | 动荡后成长 | 初期上升，中期波动，调整成功后更稳定 |
| `stable_high_satisfaction` | 长期高满意 | 有稳定正向互动、修复能力和共同成长 |
| `stable_low_satisfaction` | 长期低满意 | 不一定分开，但长期沉闷或不满 |
| `volatile_high_reward_high_cost` | 高奖赏高代价波动 | 强激情、高冲突、强吸引也强消耗 |
| `slow_burn_growth` | 缓慢升温 | 初期不强烈，但随着理解和信任增长而变好 |

### 6.3 关键修正

不要写成：

```text
关系时间越长 → 满意度自动下降
```

应写成：

```text
关系时间增长会提高相互依赖、协调负荷和沉闷风险，
但如果正向奖赏、修复能力、自我延伸和共同成长足够，满意度可以稳定或再次上升。
```

---

## 7. 与 30 号文档的修正关系

`30_social_exchange_dependency_system.md` 中的 `relationship_outcome = rewards - costs` 仍可保留为总括公式，但实现时应按以下方式拆分：

```text
approach_reward_level：关系带来多少正向奖赏
avoidance_cost_pressure：关系带来多少痛苦、威胁和代价
relationship_outcome：两者综合后的总体结果
```

不要把“没有痛苦”直接等同于“有快乐”，也不要把“有快乐”直接等同于“安全”。

统一修正口径：

| 状态 | 正确理解 |
| --- | --- |
| 高奖赏低代价 | 丰盛关系，既快乐又安全 |
| 高奖赏高代价 | 高刺激高风险，可能强吸引也强消耗 |
| 低奖赏低代价 | 安全但沉闷，稳定但不一定满足 |
| 低奖赏高代价 | 痛苦关系，既无足够奖赏又有高负担 |

---

## 8. 与现有系统的关系

本系统与以下文档直接关联：

```text
docs/design/25_attribution_memory_belief_system.md
docs/design/26_partner_perception_and_impression_system.md
docs/design/27_communication_self_disclosure_system.md
docs/design/29_conflict_communication_repair_system.md
docs/design/30_social_exchange_dependency_system.md
docs/design/31_system_integration_consistency_rules.md
```

其中：

- 25 判断行为如何被解释；
- 26 判断伴侣认知是否准确；
- 27 判断双方如何交换真实信息；
- 29 判断冲突如何升级或修复；
- 30 判断满意、依赖、替代选择和权力；
- 31 防止系统重复扣分和逻辑打架；
- 32 判断关系是否有快乐、是否有痛苦、是否沉闷、是否经历动荡。

---

## 9. 前期问卷可补字段

后续如果扩展问卷，可以加入以下维度：

```text
approach_motivation
avoidance_motivation
self_expansion_need
shared_novelty_need
relationship_safety_need
boredom_sensitivity
routine_tolerance
external_novelty_pull
interdependence_tolerance
autonomy_need
future_uncertainty_tolerance
```

这些字段可用于判断玩家：

- 是否追求激情、新鲜感和共同成长；
- 是否更重视安全、少冲突和低风险；
- 是否容易被沉闷消耗；
- 是否能承受关系早期的动荡和协调；
- 是否在高奖赏高风险关系里容易上瘾；
- 是否在低代价低奖赏关系里逐渐失去热情。

---

## 10. 报告标签设计

| 标签 ID | 含义 | 报告表达方向 |
| --- | --- | --- |
| `high_approach_motivation` | 高接近动机 | 更需要快乐、新鲜感、亲密和共同成长 |
| `high_avoidance_motivation` | 高回避动机 | 更重视避免冲突、伤害和不确定性 |
| `risk_excitement_pattern` | 高刺激高风险 | 容易被强烈关系吸引，但也更容易受伤和消耗 |
| `safe_but_bored_pattern` | 安全但沉闷 | 低冲突不代表高满足，可能需要共同新鲜体验 |
| `self_expansion_seeker` | 自我延伸需求高 | 需要关系带来成长、探索和新体验 |
| `routine_comfort_seeker` | 稳定日常偏好 | 更能从规律、熟悉和低风险中获得安全感 |
| `turbulence_sensitive` | 动荡敏感 | 关系早期的相互依赖调整容易带来压力 |
| `novelty_repair_potential` | 新鲜感修复潜力 | 可通过新活动、新目标和共同挑战改善沉闷 |

---

## 11. 事件库方向

后续可以设计以下事件：

1. 关系很安全，但玩家觉得越来越无聊；
2. 双方尝试新的共同活动，关系活力上升；
3. 玩家被高刺激但高风险的人吸引；
4. 恋爱后朋友抱怨玩家消失太久；
5. 一方想周末在家，另一方想外出约会；
6. 关系从暧昧转正式后，时间安排开始混乱；
7. 蜜月期后对方不再每天制造惊喜；
8. 双方经历动荡后建立新的相处节奏；
9. 一方只想避免吵架，另一方想追求更多亲密和热情；
10. 长期稳定伴侣通过共同目标重新找回活力。

---

## 12. 不做什么

本系统暂不做：

1. 不把高刺激关系写成一定坏；
2. 不把低冲突关系写成一定好；
3. 不把沉闷直接等同于不爱；
4. 不把新鲜感需求直接等同于花心；
5. 不把关系动荡直接等同于关系失败；
6. 不把蜜月期下降写成必然结局；
7. 不接 AI API；
8. 不上传原始截图或大段原文。

---

## 13. 一句话总结

```text
IF 的接近/回避系统要模拟的不是“奖赏多还是代价多”这一条线，
而是：关系是否同时提供快乐和安全，是否陷入沉闷或高风险刺激，以及伴侣能否在相互依赖增长带来的动荡期中重新找到稳定而有活力的相处方式。
```

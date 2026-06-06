# 关系状态聚合器实施方案

本文档用于把 `docs/design/25_attribution_memory_belief_system.md` 到 `docs/design/33_communal_exchange_equity_system.md` 的关系系统收束为一个后续可编码的统一结算层：

```text
relationship_state_aggregator
```

它不是新增剧情系统，也不是新的心理理论文档，而是后续实现时用于统一汇总关系事件影响、防止重复扣分、防止系统互相打架的实施方案。

核心原则：

```text
25-33 号文档不应被实现成多套各自改数值的独立系统。
它们应当共同向 relationship_state_aggregator 提供证据、解释和修正因子，
由聚合器统一结算信任、满意度、亲密感、依赖度、稳定性、旧伤记忆和报告标签。
```

---

## 1. 目标

`relationship_state_aggregator` 的目标是统一回答一个问题：

```text
一次关系事件发生后，玩家和 NPC 的关系状态到底应该如何变化？
```

它需要接收来自多个系统的结果：

- 真实原因层；
- 可见线索层；
- 伴侣认知层；
- 归因解释层；
- 自我表露与回应性层；
- 冲突沟通与修复层；
- 社会交换层；
- 接近/回避动机层；
- 共有/交换/公平层。

然后统一输出：

```text
trust_delta
satisfaction_delta
intimacy_delta
dependence_delta
stability_delta
old_wound_memory_delta
repair_chance_delta
report_tags
```

聚合器的主要价值不是增加复杂度，而是减少混乱：

```text
同一事件只能被统一结算一次，不能被每个子系统各扣一次。
```

---

## 2. 不做什么

本实施方案暂不做：

1. 不直接实现完整代码；
2. 不接 AI API；
3. 不修改现有问卷 JSON；
4. 不重写 14 天主流程；
5. 不替代 `relationship_interpretation.py`；
6. 不让每个子系统直接修改最终关系值；
7. 不把心理概念直接等同于数值扣分；
8. 不做心理诊断；
9. 不上传原始截图或长篇原文。

---

## 3. 总体数据流

建议后续代码采用以下顺序：

```text
RelationshipEvent
    ↓
truth_layer_result
    ↓
observable_evidence_result
    ↓
interpretation_result
    ↓
communication_result
    ↓
conflict_repair_result
    ↓
exchange_dependency_result
    ↓
approach_avoidance_result
    ↓
equity_communal_result
    ↓
relationship_state_aggregator
    ↓
RelationshipStateDelta
```

其中，子系统只负责提供“解释材料”和“局部影响建议”，最终由聚合器统一合并。

---

## 4. 输入结构草案

### 4.1 顶层输入

后续可定义一个轻量输入结构：

```python
@dataclass
class AggregatorInput:
    event_id: str
    actor_id: str
    target_id: str
    event_type: str
    truth: TruthLayerResult | None = None
    evidence: EvidenceResult | None = None
    interpretation: InterpretationResult | None = None
    communication: CommunicationResult | None = None
    conflict: ConflictRepairResult | None = None
    exchange: ExchangeDependencyResult | None = None
    approach_avoidance: ApproachAvoidanceResult | None = None
    equity: EquityResult | None = None
    current_state: RelationshipStateSnapshot | None = None
```

MVP 阶段不必一次实现所有字段。可以先用 `dict` 或简单 dataclass，避免过度工程化。

---

### 4.2 真实原因输入

来源：`25_attribution_memory_belief_system.md` 与当前 `relationship_interpretation.py`。

```python
@dataclass
class TruthLayerResult:
    truth_type: str
    truth_reason: str
    truth_intention: str
    truth_harm_level: int
    deception_level: int = 0
    boundary_violation_level: int = 0
```

用途：

- 判断事实信任损失；
- 判断是否写入旧伤；
- 判断怀疑是否准确；
- 判断解释是否只是误会。

---

### 4.3 证据与可见线索输入

```python
@dataclass
class EvidenceResult:
    evidence_chain_strength: int
    observable_trace_count: int
    behavior_explanation_gap: int
    explanation_consistency: int
    deleted_or_hidden_trace: bool = False
```

用途：

- 调整怀疑准确度；
- 调整解释可信度；
- 区分“焦虑误会”和“准确警觉”；
- 避免无证据时过度扣信任。

---

### 4.4 解释与认知输入

来源：`26_partner_perception_and_impression_system.md`。

```python
@dataclass
class InterpretationResult:
    interpretation_type: str
    interpretation_accuracy: str
    partner_model_confidence: int
    partner_model_accuracy: int
    projection_bias_effect: int = 0
    threat_bias_effect: int = 0
    selective_blindness_effect: int = 0
    report_tags: list[str] = field(default_factory=list)
```

用途：

- 生成报告标签；
- 判断玩家/NPC 是准确警觉、自信误读、选择性忽视还是稳定信任；
- 不直接大幅修改信任，只作为结算修正因子。

---

### 4.5 沟通与表露输入

来源：`27_communication_self_disclosure_system.md` 和 `28_questionnaire_communication_disclosure_module.md`。

```python
@dataclass
class CommunicationResult:
    disclosure_depth: int = 0
    disclosure_pacing_risk: int = 0
    perceived_responsiveness: int = 0
    emotional_validation: int = 0
    privacy_boundary_conflict: int = 0
    secret_damage_level: int = 0
    safe_disclosure_space_delta: int = 0
```

用途：

- 调整亲密感；
- 调整表露安全感；
- 调整信任和旧伤；
- 区分隐私边界和伤害性隐瞒。

---

### 4.6 冲突与修复输入

来源：`29_conflict_communication_repair_system.md`。

```python
@dataclass
class ConflictRepairResult:
    conflict_escalation_risk: int = 0
    criticism_intensity: int = 0
    contempt_signal: int = 0
    defensive_response: int = 0
    stonewalling_level: int = 0
    active_listening_skill: int = 0
    validation_skill: int = 0
    timeout_repair_success: bool = False
    repair_attempt_quality: int = 0
```

用途：

- 判断冲突是升级还是修复；
- 区分暂停和石墙；
- 调整修复机会；
- 对蔑视、人格攻击、长期石墙写旧伤记忆。

---

### 4.7 社会交换与依赖输入

来源：`30_social_exchange_dependency_system.md`。

```python
@dataclass
class ExchangeDependencyResult:
    relationship_rewards_delta: int = 0
    relationship_costs_delta: int = 0
    comparison_level_gap: int = 0
    comparison_level_alternatives_delta: int = 0
    investment_weight_delta: int = 0
    leaving_cost_delta: int = 0
    dependence_gap_delta: int = 0
```

用途：

- 调整满意度；
- 调整依赖度；
- 调整稳定性；
- 区分“不幸福但稳定”和“幸福但不稳定”。

---

### 4.8 接近/回避输入

来源：`32_approach_avoidance_turbulence_system.md`。

```python
@dataclass
class ApproachAvoidanceResult:
    approach_reward_delta: int = 0
    avoidance_cost_pressure_delta: int = 0
    relationship_excitement_delta: int = 0
    relationship_safety_delta: int = 0
    boredom_delta: int = 0
    turbulence_delta: int = 0
    self_expansion_delta: int = 0
```

用途：

- 防止把低痛苦误判成高快乐；
- 防止把高刺激误判成安全；
- 处理沉闷、新鲜感和关系动荡。

---

### 4.9 共有/交换/公平输入

来源：`33_communal_exchange_equity_system.md`。

```python
@dataclass
class EquityResult:
    communal_care_delta: int = 0
    exchange_scorekeeping_delta: int = 0
    perceived_equity_delta: int = 0
    underbenefit_feeling_delta: int = 0
    overbenefit_guilt_delta: int = 0
    felt_appreciation_delta: int = 0
    taken_for_granted_delta: int = 0
```

用途：

- 调整公平感；
- 调整满意度和怨恨；
- 处理家务、照料、情绪劳动和被理所当然对待；
- 防止把共有关系写成无限牺牲。

---

## 5. 输出结构草案

聚合器输出建议统一为：

```python
@dataclass
class RelationshipStateDelta:
    trust_delta: int = 0
    satisfaction_delta: int = 0
    intimacy_delta: int = 0
    dependence_delta: int = 0
    stability_delta: int = 0
    repair_chance_delta: int = 0
    old_wound_memory_delta: int = 0
    safety_delta: int = 0
    excitement_delta: int = 0
    fairness_delta: int = 0
    report_tags: list[str] = field(default_factory=list)
    memory_notes: list[str] = field(default_factory=list)
    debug_reasons: list[str] = field(default_factory=list)
```

### 5.1 字段边界

| 字段 | 含义 | 主要来源 |
| --- | --- | --- |
| `trust_delta` | 信任变化 | 真实原因、欺骗、解释可信度、隐私/秘密 |
| `satisfaction_delta` | 满意度变化 | 奖赏代价、CL、公平、冲突质量 |
| `intimacy_delta` | 亲密感变化 | 自我表露、回应性、共有照顾、积极体验 |
| `dependence_delta` | 依赖度变化 | CLalt、投入、离开成本、替代选择 |
| `stability_delta` | 稳定性变化 | 依赖度、修复机会、替代选择、重大伤害 |
| `repair_chance_delta` | 修复机会变化 | 积极倾听、确认、暂停、补偿、道歉 |
| `old_wound_memory_delta` | 旧伤记忆变化 | 背叛、羞辱、蔑视、长期石墙、被攻击脆弱点 |
| `safety_delta` | 安全感变化 | 回避代价、信任、尊重、稳定回应 |
| `excitement_delta` | 活力和新鲜感变化 | 接近奖赏、自我延伸、共同新体验 |
| `fairness_delta` | 公平感变化 | 获益不足、过度获益、被珍惜、重新分工 |

---

## 6. 防止重复扣分规则

### 6.1 主责系统规则

同一影响只能有一个主责系统，其他系统只能作为修正因子。

| 影响类型 | 主责系统 | 其他系统角色 |
| --- | --- | --- |
| 事实信任损失 | 真实原因层 / 解释可信度 | 伴侣认知提供准确度标签 |
| 表露安全感 | 自我表露 / 回应性 | 冲突系统补充伤害程度 |
| 冲突升级 | 冲突沟通系统 | 归因系统补充解释倾向 |
| 满意度变化 | 社会交换 / 公平系统 | 沟通和冲突作为奖赏代价来源 |
| 依赖度变化 | 社会交换系统 | 替代选择和投入修正 |
| 沉闷和活力 | 接近/回避系统 | 社会交换系统只接收汇总结果 |
| 公平感变化 | 共有/公平系统 | 社会交换系统只接收结果修正 |
| 旧伤写入 | 真实伤害 + 冲突高伤害共同判定 | 不允许轻微事件反复写入 |

### 6.2 上限与归一化

MVP 阶段建议：

```text
单次事件每个 delta 限制在 -10 到 +10。
重大背叛、严重羞辱、长期石墙等特殊事件可以到 -20。
普通误会、轻微不满、一次性小冲突不应超过 -5。
```

理由：

```text
IF 是长期关系模拟，不应让单个普通事件直接摧毁关系。
```

---

## 7. 关键裁决规则

### 7.1 隐私不等于欺骗

```text
如果 privacy_boundary_conflict 高，但 deception_level 低，
则优先影响 intimacy_delta 和 satisfaction_delta，
不直接大幅扣 trust_delta。
```

只有当存在主动撒谎、隐藏证据、前后解释不一致或伤害性隐瞒时，才强烈影响 `trust_delta`。

---

### 7.2 沉默不一定是石墙

```text
如果 timeout_repair_success 为 true，
则不按 stonewalling 处理。
```

有效暂停可以：

- 小幅降低短期亲密感；
- 增加修复机会；
- 避免冲突升级。

石墙则会：

- 降低信任和满意度；
- 提高旧伤记忆；
- 降低修复机会。

---

### 7.3 争吵不一定扣分

```text
如果 conflict_escalation_risk 高，但 validation_skill、active_listening_skill 或 repair_attempt_quality 也高，
则冲突可能转化为修复机会。
```

会修复的冲突可以：

- 短期降低情绪稳定；
- 长期提高信任和亲密感；
- 增加双方对问题的理解。

---

### 7.4 怀疑不一定是焦虑

```text
如果 interpretation_type 是 suspicion，且 evidence_chain_strength 高，truth_harm_level 高，
则应标记 accurate_alertness，而不是 over_suspicion_pattern。
```

如果证据弱、投射强、威胁偏向强，则更可能是误会/焦虑。

---

### 7.5 低痛苦不等于高快乐

```text
avoidance_cost_pressure_delta 下降，只能说明痛苦和威胁下降；
不能自动提高 excitement_delta 或 intimacy_delta。
```

安全但沉闷的关系应表现为：

```text
safety_delta 高
excitement_delta 低或下降
boredom_delta 上升
```

---

### 7.6 高快乐不等于安全

```text
approach_reward_delta 高，但 avoidance_cost_pressure_delta 也高，
则可能是高刺激高风险关系。
```

这种关系可以提高 `intimacy_delta` 或 `excitement_delta`，同时降低 `safety_delta` 或 `stability_delta`。

---

### 7.7 公平不是五五分

```text
如果贡献不同但结果比例合理，perceived_equity 不应下降。
```

短期不对等在共有关系中可接受，但长期不被珍惜会增加：

```text
underbenefit_feeling_delta
taken_for_granted_delta
satisfaction_delta 下降
```

---

### 7.8 依赖不是爱，也不是弱点

```text
dependence_delta 高不等于 intimacy_delta 高。
```

依赖可能来自：

- 爱和投入；
- 离开成本；
- 替代选择低；
- 共同生活绑定；
- 害怕孤独。

聚合器必须区分：

```text
我想留下
我不敢离开
我离不开
我觉得值得继续
```

---

## 8. MVP 实现范围

第一版代码不必实现全部系统。建议 MVP 只实现：

```text
trust_delta
satisfaction_delta
intimacy_delta
stability_delta
repair_chance_delta
old_wound_memory_delta
report_tags
debug_reasons
```

暂缓：

```text
dependence_delta
fairness_delta
safety_delta
excitement_delta
完整 CL / CLalt 计算
完整共有/交换关系模型
完整关系动荡轨迹
```

### 8.1 MVP 输入

MVP 可以只接：

```text
truth_harm_level
deception_level
evidence_chain_strength
interpretation_accuracy
perceived_responsiveness
conflict_escalation_risk
validation_skill
stonewalling_level
repair_attempt_quality
relationship_rewards_delta
relationship_costs_delta
```

### 8.2 MVP 输出

MVP 输出：

```text
RelationshipStateDelta(
    trust_delta=..., 
    satisfaction_delta=..., 
    intimacy_delta=..., 
    stability_delta=..., 
    repair_chance_delta=..., 
    old_wound_memory_delta=..., 
    report_tags=[...],
    debug_reasons=[...],
)
```

---

## 9. 关键测试用例

后续实现时，至少添加以下测试。

### 9.1 沉默不一定是石墙

输入：

```text
stonewalling_level = 0
timeout_repair_success = true
repair_attempt_quality = high
```

预期：

```text
repair_chance_delta > 0
old_wound_memory_delta <= 0
不出现 stonewalling_pattern 标签
```

---

### 9.2 石墙是高伤害沟通

输入：

```text
stonewalling_level = high
timeout_repair_success = false
```

预期：

```text
trust_delta < 0
satisfaction_delta < 0
repair_chance_delta < 0
old_wound_memory_delta > 0
出现 stonewalling_pattern 标签
```

---

### 9.3 吵架但成功修复

输入：

```text
conflict_escalation_risk = medium
validation_skill = high
active_listening_skill = high
repair_attempt_quality = high
```

预期：

```text
repair_chance_delta > 0
intimacy_delta >= 0
satisfaction_delta 不应大幅下降
```

---

### 9.4 怀疑是准确警觉

输入：

```text
truth_harm_level = high
evidence_chain_strength = high
interpretation_type = suspicion
interpretation_accuracy = accurate
```

预期：

```text
出现 accurate_alertness 标签
不出现 over_suspicion_pattern 标签
trust_delta 根据事实伤害下降
```

---

### 9.5 怀疑是误会/焦虑

输入：

```text
truth_harm_level = low
evidence_chain_strength = low
projection_bias_effect = high
threat_bias_effect = high
```

预期：

```text
出现 over_suspicion_pattern 或 confident_misreader 标签
trust_delta 不应因事实伤害大幅下降
satisfaction_delta 可因压力小幅下降
```

---

### 9.6 隐私不等于欺骗

输入：

```text
privacy_boundary_conflict = high
deception_level = 0
truth_harm_level = low
```

预期：

```text
trust_delta 不应大幅下降
intimacy_delta 或 satisfaction_delta 可下降
出现 privacy_boundary_conflict 相关标签
```

---

### 9.7 低痛苦不等于高快乐

输入：

```text
avoidance_cost_pressure_delta = negative
approach_reward_delta = 0
boredom_delta = positive
```

预期：

```text
safety_delta 可上升
excitement_delta 不自动上升
可能出现 safe_but_bored_pattern
```

---

### 9.8 高快乐不等于安全

输入：

```text
approach_reward_delta = high
avoidance_cost_pressure_delta = high
conflict_escalation_risk = high
```

预期：

```text
excitement_delta > 0
safety_delta < 0
stability_delta < 0 或风险标签上升
出现 risk_excitement_pattern
```

---

### 9.9 公平不是五五分

输入：

```text
player_contribution = 70
player_outcome = 90
npc_contribution = 40
npc_outcome = 50
比例接近
```

预期：

```text
fairness_delta 不应下降
不出现 underbenefit_sensitive 标签
```

---

### 9.10 同一事件不能重复扣 trust

输入：

```text
一次欺骗事件同时触发 truth、evidence、interpretation、conflict
```

预期：

```text
trust_delta 由真实原因层主导
其他系统只能修正，不得重复叠加成过大扣分
```

---

## 10. 后续代码文件建议

第一批可新增：

```text
if_game/relationship_state_aggregator.py
tests/relationship_state_aggregator_test.py
```

建议 `relationship_state_aggregator.py` 暂时只包含：

```python
@dataclass
class RelationshipStateDelta:
    ...

def aggregate_relationship_event(...):
    ...
```

不要一开始就拆成大量文件。

---

## 11. 与现有代码的接入路径

### 11.1 第一阶段：独立测试

先让聚合器独立运行，不接主流程。

```bash
python tests/relationship_state_aggregator_test.py
```

### 11.2 第二阶段：接入 `relationship_interpretation.py`

让 `relationship_interpretation.py` 的输出可以转为聚合器输入。

### 11.3 第三阶段：接入事件报告

在玩家报告中展示：

- 本次事件影响了什么；
- 是信任问题、满意度问题、表露安全问题，还是公平问题；
- 哪些只是短期波动，哪些会进入长期记忆。

### 11.4 第四阶段：接入问卷结果

问卷只提供初始画像，不直接覆盖行为结果。

```text
问卷结果 = 初始倾向
事件行为 = 动态证据
聚合器 = 最终汇总
```

---

## 12. 后续版本建议

```text
v0.1.33 relationship_state_aggregator.py 原型
v0.1.34 aggregator 测试覆盖关键裁决规则
v0.1.35 relationship_interpretation.py 接入 aggregator
v0.1.36 冲突沟通事件接入 aggregator
v0.1.37 社会交换/公平轻量接入 aggregator
v0.1.38 问卷补 4 个沟通表露题
```

---

## 13. 一句话总结

```text
relationship_state_aggregator 的作用不是让关系模拟更复杂，
而是把 25-33 号文档中的复杂心理机制收束成一个稳定、可测试、不会重复扣分的关系状态结算层。
```

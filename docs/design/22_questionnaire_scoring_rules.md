# 问卷计分与可信度规则 v0.1

本文档定义 IF 超级真实版问卷的计分、可信度、标签生成和报告输出规则。它承接：

- `docs/design/15_full_questionnaire_upgrade_plan.md`
- `docs/design/16_questionnaire_dimension_table.md`
- `docs/design/17_question_type_schema.md`
- `docs/design/18_super_realistic_question_bank.md`
- `docs/design/18_super_realistic_question_bank_part2.md`
- `docs/design/18_super_realistic_question_bank_part3.md`
- `docs/design/18_super_realistic_question_bank_part4.md`
- `docs/design/19_relationship_report_templates.md`

本文档只做规则设计，不修改控制台原型运行逻辑。

## 1. 设计目标

问卷计分系统的目标不是把玩家简单判定成某种人格，而是把 Q001-Q150 的答案转成：

1. `self_report_profile`：自述人格与关系倾向；
2. `dimension_scores`：128维主表中的维度分数；
3. `confidence_scores`：每个维度的证据可信度；
4. `risk_tags`：可能影响剧情的风险标签；
5. `strength_tags`：稳定优势或修复能力标签；
6. `profile_gap_hints`：自述与情境题的潜在差异；
7. `report_sections`：玩家可读报告的输入。

计分系统必须遵守以下原则：

- 不做医学或心理诊断；
- 不用单题给严重标签；
- 不把高低值直接等同于好坏；
- 自评题权重低于情境题；
- 游戏内真实行为后续可以覆盖问卷自述；
- 反向验证题只降低可信度或提示矛盾，不直接惩罚玩家。

## 2. 总体流程

```text
玩家答案
  ↓
标准化 answer record
  ↓
题型权重处理
  ↓
选项维度影响累积
  ↓
模块内归一化
  ↓
生成 dimension_scores
  ↓
计算 evidence_count 与 confidence_scores
  ↓
执行反向验证和双标检测
  ↓
生成 tags 与 report_inputs
  ↓
输出玩家可读报告 + 游戏系统隐藏档案
```

## 3. 分数范围

所有底层维度建议统一使用 0-100。

| 区间 | 等级 | 报告表达 |
| ---: | --- | --- |
| 0-20 | 很低 | 很少出现 / 明显不倾向 |
| 21-40 | 较低 | 倾向较弱 |
| 41-60 | 中等 | 情境相关，需结合压力判断 |
| 61-80 | 较高 | 比较容易出现 |
| 81-100 | 很高 | 高概率出现，但仍需行为验证 |

报告中不建议直接显示数值，除非处于调试模式。玩家可读文本应使用“较低、中等、较高”等表达。

## 4. 初始基准值

每个维度默认从 50 开始。

```text
dimension_score_start = 50
```

选项影响不应让某一题直接把分数推到极端。建议单题对单一维度的最大影响：

| 题目类型 | 单题单维度最大影响 |
| --- | ---: |
| 普通自评题 | ±6 |
| 情境行为题 | ±10 |
| 主选择 + 次选择题 | 主选 ±10，次选 ±3 |
| 反向验证题 | ±4，同时影响可信度 |
| 双标配对题 | 直接分差后再计算，不单题极端加分 |
| 开放文本题 | 当前不自动计分 |

最终分数 clamp 到 0-100。

## 5. 题型权重

### 5.1 基础权重

| selection_mode | 基础权重 | 说明 |
| --- | ---: | --- |
| `forced_single` | 1.0 | 明确行为或态度 |
| `primary_with_secondary` | 1.0 | 主行为权重高，次要冲动低 |
| `multi_select` | 0.65 | 多个选项分散权重 |
| `multi_with_primary` | 0.85 | 主因高，其他原因中低 |
| `ranked_multi` | 0.8 | 根据排序递减 |
| `weighted_multi` | 1.0 | 根据玩家分配比例 |
| `slider` | 0.75 | 强度题，需反向验证 |
| `axis_2d` | 0.9 | 连续坐标，信息量较高 |
| `scenario_choice` | 1.0 | 具体情境，接近行为预测 |
| `npc_perspective` | 0.75 | 主要用于双标/共情检测 |
| `reverse_check` | 0.65 | 主要用于一致性和可信度 |
| `open_text` | 0.0 | 当前仅记录文本，不自动计分 |

### 5.2 主选择、次选择和原因标签

```text
primary_choice_weight = 1.0
secondary_choice_weight = 0.3
reason_tag_weight = 0.35
```

解释：

- `primary_choice` 表示玩家认为自己最可能执行的行为；
- `secondary_choices` 表示未执行但存在的冲动；
- `reason_tags` 表示背后的动机，可用于微调维度和生成报告文本；
- 次选择和原因标签不能压过主选择。

## 6. 不同题型计分规则

### 6.1 `forced_single`

只记录一个 `primary_choice`。

```text
score_delta = option_effect × 1.0 × confidence_factor
```

如果没有 `confidence` 字段，默认 `confidence_factor = 1.0`。

### 6.2 `primary_with_secondary`

```text
primary_delta = primary_option_effect × 1.0
secondary_delta = sum(secondary_option_effects) × 0.3
reason_delta = sum(reason_tag_effects) × 0.35
score_delta = primary_delta + secondary_delta + reason_delta
```

示例：

```text
primary_choice: partial_truth
secondary_choices: [full_truth]
reason_tags: [fear_conflict, protect_privacy]
```

表示主行为是“说一半”，但仍有坦白冲动。计分时提高 `info_partial_truth_tendency`，小幅提高 `info_honesty_tendency`，并记录“怕冲突”和“保留隐私”作为报告解释。

### 6.3 `multi_select`

多选题不能把所有选项完整相加，否则容易过度放大。

```text
per_choice_weight = 1 / sqrt(selected_count)
score_delta = sum(option_effect × per_choice_weight)
```

最多建议选择 5 项。超过 5 项时，应提示玩家标出主因或改用 `ranked_multi`。

### 6.4 `multi_with_primary`

```text
primary_delta = primary_option_effect × 1.0
other_delta = sum(other_option_effects) × 0.45
score_delta = primary_delta + other_delta
```

主因用于报告摘要，其他选项用于补充风险。

### 6.5 `ranked_multi`

排序权重建议：

| 排名 | 权重 |
| ---: | ---: |
| 1 | 1.0 |
| 2 | 0.75 |
| 3 | 0.55 |
| 4 | 0.35 |
| 5 | 0.25 |

超过第 5 项不建议计入核心分数，只可作为备注。

### 6.6 `weighted_multi`

玩家分配 100 点权重。

```text
choice_weight = allocated_points / 100
score_delta = option_effect × choice_weight
```

如果总和不是 100，保存前应归一化：

```text
normalized_weight = raw_weight / sum(raw_weights)
```

### 6.7 `slider`

滑条统一转成 -1 到 +1 的中心化值。

```text
centered = (slider_value - 50) / 50
score_delta = max_effect × centered × question_weight
```

示例：

```text
slider_value = 80
centered = 0.6
max_effect = +10
score_delta = +6
```

### 6.8 `axis_2d`

二维题通常影响 2-4 个维度。

```text
x_centered = (axis_x - 50) / 50
y_centered = (axis_y - 50) / 50
```

示例：依恋坐标：

```text
axis_x: 不担心被抛弃 ←→ 很担心被抛弃
axis_y: 愿意亲密 ←→ 害怕亲密

attachment_abandonment_anxiety += x_centered × 10
attachment_intimacy_avoidance += y_centered × 10
```

不要直接输出“你是某种依恋类型”，而是输出行为倾向。

### 6.9 `npc_perspective`

NPC视角题通常与玩家自身视角题配对，不建议单独使用。

```text
self_standard_score
partner_standard_score
standard_gap = partner_standard_score - self_standard_score
```

如果玩家对自己更宽松、对对方更严格，则增加：

- `boundary_double_standard`
- `trust_projection_tendency`
- `boundary_control_need`

如果玩家对自己和对方规则一致，则降低双标风险。

### 6.10 `reverse_check`

反向验证题主要影响可信度和自我认知差异。

```text
if self_rating_high and scenario_behavior_conflict:
  confidence -= conflict_penalty
  self_discrepancy_awareness += delta
  self_beautification_risk += delta
```

反向题不应写成“玩家撒谎”，而应写成“自评与压力情境存在差异”。

### 6.11 `open_text`

当前不自动计分。只进入：

- 玩家报告引用；
- 角色设定补充；
- 后续人工分析；
- 未来 AI 解析接口。

## 7. 确信度处理

`confidence` 表示玩家对该答案是否代表自己的确定程度。

| confidence | factor | 说明 |
| ---: | ---: | --- |
| 0-30 | 0.45 | 很不确定，降低权重 |
| 31-60 | 0.7 | 有倾向但不稳定 |
| 61-85 | 1.0 | 较可信 |
| 86-100 | 1.05 | 高可信，但仍需反向验证 |

高确信度只表示“自述更确定”，不表示“现实一定如此”。

## 8. 维度可信度 confidence_scores

每个维度应同时计算：

```text
dimension_score
confidence_score
evidence_count
conflict_count
```

### 8.1 证据数量

| evidence_count | 可信度上限 |
| ---: | --- |
| 0 | 无结论 |
| 1 | 低 |
| 2 | 中低 |
| 3-4 | 中 |
| 5-7 | 中高 |
| 8+ | 高 |

### 8.2 证据质量

证据来源权重：

| 来源 | 证据质量 |
| --- | ---: |
| 情境行为题 | 高 |
| 配对双标题 | 高 |
| 反向验证题 | 中高 |
| 排序/权重题 | 中 |
| 滑条自评题 | 中 |
| 普通自评题 | 中低 |
| 开放文本 | 当前不计 |

### 8.3 冲突惩罚

如果同一维度出现明显矛盾答案：

```text
confidence_score -= conflict_count × 0.08
```

但最低不低于 0。

报告文本应写：

```text
该维度在不同情境下存在差异，系统会在游戏中继续观察。
```

## 9. 完整度评分

```text
completion_rate = answered_questions / total_questions
```

| 完成率 | 等级 |
| ---: | --- |
| 90%-100% | 高 |
| 70%-89% | 中高 |
| 50%-69% | 中 |
| 25%-49% | 低 |
| 0%-24% | 很低 |

跳过题目不应强行填默认值，只降低相关维度的证据数量。

## 10. 自我美化风险

### 10.1 触发条件

自我美化风险来自以下差异：

| 自评 | 情境题 | 可能标签 |
| --- | --- | --- |
| 自称很诚实 | 多次选择说一半/模糊带过 | `self_beautification_risk` |
| 自称尊重隐私 | 多次选择查证/看线索 | `privacy_gap_risk` |
| 自称成熟沟通 | 冷处理/说重话/拉黑高 | `communication_gap_risk` |
| 自称忠诚原则强 | 精神暧昧/替代倾向高 | `loyalty_gap_risk` |
| 自称规则公平 | 自己宽松、对方严格 | `double_standard_risk` |

### 10.2 风险等级

| 分数 | 等级 | 报告表达 |
| ---: | --- | --- |
| 0-20 | 低 | 自述与情境选择大体一致。 |
| 21-40 | 中低 | 存在少量压力情境差异。 |
| 41-60 | 中 | 自述和情境反应存在一定落差。 |
| 61-80 | 中高 | 压力下行为可能明显不同于自我描述。 |
| 81-100 | 高 | 自述画像需要较强行为修正。 |

报告中不要写“你虚伪”，应写“自述和压力情境存在差异”。

## 11. 双标风险

### 11.1 配对题计算

双标主要来自成对问题，例如：

- Q034 对方和前任联系；
- Q035 自己和前任联系；
- Q041 对方和异性单独吃饭；
- Q042 自己和异性单独吃饭；
- Q045 对方要求你报备；
- Q046 你要求对方报备；
- Q057 自己被揭穿后的反应；
- Q058 对方被揭穿后的期望反应；
- Q094 自己暧昧 vs 对方暧昧；
- Q135 聊天记录透明度。

计算方式：

```text
self_freedom_score = 自己允许自己做某事的宽松程度
partner_freedom_score = 自己允许对方做同样事情的宽松程度
standard_gap = self_freedom_score - partner_freedom_score
```

如果 `standard_gap` 明显为正，说明玩家对自己更宽松，对对方更严格。

### 11.2 等级

| gap | 双标风险 |
| ---: | --- |
| 0-10 | 低 |
| 11-25 | 中低 |
| 26-45 | 中 |
| 46-65 | 中高 |
| 66+ | 高 |

双标风险不等于道德审判。报告应写：

```text
你在部分边界题中对自己的自由需求更高，同时也希望对方更透明。游戏中这会增加边界协商难度。
```

## 12. 标签生成规则

### 12.1 标签类型

| 标签类型 | 用途 |
| --- | --- |
| `visible_tags` | 玩家报告中展示 |
| `hidden_tags` | 游戏系统内部使用 |
| `risk_tags` | 高风险事件权重 |
| `strength_tags` | 修复能力、稳定能力 |
| `gap_tags` | 自述/情境差异 |
| `module_tags` | 模块摘要标签 |

### 12.2 标签触发条件

标签必须由多项证据触发。

```text
if dimension_score >= 70 and confidence_score >= medium and evidence_count >= 3:
  add_tag
```

高风险标签建议更严格：

```text
if risk_dimension >= 75 and confidence_score >= medium_high and evidence_count >= 4:
  add_risk_tag
```

### 12.3 示例标签规则

| 标签 | 条件示例 |
| --- | --- |
| `high_reassurance_need` | `emotion_reassurance_need >= 70` 且亲密/消息题证据 >= 3 |
| `suspicion_under_ambiguity` | `trust_suspicion_sensitivity >= 70` 且 `trust_explanation_acceptance <= 45` |
| `checking_impulse_risk` | `trust_checking_impulse >= 70` 且数字证据题证据 >= 3 |
| `pressure_based_concealment` | `info_concealment_tendency >= 65` 且 `communication_conflict_avoidance >= 60` |
| `partial_truth_pattern` | `info_partial_truth_tendency >= 70` |
| `conflict_shutdown_risk` | `emotion_shutdown_tendency >= 70` 或 `risk_avoidant_disappearance >= 70` |
| `repair_capable` | `communication_repair_initiative >= 65` 且 `moral_compensation_willingness >= 65` |
| `emotional_validation_vulnerability` | `desire_emotional_validation_hunger >= 70` 且 `desire_temptation_resistance <= 50` |
| `double_standard_risk` | 配对题 gap 达中高以上 |
| `stable_low_drama_pattern` | 多个冲突/信任风险较低，修复能力中高 |

## 13. 模块分数

报告不展示128维全量分数，而是先聚合为模块分数。

```text
module_score = weighted_average(selected_dimension_scores)
```

建议模块：

| 模块 | 组成维度示例 |
| --- | --- |
| 亲密依恋 | 忧虑被弃、回避亲密、亲密需求、独立需求、修复接受度 |
| 信任边界 | 基础信任、怀疑敏感、查证冲动、占有欲、边界尊重 |
| 信息管理 | 诚实倾向、隐瞒倾向、半真半假、秘密管理、愧疚感 |
| 冲突修复 | 直接沟通、防御性、冷处理、道歉能力、修复主动性 |
| 欲望忠诚 | 新鲜感、诱惑抵抗、替代倾向、情绪价值饥渴、忠诚认同 |
| 现实压力 | 时间管理、金钱管理、环境压力、作息、家庭压力 |
| 数字生活 | 手机隐私、在线压力、社媒展示、数字证据、小号倾向 |

## 14. 报告输出规则

### 14.1 文本强度映射

| 分数 | 文本 |
| ---: | --- |
| 0-20 | 很低 |
| 21-40 | 较低 |
| 41-60 | 中等 |
| 61-80 | 较高 |
| 81-100 | 很高 |

### 14.2 不确定表达

如果某维度分数高但可信度低，应写：

```text
你在少数题目中表现出较高倾向，但证据不足，系统会在游戏中继续观察。
```

如果分数中等但冲突多，应写：

```text
你在这个维度上呈现情境差异：平时可能较稳定，但压力下会明显变化。
```

### 14.3 高风险表达

不要写：

```text
你很可能背叛。
你很危险。
你就是控制欲强的人。
```

应写：

```text
在关系不顺、又出现强情绪价值来源时，你更需要主动设边界，否则容易进入模糊暧昧。
```

## 15. 游戏内行为修正规则

问卷生成的是初始自述档案。

```text
self_report_profile = questionnaire_result
behavior_profile = gameplay_choices
```

游戏行为权重应逐步高于问卷：

| 阶段 | 问卷权重 | 行为权重 |
| --- | ---: | ---: |
| 游戏开始 | 1.0 | 0.0 |
| 早期 1-3 个关键事件 | 0.75 | 0.25 |
| 中期 4-8 个关键事件 | 0.5 | 0.5 |
| 后期 9+ 关键事件 | 0.35 | 0.65 |
| 结局阶段 | 0.25 | 0.75 |

如果玩家实际行为长期违背问卷答案，报告应生成：

- 自我美化；
- 压力下行为变化；
- 表里不一；
- 关系伪装；
- 成长修正；
- 行为证明自述可信。

注意：这些标签应根据语境生成，不一定都是负面。

## 16. 输出数据结构草案

```text
questionnaire_result:
  mode: super_realistic
  total_questions: 150
  answered_questions: 148
  completion_rate: 0.986
  consistency_score: 0.78
  self_beautification_risk: medium
  double_standard_risk: medium_high
  dimension_scores:
    attachment_abandonment_anxiety:
      score: 76
      confidence: medium_high
      evidence_count: 7
      conflict_count: 1
    info_concealment_tendency:
      score: 68
      confidence: high
      evidence_count: 9
      conflict_count: 0
  module_scores:
    intimacy_attachment: medium_high
    trust_boundary: medium_high
    information_management: medium
    conflict_repair: medium
  visible_tags:
    - 需要稳定回应
    - 重视边界说明
    - 压力下容易选择性表达
  hidden_tags:
    - high_reassurance_need
    - suspicion_under_ambiguity
    - pressure_based_concealment
  risk_tags:
    - checking_impulse_risk
    - partial_truth_pattern
  strength_tags:
    - repair_possible_with_clear_explanation
  weak_evidence_dimensions:
    - family_privacy_boundary
    - stability_self_care
```

## 17. 计分配置示例

题库 JSON 化时，每个选项应包含维度影响。

```text
question_id: Q051
selection_mode: primary_with_secondary
options:
  full_truth:
    effects:
      info_honesty_tendency: 10
      info_concealment_tendency: -8
      moral_responsibility: 4
  partial_truth:
    effects:
      info_honesty_tendency: -4
      info_concealment_tendency: 8
      info_partial_truth_tendency: 12
      communication_conflict_avoidance: 5
  vague_explanation:
    effects:
      info_concealment_tendency: 10
      info_partial_truth_tendency: 6
      communication_conflict_avoidance: 8
  counter_question:
    effects:
      communication_defensiveness: 10
      moral_accountability_under_exposure: -6
      info_exposure_reaction: 8
```

## 18. 当前非目标

本规则暂不做：

- 实际 Python 实现；
- JSON 配置落地；
- AI 自动解析开放文本；
- 临床量表；
- 精准心理诊断；
- 所有128维度的最终权重校准；
- 大规模统计验证。

## 19. 后续待做

建议后续继续：

1. `docs/design/23_questionnaire_dimension_coverage.md`：Q001-Q150 对128维的覆盖率检查；
2. `docs/design/24_questionnaire_json_schema.md`：题库 JSON 配置草案；
3. `docs/design/20_npc_profile_layers.md`：NPC四层档案样例；
4. `docs/design/21_lie_evidence_memory_system.md`：谎言、证据和记忆系统；
5. 根据覆盖率检查结果，决定是否补充 Q151-Q180，而不是盲目继续加题。

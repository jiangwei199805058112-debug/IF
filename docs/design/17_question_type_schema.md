# 问卷题型数据结构设计 v0.1

本文档定义 IF 完整调查问卷的题型、答题记录、计分输入和反向验证结构。它承接：

- `docs/design/15_full_questionnaire_upgrade_plan.md`
- `docs/design/16_questionnaire_dimension_table.md`

本文件只做文档设计，不要求立即实现代码。

## 1. 设计目标

IF 的问卷题型不能简单分成“单选题”和“多选题”。现实关系中的回答通常同时包含：

1. 当下实际行为；
2. 没有执行但存在的次要冲动；
3. 多个并存的原因；
4. 对选择的确信度；
5. 自己视角和对方视角的差异；
6. 自述答案和游戏行为的差异。

因此题型系统的目标是：

- 支持强制主行为；
- 支持多选原因和动机；
- 支持主选项与次选项并存；
- 支持排序和权重分配；
- 支持二维点击和滑条；
- 支持反向验证、自我美化检测和双标检测；
- 为后续 `self_report_profile` 与 `behavior_profile` 对比提供结构化输入。

## 2. 核心原则

### 2.1 行为题必须保留主行为

现实中某些场景当下只能做一个主要行为。例如：

> 恋人问你是不是和异性单独吃饭，你会怎么回答？

玩家可能有多个念头，但最终会表现出一个主行为。因此这类题必须记录：

```text
primary_choice: vague_explanation
```

### 2.2 心理动机可以多选

同一行为可能有多个原因。例如“模糊带过”可能同时因为：

- 怕吵架；
- 觉得事情不严重；
- 怕对方误会；
- 想保留私人空间；
- 自己也有一点心虚。

因此原因字段应允许多选：

```text
reason_tags:
  - fear_conflict
  - think_not_serious
  - protect_private_space
```

### 2.3 单选题也可以有次要冲动

题目看似单选，但玩家可能会觉得“我主要会这样做，但也有另一种冲动”。因此推荐结构是：

```text
primary_choice: partial_truth
secondary_choices:
  - tell_full_truth
  - avoid_answer
confidence: 65
```

### 2.4 多选题最好能标出主因

如果原因可以多选，最好允许标出最主要原因：

```text
selected_choices:
  - fear_conflict
  - fear_misunderstanding
  - protect_freedom
primary_choice: fear_conflict
```

这样既保留复杂性，也不损失计分权重。

### 2.5 价值题优先用排序或权重

例如“关系中最重要的是什么”，不建议强制单选。更适合：

- `ranked_multi`：按重要性排序；
- `weighted_multi`：给每项分配权重。

### 2.6 不建议所有题都自由多选

如果所有题都自由多选，会降低行为预测力。题型应根据问题目的选择：

| 问题目的 | 推荐结构 |
| --- | --- |
| 当下行为 | 主选择必须唯一 |
| 原因动机 | 可多选，最好有主因 |
| 价值优先级 | 排序或权重 |
| 程度强弱 | 滑条 |
| 二维倾向 | 坐标点击 |
| 双标检测 | 玩家视角 + NPC视角配对 |
| 自我美化检测 | 自评题 + 情境题配对 |

## 3. 通用数据结构

每道题建议使用以下通用字段。

```text
question:
  id: Q_INFO_001
  module: info_management
  title: 异性饭局被问起
  prompt: 恋人问你是不是和异性单独吃饭，你会怎么回答？
  question_type: primary_with_secondary
  selection_mode: primary_with_secondary
  required: true
  allow_skip: false
  dimensions:
    - info_honesty_tendency
    - info_concealment_tendency
    - communication_conflict_avoidance
  options:
    - id: full_truth
      label: 完整坦白
    - id: partial_truth
      label: 说一半，但省略关键细节
    - id: vague_explanation
      label: 模糊带过
    - id: direct_lie
      label: 直接说不是
    - id: counter_question
      label: 反问对方为什么不信任
```

### 3.1 通用字段说明

| 字段 | 含义 |
| --- | --- |
| `id` | 题目唯一ID |
| `module` | 所属模块，例如依恋、信任、诚实、冲突 |
| `title` | 题目短标题 |
| `prompt` | 玩家看到的问题正文 |
| `question_type` | 题型类型 |
| `selection_mode` | 选择模式 |
| `required` | 是否必答 |
| `allow_skip` | 是否允许跳过 |
| `dimensions` | 影响的128维度ID |
| `options` | 可选项列表 |
| `reverse_pair_id` | 反向验证配对题，可选 |
| `perspective_pair_id` | NPC视角配对题，可选 |
| `report_tags` | 可影响的报告标签 |
| `notes` | 设计备注 |

## 4. selection_mode 枚举

| `selection_mode` | 中文名 | 用途 |
| --- | --- | --- |
| `forced_single` | 强制单选 | 现实中必须做一个主行为的题 |
| `multi_select` | 普通多选 | 原因、担忧、底线、触发点 |
| `primary_with_secondary` | 主选项+次选项 | 一个主行为，多个次要冲动 |
| `multi_with_primary` | 多选并标主因 | 多个原因并存，但有最主要原因 |
| `ranked_multi` | 多选排序 | 价值优先级、不可接受事项排序 |
| `weighted_multi` | 多选权重 | 多个价值/原因分配100点权重 |
| `slider` | 滑条 | 强度、频率、接受度 |
| `axis_2d` | 二维坐标 | 两个连续轴组合 |
| `scenario_choice` | 情境选择 | 复杂场景中的行为倾向 |
| `npc_perspective` | NPC视角题 | 测双标、共情、投射 |
| `reverse_check` | 反向验证题 | 测自我美化和前后矛盾 |
| `open_text` | 开放文本 | 补充经历、解释和自定义设定 |

## 5. 答案记录结构

玩家答案不建议只存一个选项ID。应根据题型记录完整结构。

```text
answer:
  question_id: Q_INFO_001
  selection_mode: primary_with_secondary
  primary_choice: partial_truth
  secondary_choices:
    - tell_full_truth
    - avoid_answer
  reason_tags:
    - fear_conflict
    - fear_misunderstanding
  confidence: 65
  answered_at: day_0_setup
```

### 5.1 答案字段说明

| 字段 | 含义 |
| --- | --- |
| `question_id` | 对应题目ID |
| `selection_mode` | 答案使用的选择模式 |
| `primary_choice` | 主行为或主原因 |
| `secondary_choices` | 次要冲动或次要选项 |
| `selected_choices` | 多选题全部选项 |
| `ranked_choices` | 排序题结果 |
| `weights` | 权重分配结果 |
| `slider_value` | 滑条数值 |
| `axis_x` / `axis_y` | 二维坐标结果 |
| `reason_tags` | 原因标签 |
| `confidence` | 确信度，0-100 |
| `open_text` | 开放文本 |
| `skipped` | 是否跳过 |

## 6. 题型定义与示例

### 6.1 `forced_single` 强制单选

适用场景：现实中当下只能做一个明确行为。

```text
question_type: forced_single
prompt: 对方当面问你是不是撒谎，你第一反应是什么？
options:
  - admit
  - explain_first
  - deny
  - counter_attack
  - leave_scene
```

答案：

```text
primary_choice: explain_first
confidence: 80
```

设计限制：

- 只能有一个 `primary_choice`；
- 可附加 `confidence`；
- 不建议用于价值观和复杂原因题。

### 6.2 `multi_select` 普通多选

适用场景：多个原因、担忧、底线可同时存在。

```text
question_type: multi_select
prompt: 什么情况最容易让你在关系里不安？
options:
  - long_no_reply
  - vague_explanation
  - opposite_sex_meal
  - hidden_phone
  - ex_contact
```

答案：

```text
selected_choices:
  - long_no_reply
  - vague_explanation
  - ex_contact
```

### 6.3 `primary_with_secondary` 主选项 + 次选项

适用场景：行为必须有一个主选择，但内心存在其他冲动。

```text
question_type: primary_with_secondary
prompt: 恋人问你和谁吃饭，你会怎么说？
options:
  - full_truth
  - partial_truth
  - vague_explanation
  - direct_lie
  - counter_question
```

答案：

```text
primary_choice: partial_truth
secondary_choices:
  - full_truth
reason_tags:
  - fear_conflict
  - think_not_serious
confidence: 65
```

计分建议：

- `primary_choice` 权重大；
- `secondary_choices` 权重小；
- `reason_tags` 用于解释报告和微调维度；
- `confidence` 影响结果可信度。

### 6.4 `multi_with_primary` 多选并标主因

适用场景：原因可以多选，但要知道最主要驱动。

```text
question_type: multi_with_primary
prompt: 你不想全部说明的原因有哪些？
options:
  - fear_conflict
  - protect_privacy
  - fear_misunderstanding
  - feel_guilty
  - think_partner_controls_too_much
```

答案：

```text
selected_choices:
  - fear_conflict
  - protect_privacy
  - fear_misunderstanding
primary_choice: fear_conflict
```

### 6.5 `ranked_multi` 多选排序

适用场景：价值优先级、底线严重程度。

```text
question_type: ranked_multi
prompt: 以下关系问题中，你最不能接受哪些？请选出并排序。
options:
  - cheating
  - lying
  - cold_violence
  - controlling
  - no_future_plan
```

答案：

```text
ranked_choices:
  - lying
  - cheating
  - cold_violence
```

### 6.6 `weighted_multi` 多选权重

适用场景：多个价值同时重要，需要表达比例。

```text
question_type: weighted_multi
prompt: 一段关系中你最看重什么？请分配100点。
options:
  - loyalty
  - freedom
  - companionship
  - spiritual_resonance
  - material_stability
```

答案：

```text
weights:
  loyalty: 35
  freedom: 20
  companionship: 20
  spiritual_resonance: 15
  material_stability: 10
```

规则：

- 总和必须为100；
- 可允许少量误差，但保存前应归一化；
- 用于价值观、爱情语言、需求优先级。

### 6.7 `slider` 滑条题

适用场景：程度、频率、接受度。

```text
question_type: slider
prompt: 吵架后你有多可能冷战或长时间不回复？
scale:
  min: 0
  max: 100
  left_label: 基本不会
  right_label: 很容易
```

答案：

```text
slider_value: 72
```

建议：

- 内部统一用 0-100；
- 玩家界面可显示 1-10 或文字刻度；
- 极端值应通过反向题验证。

### 6.8 `axis_2d` 二维坐标题

适用场景：两个连续轴共同决定一个倾向。

```text
question_type: axis_2d
prompt: 在亲密关系中，你更接近哪个位置？
axis_x:
  left: 不太担心被抛弃
  right: 很担心被抛弃
axis_y:
  top: 愿意亲密
  bottom: 害怕亲密
```

答案：

```text
axis_x: 78
axis_y: 62
```

说明：

- `axis_x` 和 `axis_y` 均建议使用 0-100；
- 不直接输出“你是某类型”；
- 可用于依恋、信任、边界、诚实、冲突、欲望、权力、责任坐标。

### 6.9 `scenario_choice` 情境选择题

适用场景：模拟具体关系事件。

```text
question_type: scenario_choice
prompt: 对方 4 小时没回消息，但朋友圈刚刚更新，你会怎么做？
options:
  - wait
  - ask_gently
  - question_directly
  - become_cold
  - check_more
```

建议结构：

- 可以是 `forced_single`；
- 也可以是 `primary_with_secondary`；
- 应写明是否允许次选项和原因标签。

### 6.10 `npc_perspective` NPC视角题

适用场景：检测双标、共情和投射。

玩家视角题：

> 你和异性朋友单独吃饭，没有提前告诉恋人，你觉得严重吗？

NPC视角题：

> 如果恋人和异性朋友单独吃饭，没有提前告诉你，你会怎么判断？

答案结构：

```text
perspective_pair_id: PAIR_SOC_001
```

如果玩家对自己更宽松、对对方更严格，则增加：

- `boundary_double_standard`
- `trust_projection_tendency`
- `boundary_possessiveness`

### 6.11 `reverse_check` 反向验证题

适用场景：检测自我美化和前后矛盾。

自评题：

> 我通常尊重伴侣隐私。

情境反向题：

> 当你很不安时，你是否会查看朋友圈、共同好友或时间线来确认？

如果自评“尊重隐私”高，但情境中查证冲动高，则增加：

- `self_discrepancy_awareness` 相关差异；
- `self_beautification_risk`；
- `trust_checking_impulse`。

### 6.12 `open_text` 开放文本

适用场景：补充经历、解释原因、角色自定义。

```text
question_type: open_text
prompt: 如果你愿意，可以描述一段让你很难再相信对方的经历。
max_length: 300
```

当前不接 AI API 时，开放文本只作为玩家报告和后续人工分析材料；未来接 AI 或本地解析后，可映射到维度和标签。

## 7. 原因标签 reason_tags

`reason_tags` 用于解释玩家为什么做出某个选择。它不等于选项本身。

常用原因标签：

| 标签 | 含义 |
| --- | --- |
| `fear_conflict` | 怕吵架 |
| `fear_abandonment` | 怕被抛弃 |
| `fear_misunderstanding` | 怕被误会 |
| `protect_privacy` | 想保留隐私 |
| `protect_freedom` | 想保留自由 |
| `avoid_guilt` | 不想面对愧疚 |
| `think_not_serious` | 觉得事情不严重 |
| `test_partner` | 想测试对方反应 |
| `retaliation` | 想反击或报复 |
| `save_face` | 想保全面子 |
| `avoid_responsibility` | 想避免承担后果 |
| `seek_reassurance` | 想获得安抚 |
| `maintain_image` | 想维持人设 |
| `protect_relationship` | 自认为是为了保护关系 |

## 8. 计分规则建议

### 8.1 选项影响结构

每个选项可以定义维度影响。

```text
option:
  id: partial_truth
  dimension_effects:
    info_honesty_tendency: -10
    info_concealment_tendency: +15
    info_partial_truth_tendency: +20
    communication_conflict_avoidance: +8
  report_tags:
    - pressure_based_concealment
```

### 8.2 主选项和次选项权重

建议：

| 来源 | 权重 |
| --- | ---: |
| `primary_choice` | 1.0 |
| `secondary_choices` | 0.25-0.4 |
| `reason_tags` | 0.2-0.5 |
| `confidence` | 调整可信度，不直接等于强度 |
| 游戏行为 | 应高于自述问卷 |

### 8.3 确信度处理

`confidence` 表示玩家对该选择的确定程度。

| 确信度 | 解释 |
| --- | --- |
| 0-30 | 很不确定，降低该题权重 |
| 31-60 | 有倾向但不稳定 |
| 61-85 | 较可信 |
| 86-100 | 高可信，但仍需反向验证 |

不建议把高确信度直接等于高分，只能说明该答案更能代表玩家自述。

## 9. 双标检测规则

双标检测依赖配对题。

```text
pair:
  id: PAIR_SOC_001
  self_question_id: Q_SELF_SOC_001
  partner_question_id: Q_PARTNER_SOC_001
  compared_dimensions:
    - boundary_double_standard
    - trust_loyalty_sensitivity
    - boundary_possessiveness
```

判定示例：

| 自己行为判断 | 对方同样行为判断 | 结果 |
| --- | --- | --- |
| 觉得不严重 | 觉得对方严重越界 | 双标上升 |
| 觉得需要自由 | 要求对方提前报备 | 双标和控制欲上升 |
| 自己也愿意公开说明 | 对方说明后能接受 | 双标低 |

## 10. 自我美化检测规则

自我美化检测依赖“自评题 + 情境题”。

示例：

| 自评 | 情境反应 | 解释 |
| --- | --- | --- |
| 自称很诚实 | 情境中频繁选择模糊带过 | 自我美化风险上升 |
| 自称尊重隐私 | 情境中选择查证和看手机 | 自我认知差异上升 |
| 自称成熟沟通 | 冲突中选择冷战拉黑 | 沟通自评可信度下降 |

输出不应写成“你虚伪”，而应写：

> 你的自我描述和情境选择存在差异。你倾向于认为自己尊重边界，但在不安场景中会更想查证细节。

## 11. 题库编写规范

后续 `18_super_realistic_question_bank.md` 编写题目时，应遵守：

1. 每题必须标注 `question_type` 和 `selection_mode`；
2. 行为题必须说明是否有 `primary_choice`；
3. 原因题应允许 `multi_select` 或 `multi_with_primary`；
4. 价值题优先使用 `ranked_multi` 或 `weighted_multi`；
5. 重要维度至少通过两种题型覆盖；
6. 高风险结论必须由多题支持，不能单题触发；
7. NPC视角题必须写明配对关系；
8. 反向验证题必须写明被验证的原题或维度；
9. 开放文本题不能作为唯一计分来源；
10. 玩家报告只输出关系反馈，不输出诊断标签。

## 12. 与后续文档关系

本文档完成后，下一步建议创建：

```text
docs/design/18_super_realistic_question_bank.md
```

该题库应基于：

- `15_full_questionnaire_upgrade_plan.md` 的四档问卷结构；
- `16_questionnaire_dimension_table.md` 的128维主表；
- 本文档的题型结构；
- `13_psychology_framework_mapping.md` 的理论边界；
- `02_personality_questionnaire.md` 的 v0.1 短问卷历史题目。

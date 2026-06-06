# 问卷 JSON 配置草案 v0.1

本文档定义 IF 超级真实版问卷未来 JSON 配置的结构草案。它承接：

- `docs/design/15_full_questionnaire_upgrade_plan.md`
- `docs/design/16_questionnaire_dimension_table.md`
- `docs/design/17_question_type_schema.md`
- `docs/design/18_super_realistic_question_bank.md`
- `docs/design/18_super_realistic_question_bank_part2.md`
- `docs/design/18_super_realistic_question_bank_part3.md`
- `docs/design/18_super_realistic_question_bank_part4.md`
- `docs/design/19_relationship_report_templates.md`
- `docs/design/22_questionnaire_scoring_rules.md`
- `docs/design/23_questionnaire_dimension_coverage.md`

本文件只做设计文档，不新增真实 JSON 配置文件，不修改现有题库内容，不修改 Python 代码。

## 1. 设计目标

问卷 JSON 的目标是把 Q001-Q150 从文档题库转换成可加载、可计分、可生成报告的配置结构。第一版配置要优先支持：

- 四档问卷模式：快速版、标准版、深度版、超级真实版；
- 150 题超级真实版题库；
- 128 维度计分；
- 主选项、次选项、原因标签、确信度；
- 双标配对题和反向验证题；
- 玩家可读报告和系统隐藏标签；
- 后续游戏行为修正 `self_report_profile`。

## 2. 顶层结构

未来题库配置建议使用一个顶层对象，包含 `questionnaire_meta`、`modules`、`questions` 和可选的全局计分配置。

```json
{
  "questionnaire_meta": {
    "id": "if_super_realistic_questionnaire_v0_1",
    "version": "0.1",
    "title": "IF 超级真实版关系问卷",
    "source_docs": [
      "docs/design/18_super_realistic_question_bank.md",
      "docs/design/18_super_realistic_question_bank_part2.md",
      "docs/design/18_super_realistic_question_bank_part3.md",
      "docs/design/18_super_realistic_question_bank_part4.md"
    ],
    "default_mode": "standard",
    "supported_modes": ["quick", "standard", "deep", "super_realistic"],
    "score_range": [0, 100],
    "default_dimension_score": 50
  },
  "modules": [],
  "questions": [],
  "scoring": {
    "selection_mode_weights": {
      "forced_single": 1.0,
      "primary_with_secondary": 1.0,
      "multi_select": 0.65,
      "multi_with_primary": 0.85,
      "ranked_multi": 0.8,
      "weighted_multi": 1.0,
      "slider": 0.75,
      "axis_2d": 0.9,
      "scenario_choice": 1.0,
      "npc_perspective": 0.75,
      "reverse_check": 0.65,
      "open_text": 0.0
    },
    "primary_choice_weight": 1.0,
    "secondary_choice_weight": 0.3,
    "reason_tag_weight": 0.35
  }
}
```

## 3. `questionnaire_meta`

`questionnaire_meta` 描述整份问卷，不参与单题计分。

| 字段 | 类型 | MVP | 说明 |
| --- | --- | --- | --- |
| `id` | string | 必须 | 问卷配置唯一 ID |
| `version` | string | 必须 | 配置版本 |
| `title` | string | 必须 | 玩家或编辑器可读标题 |
| `source_docs` | string[] | 必须 | 来源设计文档 |
| `default_mode` | string | 必须 | 默认问卷模式 |
| `supported_modes` | string[] | 必须 | 支持的问卷模式 |
| `score_range` | number[] | 必须 | 维度分数范围，默认 0-100 |
| `default_dimension_score` | number | 必须 | 维度起始值，默认 50 |
| `locale` | string | 扩展 | 多语言预留 |
| `status` | string | 扩展 | draft/review/published |

## 4. `modules`

`modules` 用于组织题目、控制问卷模式下的题目筛选，以及生成模块报告。

```json
{
  "id": "intimacy_attachment",
  "title": "依恋与亲密",
  "order": 3,
  "description": "测量亲密需求、独立需求、被弃焦虑和修复接受度。",
  "modes": ["quick", "standard", "deep", "super_realistic"],
  "target_question_ids": ["Q017", "Q018", "Q019", "Q020"],
  "report_section_id": "attachment_report",
  "primary_dimensions": [
    "attachment_abandonment_anxiety",
    "attachment_intimacy_avoidance",
    "attachment_closeness_need",
    "attachment_independence_need"
  ]
}
```

| 字段 | MVP | 说明 |
| --- | --- | --- |
| `id` | 必须 | 模块 ID |
| `title` | 必须 | 模块中文名 |
| `order` | 必须 | 展示顺序 |
| `description` | 必须 | 模块说明 |
| `modes` | 必须 | 哪些问卷模式启用 |
| `target_question_ids` | 必须 | 模块包含题号 |
| `report_section_id` | 必须 | 对应报告章节 |
| `primary_dimensions` | 必须 | 模块主要维度 |
| `coverage_level` | 扩展 | 高/中/低/空缺 |

## 5. `questions`

每道题建议使用统一结构。不同题型可以增加 `scale`、`axis`、`rank_rules`、`weight_rules` 等扩展字段。

```json
{
  "id": "Q017",
  "module_id": "intimacy_attachment",
  "title": "对方长时间不回消息",
  "prompt": "你发了重要消息，对方几个小时没回，也没有提前说忙。你第一反应更接近哪种？",
  "question_type": "primary_with_secondary",
  "selection_mode": "primary_with_secondary",
  "required": true,
  "allow_skip": false,
  "modes": ["quick", "standard", "deep", "super_realistic"],
  "dimensions": [
    "attachment_abandonment_anxiety",
    "trust_checking_impulse",
    "emotion_reassurance_need"
  ],
  "options": [],
  "reason_tags": [],
  "reverse_pair_id": null,
  "perspective_pair_id": null,
  "scoring": {
    "base_weight": 1.0,
    "evidence_quality": "high"
  },
  "confidence": {
    "enabled": true,
    "default": 70,
    "affects_weight": true
  },
  "report_tags": []
}
```

### 5.1 题目字段说明

| 字段 | MVP | 说明 |
| --- | --- | --- |
| `id` | 必须 | 题号，例如 `Q017` |
| `module_id` | 必须 | 所属模块 |
| `title` | 必须 | 短标题 |
| `prompt` | 必须 | 玩家看到的题干 |
| `question_type` | 必须 | 题型 |
| `selection_mode` | 必须 | 答题选择模式 |
| `required` | 必须 | 是否必答 |
| `allow_skip` | 必须 | 是否允许跳过 |
| `modes` | 必须 | 哪些问卷模式启用 |
| `dimensions` | 必须 | 影响的维度 ID |
| `options` | 必须 | 离散选项；滑条/坐标题可为空 |
| `dimension_effects` | 必须 | 非选项型题或坐标题的维度影响 |
| `reason_tags` | 建议 MVP 支持 | 可选原因标签 |
| `reverse_pair_id` | 扩展 | 反向验证配对题 |
| `perspective_pair_id` | 扩展 | 自己/对方视角配对题 |
| `scoring` | 必须 | 题级计分规则 |
| `confidence` | 必须 | 确信度规则 |
| `report_tags` | 必须 | 报告标签候选 |

## 6. `options`

离散题的 `options` 是数组。每个选项可以独立配置维度影响、报告标签和原因标签。

```json
{
  "id": "partial_truth",
  "label": "只说重点，不展开细节。",
  "value": "B",
  "dimension_effects": {
    "info_honesty_tendency": -4,
    "info_concealment_tendency": 8,
    "info_partial_truth_tendency": 12,
    "communication_conflict_avoidance": 5
  },
  "reason_tags": ["fear_conflict", "fear_misunderstanding", "protect_privacy"],
  "report_tags": ["pressure_based_concealment", "partial_truth_pattern"]
}
```

| 字段 | MVP | 说明 |
| --- | --- | --- |
| `id` | 必须 | 稳定选项 ID |
| `label` | 必须 | 玩家看到的选项文本 |
| `value` | 必须 | 原题选项序号，例如 A/B/C |
| `dimension_effects` | 必须 | 对维度分数的方向和强度 |
| `reason_tags` | 扩展 | 该选项可关联的原因 |
| `report_tags` | 必须 | 可触发的报告标签 |
| `hidden_tags` | 扩展 | 系统内部标签 |
| `visible_tags` | 扩展 | 玩家可见标签 |

## 7. `selection_mode`

`selection_mode` 与 `17_question_type_schema.md` 保持一致。

| 值 | 用途 |
| --- | --- |
| `forced_single` | 强制单选 |
| `multi_select` | 普通多选 |
| `primary_with_secondary` | 主选项 + 次选项 |
| `multi_with_primary` | 多选并标主因 |
| `ranked_multi` | 多选排序 |
| `weighted_multi` | 多选权重 |
| `slider` | 滑条 |
| `axis_2d` | 二维坐标 |
| `scenario_choice` | 情境行为题 |
| `npc_perspective` | NPC 视角题 |
| `reverse_check` | 反向验证题 |
| `open_text` | 开放文本 |

## 8. `dimensions` 与 `dimension_effects`

`dimensions` 表示题目可能影响哪些维度；`dimension_effects` 表示实际计分影响。

离散选项的 `dimension_effects` 放在每个 option 内。滑条和坐标题可以放在题目级：

```json
{
  "dimension_effects": {
    "axis_x": {
      "boundary_double_standard": 12,
      "values_freedom_need": 8
    },
    "axis_y": {
      "boundary_double_standard": 12,
      "trust_loyalty_sensitivity": 8
    }
  }
}
```

规则：

- 单题单维度影响不应过大；
- 情境题、坐标题、配对题证据质量更高；
- 开放文本当前不自动计分；
- 高风险标签不能由单题直接触发。

## 9. `reason_tags`

`reason_tags` 解释玩家为什么做出选择。它用于微调分数和生成报告，不等于选项本身。

```json
{
  "id": "fear_conflict",
  "label": "怕吵架",
  "dimension_effects": {
    "communication_conflict_avoidance": 5,
    "info_concealment_tendency": 3
  },
  "report_tags": ["avoid_conflict_motive"]
}
```

常用原因包括：

- `fear_conflict`
- `fear_abandonment`
- `fear_misunderstanding`
- `protect_privacy`
- `protect_freedom`
- `avoid_guilt`
- `think_not_serious`
- `test_partner`
- `retaliation`
- `save_face`
- `avoid_responsibility`
- `seek_reassurance`
- `maintain_image`
- `protect_relationship`

## 10. 配对字段

### 10.1 `reverse_pair_id`

用于反向验证。例如自评“我很诚实”和情境中“我会说一半”存在差异时，不直接判定玩家撒谎，只降低相关结论可信度并生成差异提示。

```json
{
  "id": "Q051",
  "reverse_pair_id": "Q065"
}
```

### 10.2 `perspective_pair_id`

用于自己视角和对方视角配对，检测双标、投射和共情。

```json
{
  "id": "Q042",
  "perspective_pair_id": "PAIR_SOCIAL_BOUNDARY_001"
}
```

配对对象建议单独配置：

```json
{
  "id": "PAIR_SOCIAL_BOUNDARY_001",
  "self_question_id": "Q042",
  "partner_question_id": "Q041",
  "compared_dimensions": [
    "boundary_double_standard",
    "trust_loyalty_sensitivity",
    "boundary_possessiveness"
  ]
}
```

## 11. `scoring`

题级 `scoring` 用于覆盖默认计分规则。

```json
{
  "scoring": {
    "base_weight": 1.0,
    "primary_choice_weight": 1.0,
    "secondary_choice_weight": 0.3,
    "reason_tag_weight": 0.35,
    "evidence_quality": "high",
    "max_single_dimension_effect": 10,
    "normalization": "clamp_0_100"
  }
}
```

说明：

- `base_weight` 先来自 `selection_mode`；
- `primary_choice` 权重大于 `secondary_choices`；
- `reason_tags` 只做解释和微调；
- `confidence` 影响权重，不代表强度；
- 反向验证主要影响可信度，不直接惩罚玩家。

## 12. `confidence`

`confidence` 表示玩家对该回答是否代表自己的确定程度。

```json
{
  "confidence": {
    "enabled": true,
    "default": 70,
    "min": 0,
    "max": 100,
    "affects_weight": true,
    "low_confidence_policy": "reduce_weight"
  }
}
```

建议映射：

| confidence | factor | 说明 |
| ---: | ---: | --- |
| 0-30 | 0.45 | 很不确定 |
| 31-60 | 0.7 | 有倾向但不稳定 |
| 61-85 | 1.0 | 较可信 |
| 86-100 | 1.05 | 高可信，但仍需反向验证 |

## 13. `report_tags`

`report_tags` 用于生成玩家报告和系统内部标签。标签必须由多项证据触发。

```json
{
  "report_tags": [
    {
      "id": "pressure_based_concealment",
      "visibility": "visible",
      "label": "压力下容易选择性表达",
      "requires_evidence_count": 3
    },
    {
      "id": "partial_truth_pattern",
      "visibility": "hidden",
      "label": "半真半假倾向",
      "requires_evidence_count": 3
    }
  ]
}
```

可见标签进入玩家报告；隐藏标签进入事件权重、NPC 反应、风险事件和后续行为修正。

## 14. 六个题目 JSON 示例

以下示例用于说明结构，不代表最终数值权重已经校准。

### 14.1 Q001 关系入口

```json
{
  "id": "Q001",
  "module_id": "basic_profile",
  "title": "关系入口",
  "prompt": "你们当前的关系更接近哪一种？",
  "question_type": "forced_single",
  "selection_mode": "forced_single",
  "required": true,
  "allow_skip": false,
  "modes": ["quick", "standard", "deep", "super_realistic"],
  "dimensions": ["attachment_commitment_pace", "values_belonging_need"],
  "options": [
    {
      "id": "chatting_new",
      "value": "A",
      "label": "刚认识，还在普通聊天。",
      "dimension_effects": {
        "attachment_commitment_pace": -6,
        "values_belonging_need": -2
      },
      "report_tags": ["early_contact_stage"]
    },
    {
      "id": "chatting_frequent",
      "value": "B",
      "label": "已经频繁聊天，有一点暧昧。",
      "dimension_effects": {
        "attachment_commitment_pace": -2,
        "values_belonging_need": 2
      },
      "report_tags": ["ambiguous_start"]
    },
    {
      "id": "ambiguous_clear",
      "value": "C",
      "label": "暧昧明显，但还没有正式确认关系。",
      "dimension_effects": {
        "attachment_commitment_pace": 2,
        "values_belonging_need": 4
      },
      "report_tags": ["ambiguous_start"]
    },
    {
      "id": "new_relationship",
      "value": "D",
      "label": "刚确认恋爱关系。",
      "dimension_effects": {
        "attachment_commitment_pace": 5,
        "values_belonging_need": 5
      },
      "report_tags": ["new_relationship_stage"]
    },
    {
      "id": "reconnected_after_breakup",
      "value": "E",
      "label": "已经分手，但最近又开始联系。",
      "dimension_effects": {
        "attachment_commitment_pace": -3,
        "values_belonging_need": 3,
        "risk_repeat_pattern": 4
      },
      "report_tags": ["reconnect_stage"]
    }
  ],
  "reason_tags": [],
  "reverse_pair_id": null,
  "perspective_pair_id": null,
  "dimension_effects": {},
  "scoring": {
    "base_weight": 1.0,
    "evidence_quality": "medium"
  },
  "confidence": {
    "enabled": false,
    "default": 100
  },
  "report_tags": ["relationship_entry_context"]
}
```

### 14.2 Q017 对方长时间不回消息

```json
{
  "id": "Q017",
  "module_id": "intimacy_attachment",
  "title": "对方长时间不回消息",
  "prompt": "你发了重要消息，对方几个小时没回，也没有提前说忙。你第一反应更接近哪种？",
  "question_type": "primary_with_secondary",
  "selection_mode": "primary_with_secondary",
  "required": true,
  "allow_skip": false,
  "modes": ["quick", "standard", "deep", "super_realistic"],
  "dimensions": [
    "attachment_abandonment_anxiety",
    "trust_checking_impulse",
    "emotion_reassurance_need"
  ],
  "options": [
    {
      "id": "assume_busy",
      "value": "A",
      "label": "先默认对方在忙。",
      "dimension_effects": {
        "attachment_abandonment_anxiety": -6,
        "trust_explanation_acceptance": 5
      },
      "report_tags": ["can_hold_uncertainty"]
    },
    {
      "id": "uncomfortable_but_wait",
      "value": "B",
      "label": "有点不舒服，但先忍住。",
      "dimension_effects": {
        "attachment_abandonment_anxiety": 4,
        "emotion_suppression_tendency": 5
      },
      "report_tags": ["quiet_unease"]
    },
    {
      "id": "ask_why_no_reply",
      "value": "C",
      "label": "想追问为什么不回。",
      "dimension_effects": {
        "attachment_abandonment_anxiety": 7,
        "emotion_reassurance_need": 7
      },
      "report_tags": ["needs_reassurance"]
    },
    {
      "id": "become_cold",
      "value": "D",
      "label": "表面不问，但自己开始冷淡。",
      "dimension_effects": {
        "emotion_shutdown_tendency": 8,
        "communication_conflict_avoidance": 5
      },
      "report_tags": ["cold_response_risk"]
    },
    {
      "id": "check_clues",
      "value": "E",
      "label": "想去看朋友圈、共同好友或其他线索。",
      "dimension_effects": {
        "trust_checking_impulse": 9,
        "attachment_abandonment_anxiety": 5
      },
      "report_tags": ["checking_impulse_risk"]
    }
  ],
  "reason_tags": [
    "fear_abandonment",
    "seek_reassurance",
    "fear_misunderstanding",
    "protect_relationship"
  ],
  "reverse_pair_id": null,
  "perspective_pair_id": null,
  "dimension_effects": {},
  "scoring": {
    "base_weight": 1.0,
    "primary_choice_weight": 1.0,
    "secondary_choice_weight": 0.3,
    "reason_tag_weight": 0.35,
    "evidence_quality": "high"
  },
  "confidence": {
    "enabled": true,
    "default": 70,
    "affects_weight": true
  },
  "report_tags": ["message_delay_sensitivity"]
}
```

### 14.3 Q051 做了可能让对方不高兴的事

```json
{
  "id": "Q051",
  "module_id": "information_management",
  "title": "做了可能让对方不高兴的事",
  "prompt": "你做了一件可能让对方不高兴、但你觉得不算严重的事。对方问起来时，你更可能怎么说？",
  "question_type": "primary_with_secondary",
  "selection_mode": "primary_with_secondary",
  "required": true,
  "allow_skip": false,
  "modes": ["standard", "deep", "super_realistic"],
  "dimensions": [
    "info_honesty_tendency",
    "info_concealment_tendency",
    "info_partial_truth_tendency",
    "communication_defensiveness"
  ],
  "options": [
    {
      "id": "full_truth",
      "value": "A",
      "label": "主动完整说明。",
      "dimension_effects": {
        "info_honesty_tendency": 10,
        "info_concealment_tendency": -8,
        "moral_responsibility": 4
      },
      "report_tags": ["transparent_under_pressure"]
    },
    {
      "id": "key_points_only",
      "value": "B",
      "label": "只说重点，不展开细节。",
      "dimension_effects": {
        "info_honesty_tendency": -2,
        "info_concealment_tendency": 5,
        "info_partial_truth_tendency": 8
      },
      "report_tags": ["selective_expression"]
    },
    {
      "id": "wait_for_details",
      "value": "C",
      "label": "等对方问到细节再说。",
      "dimension_effects": {
        "info_concealment_tendency": 7,
        "info_partial_truth_tendency": 8,
        "communication_conflict_avoidance": 4
      },
      "report_tags": ["delayed_disclosure"]
    },
    {
      "id": "vague_avoid_conflict",
      "value": "D",
      "label": "模糊带过，避免吵架。",
      "dimension_effects": {
        "info_concealment_tendency": 10,
        "info_partial_truth_tendency": 6,
        "communication_conflict_avoidance": 8
      },
      "report_tags": ["pressure_based_concealment"]
    },
    {
      "id": "counter_question",
      "value": "E",
      "label": "反问对方为什么不信任自己。",
      "dimension_effects": {
        "communication_defensiveness": 10,
        "moral_accountability_under_exposure": -6,
        "info_exposure_reaction": 8
      },
      "report_tags": ["defensive_when_questioned"]
    }
  ],
  "reason_tags": [
    "fear_conflict",
    "think_not_serious",
    "fear_misunderstanding",
    "protect_privacy",
    "avoid_guilt",
    "protect_freedom"
  ],
  "reverse_pair_id": "Q065",
  "perspective_pair_id": null,
  "dimension_effects": {},
  "scoring": {
    "base_weight": 1.0,
    "primary_choice_weight": 1.0,
    "secondary_choice_weight": 0.3,
    "reason_tag_weight": 0.35,
    "evidence_quality": "high"
  },
  "confidence": {
    "enabled": true,
    "default": 70,
    "affects_weight": true
  },
  "report_tags": ["information_management_pattern"]
}
```

### 14.4 Q069 自己自由 vs 对方自由

```json
{
  "id": "Q069",
  "module_id": "double_standard_checks",
  "title": "自己自由 vs 对方自由",
  "prompt": "在异性朋友、前任、手机隐私这些问题上，你对自己和对方的标准更接近哪里？",
  "question_type": "axis_2d",
  "selection_mode": "axis_2d",
  "required": true,
  "allow_skip": false,
  "modes": ["deep", "super_realistic"],
  "dimensions": [
    "boundary_double_standard",
    "values_freedom_need",
    "trust_loyalty_sensitivity"
  ],
  "options": [],
  "axis": {
    "x": {
      "min": 0,
      "max": 100,
      "left_label": "自己和对方规则完全一样",
      "right_label": "自己需要更多自由"
    },
    "y": {
      "min": 0,
      "max": 100,
      "left_label": "对方也应有同等自由",
      "right_label": "对方需要更高透明度"
    }
  },
  "reason_tags": [],
  "reverse_pair_id": null,
  "perspective_pair_id": "PAIR_BOUNDARY_STANDARD_001",
  "dimension_effects": {
    "axis_x": {
      "boundary_double_standard": 12,
      "values_freedom_need": 8
    },
    "axis_y": {
      "boundary_double_standard": 12,
      "trust_loyalty_sensitivity": 8
    }
  },
  "scoring": {
    "base_weight": 0.9,
    "axis_center": 50,
    "evidence_quality": "high"
  },
  "confidence": {
    "enabled": true,
    "default": 70,
    "affects_weight": true
  },
  "report_tags": ["double_standard_risk", "boundary_rule_gap"]
}
```

### 14.5 Q090 即时满足 vs 长期后果

```json
{
  "id": "Q090",
  "module_id": "desire_loyalty",
  "title": "即时满足 vs 长期后果",
  "prompt": "面对一件当下很想做、但可能影响关系的事，你更接近哪个位置？",
  "question_type": "axis_2d",
  "selection_mode": "axis_2d",
  "required": true,
  "allow_skip": false,
  "modes": ["standard", "deep", "super_realistic"],
  "dimensions": [
    "desire_instant_gratification",
    "moral_consequence_forecast",
    "desire_temptation_resistance"
  ],
  "options": [],
  "axis": {
    "x": {
      "min": 0,
      "max": 100,
      "left_label": "更看重长期后果",
      "right_label": "更看重当下感受"
    },
    "y": {
      "min": 0,
      "max": 100,
      "left_label": "会主动设边界",
      "right_label": "需要事情发生后再处理"
    }
  },
  "reason_tags": ["avoid_responsibility", "protect_freedom", "think_not_serious"],
  "reverse_pair_id": null,
  "perspective_pair_id": null,
  "dimension_effects": {
    "axis_x": {
      "desire_instant_gratification": 12,
      "moral_consequence_forecast": -10
    },
    "axis_y": {
      "desire_temptation_resistance": -10,
      "moral_consequence_forecast": -6
    }
  },
  "scoring": {
    "base_weight": 0.9,
    "axis_center": 50,
    "evidence_quality": "high"
  },
  "confidence": {
    "enabled": true,
    "default": 70,
    "affects_weight": true
  },
  "report_tags": ["instant_gratification_risk", "temptation_boundary_risk"]
}
```

### 14.6 Q150 超级真实版最终总结

```json
{
  "id": "Q150",
  "module_id": "final_self_summary",
  "title": "超级真实版最终总结",
  "prompt": "做完整份问卷后，你觉得自己在亲密关系里最核心的矛盾是什么？可以多选，并标出最主要的一项。",
  "question_type": "multi_with_primary",
  "selection_mode": "multi_with_primary",
  "required": true,
  "allow_skip": false,
  "modes": ["super_realistic"],
  "dimensions": [
    "attachment_intimacy_avoidance",
    "trust_suspicion_sensitivity",
    "info_concealment_tendency",
    "desire_novelty_need",
    "attachment_vulnerability_fear",
    "communication_defensiveness",
    "boundary_double_standard"
  ],
  "options": [
    {
      "id": "intimacy_vs_freedom",
      "value": "A",
      "label": "想要亲密，但又害怕失去自由。",
      "dimension_effects": {
        "attachment_intimacy_avoidance": 6,
        "attachment_independence_need": 6
      },
      "report_tags": ["intimacy_freedom_conflict"]
    },
    {
      "id": "trust_vs_suspicion",
      "value": "B",
      "label": "想相信对方，但又忍不住怀疑。",
      "dimension_effects": {
        "trust_suspicion_sensitivity": 8,
        "trust_checking_impulse": 5
      },
      "report_tags": ["trust_suspicion_conflict"]
    },
    {
      "id": "honesty_vs_conflict",
      "value": "C",
      "label": "想诚实，但又害怕冲突。",
      "dimension_effects": {
        "info_concealment_tendency": 6,
        "communication_conflict_avoidance": 6
      },
      "report_tags": ["honesty_conflict_tension"]
    },
    {
      "id": "stability_vs_novelty",
      "value": "D",
      "label": "想稳定，但又需要新鲜感。",
      "dimension_effects": {
        "desire_novelty_need": 8,
        "desire_stability_preference": 4
      },
      "report_tags": ["stability_novelty_conflict"]
    },
    {
      "id": "understood_vs_vulnerable",
      "value": "E",
      "label": "想被理解，但不太会表达脆弱。",
      "dimension_effects": {
        "attachment_vulnerability_fear": 8,
        "desire_emotional_validation_hunger": 5
      },
      "report_tags": ["vulnerability_expression_gap"]
    },
    {
      "id": "mature_vs_emotional",
      "value": "F",
      "label": "想成熟沟通，但情绪上来会失控或逃避。",
      "dimension_effects": {
        "communication_defensiveness": 7,
        "emotion_impulsivity": 6,
        "emotion_shutdown_tendency": 5
      },
      "report_tags": ["conflict_behavior_gap"]
    },
    {
      "id": "fair_rules_vs_double_standard",
      "value": "G",
      "label": "想让规则公平，但现实里会双标。",
      "dimension_effects": {
        "boundary_double_standard": 9,
        "self_discrepancy_awareness": 5
      },
      "report_tags": ["double_standard_awareness"]
    },
    {
      "id": "no_clear_conflict",
      "value": "H",
      "label": "暂时没有明显核心矛盾。",
      "dimension_effects": {
        "self_reflection_capacity": -2
      },
      "report_tags": ["no_clear_core_conflict"]
    }
  ],
  "reason_tags": [],
  "reverse_pair_id": null,
  "perspective_pair_id": null,
  "dimension_effects": {},
  "scoring": {
    "base_weight": 0.85,
    "primary_choice_weight": 1.0,
    "other_choice_weight": 0.45,
    "evidence_quality": "medium"
  },
  "confidence": {
    "enabled": true,
    "default": 70,
    "affects_weight": true
  },
  "report_tags": ["final_self_summary"]
}
```

## 15. 从 JSON 生成结果

### 15.1 生成 `self_report_profile`

流程：

1. 读取 `questionnaire_meta` 和启用的 `modules`；
2. 根据问卷模式筛选 `questions`；
3. 记录玩家答案为标准 answer record；
4. 累积 `dimension_scores`、`confidence_scores`、标签和报告输入；
5. 输出初始自述档案。

```json
{
  "self_report_profile": {
    "questionnaire_id": "if_super_realistic_questionnaire_v0_1",
    "mode": "super_realistic",
    "answered_questions": 150,
    "dimension_scores": {},
    "confidence_scores": {},
    "visible_tags": [],
    "hidden_tags": [],
    "report_sections": []
  }
}
```

### 15.2 生成 `dimension_scores`

每个维度从 50 开始。

```text
dimension_score = 50
dimension_score += option_effect × selection_mode_weight × confidence_factor
dimension_score += secondary_effect × secondary_choice_weight
dimension_score += reason_effect × reason_tag_weight
dimension_score = clamp(0, 100)
```

不同题型处理：

- `forced_single`：只处理 `primary_choice`；
- `primary_with_secondary`：主选项 + 次选项 + 原因标签；
- `multi_select`：按 `1 / sqrt(selected_count)` 分散权重；
- `multi_with_primary`：主因权重大，其他选项中低；
- `ranked_multi`：按排序递减；
- `weighted_multi`：按玩家分配比例；
- `slider`：把 0-100 转为中心化值；
- `axis_2d`：分别处理 x/y 轴；
- `reverse_check`：主要影响可信度和差异标签；
- `open_text`：MVP 不自动计分。

### 15.3 生成 `confidence_scores`

每个维度同时记录：

```json
{
  "score": 76,
  "confidence": "medium_high",
  "evidence_count": 7,
  "conflict_count": 1,
  "evidence_sources": ["Q017", "Q031", "Q118"]
}
```

规则：

- 情境题、配对题、坐标题证据质量高；
- 自评题证据质量中低；
- 单题证据不足时只能给低可信度；
- 反向验证发现矛盾时增加 `conflict_count`；
- 低覆盖维度在报告中必须保留“不确定”表达。

### 15.4 生成 `visible_tags`

`visible_tags` 是玩家可读标签，来自高可信维度、模块分数和报告标签。

示例：

```json
{
  "visible_tags": [
    "需要稳定回应",
    "重视边界说明",
    "压力下容易选择性表达"
  ]
}
```

触发建议：

```text
dimension_score >= 70
confidence_score >= medium
evidence_count >= 3
```

### 15.5 生成 `hidden_tags`

`hidden_tags` 给系统使用，不直接给玩家定性。

示例：

```json
{
  "hidden_tags": [
    "high_reassurance_need",
    "suspicion_under_ambiguity",
    "pressure_based_concealment",
    "partial_truth_pattern"
  ]
}
```

隐藏标签用途：

- 事件触发权重；
- NPC 反应；
- 谎言破绽；
- 关系阶段结算；
- 后续游戏行为修正。

### 15.6 生成 `report_sections`

`report_sections` 由 `modules`、`report_tags`、`dimension_scores` 和 `confidence_scores` 共同生成。

```json
{
  "report_sections": [
    {
      "id": "main_profile",
      "title": "你的主画像",
      "template_id": "main_profile_high_reassurance",
      "source_tags": ["high_reassurance_need", "pressure_based_concealment"]
    },
    {
      "id": "trust_boundary",
      "title": "信任与边界",
      "template_id": "trust_boundary_sensitive",
      "source_dimensions": ["trust_suspicion_sensitivity", "boundary_double_standard"]
    }
  ]
}
```

报告不展示 128 维全部底层分数，只展示模块摘要、关键倾向、风险场景、适合/不适合相处模式和游戏内初始标签。

## 16. MVP 必须字段与后续扩展字段

### 16.1 MVP 必须字段

| 层级 | 字段 |
| --- | --- |
| 顶层 | `questionnaire_meta`、`modules`、`questions`、`scoring` |
| meta | `id`、`version`、`title`、`default_mode`、`supported_modes`、`score_range`、`default_dimension_score` |
| module | `id`、`title`、`order`、`modes`、`target_question_ids`、`primary_dimensions`、`report_section_id` |
| question | `id`、`module_id`、`title`、`prompt`、`question_type`、`selection_mode`、`required`、`allow_skip`、`modes`、`dimensions`、`options`、`dimension_effects`、`scoring`、`confidence`、`report_tags` |
| option | `id`、`value`、`label`、`dimension_effects`、`report_tags` |
| scoring | `base_weight`、`evidence_quality` |
| confidence | `enabled`、`default`、`affects_weight` |

### 16.2 建议 MVP 支持但可为空

| 字段 | 说明 |
| --- | --- |
| `reason_tags` | Q017、Q051 这类题需要，但部分题可以为空 |
| `reverse_pair_id` | MVP 可先保存字段，不立即做完整一致性算法 |
| `perspective_pair_id` | MVP 可先保存字段，不立即做完整双标算法 |
| `axis` | `axis_2d` 必需，但非坐标题为空 |
| `scale` | `slider` 必需，但非滑条题为空 |

### 16.3 后续扩展字段

| 字段 | 说明 |
| --- | --- |
| `localization` | 多语言文本 |
| `editor_notes` | 编辑器和人工校对备注 |
| `coverage_level` | 覆盖率文档中的高/中/低/空缺 |
| `risk_level` | 题目风险等级 |
| `dependency_rules` | 题目显示条件 |
| `skip_logic` | 跳题逻辑 |
| `randomization_group` | 随机出题分组 |
| `answer_time_expected` | 预估答题时间 |
| `open_text_parse_rules` | 未来 AI 或本地文本解析规则 |
| `calibration_stats` | 后续真实试玩统计校准 |

## 17. 非目标

本文件不做：

- 不实现 Python 读取器；
- 不新增真实 JSON 配置文件；
- 不改现有 Q001-Q150 题库内容；
- 不校准最终权重；
- 不接 AI 解析开放文本；
- 不把问卷做成心理诊断；
- 不把单题结果写成严重标签。

## 18. 后续建议

下一步若进入实现阶段，建议按以下顺序：

1. 先把 Q001-Q030 转成小型 JSON 样例；
2. 写只读 loader，验证 schema 能被加载；
3. 跑最小计分流程，生成 `dimension_scores` 和 `confidence_scores`；
4. 再扩展到 Q001-Q150；
5. 最后接报告模板和游戏内初始标签。

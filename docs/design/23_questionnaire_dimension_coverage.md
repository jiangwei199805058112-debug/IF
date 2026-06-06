# 问卷维度覆盖率检查 v0.1

本文档检查 Q001-Q150 超级真实版题库对 128维主表的覆盖情况。它承接：

- `docs/design/16_questionnaire_dimension_table.md`
- `docs/design/18_super_realistic_question_bank.md`
- `docs/design/18_super_realistic_question_bank_part2.md`
- `docs/design/18_super_realistic_question_bank_part3.md`
- `docs/design/18_super_realistic_question_bank_part4.md`
- `docs/design/22_questionnaire_scoring_rules.md`

本文档只做覆盖率审查，不修改控制台原型运行逻辑。

## 1. 检查目标

本轮检查回答四个问题：

1. Q001-Q150 是否已经覆盖 128维主表的大多数核心维度；
2. 哪些维度覆盖充足，可以直接进入计分和报告；
3. 哪些维度只有间接证据，暂时只能作为低可信度维度；
4. 是否需要补充 Q151-Q180，而不是继续盲目加题。

## 2. 覆盖等级定义

| 等级 | 标记 | 定义 | 后续处理 |
| --- | --- | --- | --- |
| 高 | `高` | 有 4 题以上直接或强相关覆盖，且至少包含情境题/配对题/滑条/排序中的两类 | 可以进入报告主标签和事件权重 |
| 中 | `中` | 有 2-3 题直接覆盖，或有多个强间接题覆盖 | 可计分，但报告需要保留可信度提示 |
| 低 | `低` | 只有 1 题或主要是间接覆盖 | 暂不适合生成强标签，可作为弱证据 |
| 空缺 | `空缺` | Q001-Q150 基本没有覆盖 | 若该维度重要，应补题 |

说明：覆盖等级不是维度重要性。低覆盖只说明当前题库证据不足，不说明该维度不重要。

## 3. 总体结论

Q001-Q150 已经能支撑超级真实版问卷的第一版结构，尤其在以下模块覆盖较强：

- 亲密关系与依恋；
- 信任、怀疑与安全感；
- 诚实、隐瞒与信息管理；
- 冲突与沟通；
- 控制、边界与权力感；
- 欲望、新鲜感与忠诚；
- 道德、责任与后果意识；
- 数字生活与社交媒体。

覆盖不足主要集中在：

- 基础人格与气质中的 Big Five 类维度；
- 自我认知与自尊中的自我接纳、自尊稳定、形象管理；
- 社交方式中的社交能量、亲和表达、孤独耐受；
- 现实生活稳定性中的生活自理、生活一致性；
- 风险行为与危机模式中的依赖危机、边界侵犯风险；
- 价值观与人生取向中的精神共鸣、地位比较、家庭取向部分虽然有题，但仍可更系统化。

因此，不建议继续无方向加题。若要补题，应补 **Q151-Q180 定向补强题**，重点覆盖低覆盖维度。

## 4. 128维覆盖总表

### A01 基础人格与气质

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `temperament_emotional_sensitivity` | 中 | Q017、Q118、Q131、Q145 | 消息、社交忽略和在线未回能间接覆盖，但缺少单独气质题。 |
| `temperament_emotional_stability` | 中 | Q073、Q074、Q076、Q081、Q145 | 冲突和压力题覆盖较好，但更偏关系场景。 |
| `temperament_extraversion` | 低 | Q002、Q111、Q117、Q120 | 只通过社交网络间接推断，缺少主动社交倾向题。 |
| `temperament_openness` | 低 | Q008、Q050、Q141 | 对新关系模式开放度覆盖不足。 |
| `temperament_conscientiousness` | 中 | Q101、Q121、Q122 | 承诺和时间管理有覆盖，但基础尽责性仍偏间接。 |
| `temperament_agreeableness` | 低 | Q077、Q080、Q102 | 主要由道歉、倾听、补偿间接推断。 |
| `temperament_risk_tolerance` | 低 | Q090、Q099、Q109 | 风险决策有覆盖，但基础冒险耐受不足。 |
| `temperament_sensation_seeking` | 中 | Q084、Q095、Q090 | 新鲜感和刺激需求覆盖中等。 |

**判断**：A01 是当前最需要补强的大类之一。现有题库更偏“关系场景人格”，而不是基础气质测量。建议补 Q151-Q158。

### A02 自我认知与自尊

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `self_esteem_stability` | 低 | Q022、Q075、Q119 | 通过被需要、面子和比较间接覆盖，不足。 |
| `self_acceptance` | 低 | Q146、Q147 | 主要依赖开放文本，当前不自动计分。 |
| `self_reflection_capacity` | 中 | Q014、Q079、Q142、Q149 | 自我反省和模式觉察覆盖中等。 |
| `self_justification_tendency` | 高 | Q063、Q066、Q100、Q104、Q108、Q144 | 自我合理化覆盖较强。 |
| `self_face_sensitivity` | 中 | Q023、Q075、Q115、Q124 | 面子、公共评价和经济硬撑有覆盖。 |
| `self_validation_need` | 中 | Q022、Q088、Q092、Q119 | 被认可和情绪价值覆盖中等。 |
| `self_image_management` | 低 | Q059、Q115、Q147 | 人设维护和形象管理覆盖不足。 |
| `self_discrepancy_awareness` | 高 | Q030、Q065-Q068、Q083、Q138、Q143、Q144 | 自述/情境差异覆盖强。 |

**判断**：A02 的自我合理化和自我差异检测足够强，但自我接纳、自尊稳定、形象管理不足。建议补 3-5 题。

### A03 情绪调节与压力反应

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `emotion_stress_tolerance` | 中 | Q121、Q128、Q145 | 压力期表现覆盖中等。 |
| `emotion_anxiety_tendency` | 中 | Q017、Q027、Q031、Q131 | 焦虑通过不安场景间接覆盖。 |
| `emotion_anger_control` | 中 | Q074、Q076、Q139 | 愤怒控制覆盖中等，但可更细化。 |
| `emotion_shutdown_tendency` | 高 | Q017、Q073、Q114、Q145 | 冷处理和关机风险覆盖强。 |
| `emotion_impulsivity` | 高 | Q074、Q076、Q090、Q106 | 冲动、拉黑、破罐破摔覆盖较强。 |
| `emotion_recovery_speed` | 高 | Q026、Q081、Q012 | 信任修复和情绪恢复有直接题。 |
| `emotion_suppression_tendency` | 中 | Q071、Q039、Q075 | 压抑、忍住、记账覆盖中等。 |
| `emotion_reassurance_need` | 高 | Q017、Q028、Q046、Q082、Q145 | 安抚需求覆盖强。 |

**判断**：A03 覆盖较好，不需要优先补题。

### A04 社交方式

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `social_initiative` | 低 | Q002、Q117 | 社交主动性覆盖不足。 |
| `social_energy_level` | 空缺 | 无明确题 | 当前没有“社交后获得能量还是消耗”的直接题。 |
| `social_warmth_expression` | 低 | Q080、Q118 | 亲和表达主要间接覆盖。 |
| `social_boundary_awareness` | 中 | Q041、Q043、Q087、Q093 | 异性/暧昧边界覆盖中等。 |
| `social_dependency` | 中 | Q004、Q019、Q118 | 社交依赖和联系需求有覆盖。 |
| `social_solitude_tolerance` | 低 | Q020、Q125 | 孤独耐受主要从个人空间和作息推断。 |
| `social_reputation_sensitivity` | 高 | Q007、Q111、Q115、Q119、Q120 | 名声和公开展示覆盖强。 |
| `social_circle_overlap_need` | 高 | Q002、Q112、Q116、Q120 | 圈子融合覆盖强。 |

**判断**：A04 需要补强社交能量、亲和表达、主动性和孤独耐受。建议补 4-5 题。

### A05 亲密关系与依恋

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `attachment_abandonment_anxiety` | 高 | Q017、Q018、Q027、Q118、Q125、Q131 | 被弃焦虑覆盖强。 |
| `attachment_intimacy_avoidance` | 高 | Q018、Q027、Q029、Q095 | 回避亲密覆盖强。 |
| `attachment_closeness_need` | 高 | Q004、Q019、Q022、Q128 | 亲密需求覆盖强。 |
| `attachment_independence_need` | 高 | Q018、Q020、Q030、Q045、Q095 | 独立需求覆盖强。 |
| `attachment_vulnerability_fear` | 高 | Q021、Q023、Q027、Q146、Q147 | 暴露脆弱恐惧覆盖强。 |
| `attachment_reliance_comfort` | 中 | Q023、Q024 | 依赖舒适度有直接题，但数量一般。 |
| `attachment_repair_receptivity` | 高 | Q003、Q008、Q012、Q016、Q026 | 亲密修复接受度覆盖强。 |
| `attachment_commitment_pace` | 高 | Q001、Q008、Q025、Q029、Q141 | 承诺节奏覆盖强。 |

**判断**：A05 是覆盖最完整的大类之一。

### A06 信任、怀疑与安全感

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `trust_baseline` | 中 | Q003、Q031、Q036、Q140 | 基础信任覆盖中等。 |
| `trust_suspicion_sensitivity` | 高 | Q031、Q032、Q034、Q036、Q037、Q114、Q133、Q134 | 怀疑敏感覆盖强。 |
| `trust_checking_impulse` | 高 | Q031、Q033、Q038、Q062、Q068、Q114 | 查证冲动覆盖强。 |
| `trust_explanation_acceptance` | 高 | Q012、Q031、Q038、Q058、Q082 | 解释接受度覆盖强。 |
| `trust_old_wound_memory` | 高 | Q010、Q012、Q015、Q034、Q039、Q148 | 旧伤记忆覆盖强。 |
| `trust_projection_tendency` | 中 | Q040、Q094 | 投射倾向有直接题，但数量可再补。 |
| `trust_loyalty_sensitivity` | 高 | Q034、Q041、Q043、Q087、Q093、Q120、Q132、Q136 | 忠诚信任敏感覆盖强。 |
| `trust_privacy_trust` | 中 | Q047、Q067、Q135 | 隐私信任覆盖中等。 |

**判断**：A06 覆盖充足。

### A07 诚实、隐瞒与信息管理

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `info_honesty_tendency` | 高 | Q051、Q053、Q064、Q065 | 诚实倾向覆盖强。 |
| `info_concealment_tendency` | 高 | Q035、Q051、Q052、Q055、Q063、Q064、Q145 | 隐瞒倾向覆盖强。 |
| `info_partial_truth_tendency` | 高 | Q051、Q054、Q065、Q066 | 半真半假覆盖强。 |
| `info_lie_skill` | 中 | Q053、Q059 | 撒谎能力有直接题，但数量一般。 |
| `info_guilt_after_deception` | 中 | Q060、Q102 | 欺瞒后愧疚覆盖中等偏低。 |
| `info_exposure_reaction` | 高 | Q057、Q103 | 被揭穿反应题直接，配合道德暴露题可用。 |
| `info_secret_management` | 高 | Q055、Q056、Q059、Q096、Q134 | 秘密管理覆盖强。 |
| `info_transparency_preference` | 高 | Q061、Q135、Q136、Q138 | 透明偏好覆盖强。 |

**判断**：A07 覆盖充足。若补题，可只补愧疚和长期内耗。

### A08 冲突与沟通

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `communication_directness` | 高 | Q021、Q071、Q122、Q123 | 直接沟通覆盖较强。 |
| `communication_conflict_avoidance` | 高 | Q014、Q051、Q071、Q073、Q079、Q122 | 冲突回避覆盖强。 |
| `communication_defensiveness` | 高 | Q051、Q057、Q072、Q080、Q143 | 防御性覆盖强。 |
| `communication_apology_capacity` | 高 | Q077、Q102 | 道歉能力直接覆盖，数量少但相关强。 |
| `communication_repair_initiative` | 高 | Q028、Q078、Q102、Q145 | 修复主动性覆盖强。 |
| `communication_meta_discussion` | 高 | Q050、Q079、Q116、Q149 | 关系复盘覆盖强。 |
| `communication_listening_capacity` | 高 | Q080、Q104 | 倾听能力直接覆盖，数量较少但关键。 |
| `communication_cruelty_under_conflict` | 高 | Q013、Q039、Q075、Q076、Q107 | 冲突伤人覆盖强。 |

**判断**：A08 覆盖充足。

### A09 控制、边界与权力感

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `boundary_control_need` | 高 | Q010、Q046、Q049 | 控制欲覆盖中高。 |
| `boundary_possessiveness` | 高 | Q015、Q034、Q041、Q049 | 占有欲覆盖强。 |
| `boundary_respect` | 中 | Q013、Q050、Q067、Q098 | 边界尊重覆盖中等。 |
| `boundary_double_standard` | 高 | Q007、Q035、Q042、Q046、Q047、Q048、Q054、Q056、Q061、Q069、Q094、Q135 | 双标覆盖很强。 |
| `boundary_manipulation_tendency` | 中 | Q049、Q107 | 操控倾向覆盖中等偏低。 |
| `boundary_dominance_need` | 低 | Q024 | 支配需求覆盖不足。 |
| `boundary_autonomy_assertion` | 中 | Q020、Q045 | 自主主张覆盖中等。 |
| `boundary_rule_negotiation` | 高 | Q042、Q045、Q050 | 边界规则协商覆盖强。 |

**判断**：A09 整体可用，但支配需求和操控倾向可补。

### A10 欲望、新鲜感与忠诚

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `desire_novelty_need` | 高 | Q084、Q092、Q095、Q150 | 新鲜感覆盖强。 |
| `desire_stability_preference` | 中 | Q085、Q141 | 稳定偏好覆盖中等。 |
| `desire_temptation_resistance` | 高 | Q086、Q088、Q090、Q096、Q143 | 诱惑抵抗覆盖强。 |
| `desire_instant_gratification` | 高 | Q090、Q099、Q109 | 即时满足覆盖中高。 |
| `desire_alternative_seeking` | 高 | Q011、Q016、Q088、Q089、Q107 | 替代倾向覆盖强。 |
| `desire_emotional_validation_hunger` | 高 | Q021、Q086、Q088、Q092、Q145 | 情绪价值饥渴覆盖强。 |
| `desire_physical_attraction_weight` | 中 | Q092 | 有权重题，但只有一题直接覆盖。 |
| `desire_loyalty_identity` | 高 | Q091、Q094 | 忠诚自我认同直接覆盖，但数量一般。 |

**判断**：A10 覆盖较强。若补题，可补身体/外貌吸引权重和长期稳定经营。

### A11 道德、责任与后果意识

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `moral_responsibility` | 高 | Q077、Q097、Q105、Q109、Q122 | 责任承担覆盖强。 |
| `moral_line_clarity` | 高 | Q013、Q054、Q089、Q091、Q093、Q098 | 底线清晰度覆盖强。 |
| `moral_consequence_forecast` | 高 | Q053、Q090、Q096、Q099、Q109 | 后果预判覆盖强。 |
| `moral_flexibility` | 高 | Q100、Q108 | 道德弹性直接覆盖。 |
| `moral_commitment_credibility` | 高 | Q085、Q101、Q149 | 承诺可信度覆盖中高。 |
| `moral_compensation_willingness` | 高 | Q028、Q058、Q060、Q097、Q102 | 补偿意愿覆盖强。 |
| `moral_accountability_under_exposure` | 高 | Q057、Q077、Q103、Q108 | 暴露后负责度覆盖强。 |
| `moral_harm_awareness` | 高 | Q015、Q060、Q077、Q080、Q104、Q149 | 伤害觉察覆盖强。 |

**判断**：A11 覆盖充足。

### A12 价值观与人生取向

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `values_achievement_need` | 中 | Q006、Q128 | 成就/工作学业压力有覆盖，但不够系统。 |
| `values_security_need` | 高 | Q008、Q027、Q085 | 安稳需求覆盖中高。 |
| `values_freedom_need` | 高 | Q008、Q020、Q029、Q045、Q061 | 自由需求覆盖强。 |
| `values_belonging_need` | 高 | Q001、Q022、Q044 | 归属需求覆盖中高。 |
| `values_material_importance` | 高 | Q092、Q105、Q119、Q123 | 物质重视覆盖强。 |
| `values_spiritual_resonance_need` | 低 | Q092、Q146 | 精神共鸣主要间接或开放文本覆盖。 |
| `values_family_orientation` | 中 | Q010、Q025、Q126、Q141 | 家庭取向覆盖中等。 |
| `values_status_comparison` | 中 | Q092、Q119、Q126、Q129 | 地位比较覆盖中等。 |

**判断**：A12 大体可用，但精神共鸣需要补直接题，成就需求也可补。

### A13 现实生活稳定性

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `stability_time_management` | 高 | Q121、Q122、Q130 | 时间管理覆盖强。 |
| `stability_money_management` | 高 | Q105、Q123、Q124、Q130 | 金钱管理覆盖强。 |
| `stability_sleep_rhythm` | 中 | Q125、Q130 | 作息覆盖中等。 |
| `stability_self_care` | 低 | Q006、Q130 | 生活自理只有间接覆盖。 |
| `stability_environmental_pressure` | 高 | Q006、Q010、Q129、Q130 | 环境压力覆盖强。 |
| `stability_adaptability` | 中 | Q005、Q129 | 适应能力覆盖中等偏低。 |
| `stability_resource_availability` | 高 | Q005、Q006、Q024、Q121、Q128 | 资源可用性覆盖强。 |
| `stability_life_consistency` | 低 | Q138、Q143、Q144 | 生活一致性主要靠自述/差异检测，缺生活习惯题。 |

**判断**：A13 可支撑现实压力模块，但生活自理和生活一致性需要补题。

### A14 数字生活与社交媒体

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `digital_phone_privacy_need` | 高 | Q036、Q037、Q047、Q061、Q135 | 手机隐私覆盖强。 |
| `digital_response_norm` | 高 | Q004、Q005、Q019、Q125、Q131、Q138 | 回复规范覆盖强。 |
| `digital_social_media_display` | 高 | Q007、Q025、Q028、Q044、Q119、Q136 | 社媒展示覆盖强。 |
| `digital_alt_account_tendency` | 高 | Q002、Q056、Q134 | 小号/备用账号覆盖中高。 |
| `digital_location_transparency` | 中 | Q048、Q062 | 定位透明覆盖中等。 |
| `digital_evidence_awareness` | 高 | Q037、Q055、Q062、Q132、Q133、Q137 | 数字证据意识覆盖强。 |
| `digital_online_flirt_boundary` | 高 | Q043、Q087、Q093、Q132 | 线上暧昧边界覆盖强。 |
| `digital_availability_pressure` | 高 | Q131、Q137 | 在线可得压力有直接题，数量一般但关键。 |

**判断**：A14 覆盖充足。

### A15 家庭、成长与关系脚本

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `family_parental_influence` | 中 | Q126、Q127 | 家庭影响有直接题。 |
| `family_conflict_model` | 中 | Q139 | 原生冲突模板有直接题，但只有一题。 |
| `family_attachment_history` | 中 | Q140 | 成长安全感有直接题，但只有一题。 |
| `family_obligation_pressure` | 中 | Q006、Q126、Q130 | 家庭义务压力有覆盖。 |
| `family_relationship_script` | 高 | Q009、Q141 | 关系脚本有覆盖。 |
| `family_approval_need` | 中 | Q111、Q126、Q127 | 家庭认可需求覆盖中等。 |
| `family_privacy_boundary` | 中 | Q127 | 家庭边界只有一题直接覆盖。 |
| `family_repetition_awareness` | 中 | Q142 | 模式重复觉察有直接题。 |

**判断**：A15 可用但偏薄。若游戏重视家庭线，建议补 4-6 题。

### A16 风险行为与危机模式

| 维度ID | 覆盖等级 | 主要题号 | 结论 |
| --- | --- | --- | --- |
| `risk_breakdown_tendency` | 中 | Q074、Q106 | 崩溃倾向有危机题，但还可细化。 |
| `risk_sabotage_tendency` | 高 | Q074、Q076、Q106 | 自毁/破坏覆盖较强。 |
| `risk_revenge_tendency` | 高 | Q107、Q133 | 报复倾向有直接题和数字回应题。 |
| `risk_escalation_under_exposure` | 高 | Q103、Q106 | 暴露后升级覆盖强。 |
| `risk_dependency_crisis` | 低 | Q022、Q145 | 依赖危机覆盖不足，更多是安抚需求间接推断。 |
| `risk_avoidant_disappearance` | 高 | Q073、Q145 | 回避消失覆盖强。 |
| `risk_boundary_violation` | 中 | Q033、Q062、Q068 | 边界侵犯风险覆盖中等，但缺更明确的越界行为题。 |
| `risk_repeat_pattern` | 高 | Q009、Q011、Q016、Q142、Q148 | 问题重复风险覆盖强。 |

**判断**：A16 关键危机维度大多可用，但依赖危机和边界侵犯风险需要补题。

## 5. 覆盖不足维度清单

### 5.1 空缺或接近空缺

| 维度ID | 问题 | 建议 |
| --- | --- | --- |
| `social_energy_level` | 没有直接题 | 补“社交后充电/耗电”题。 |

### 5.2 低覆盖优先补强

| 维度ID | 当前问题 | 建议补题方向 |
| --- | --- | --- |
| `temperament_extraversion` | 只通过社交事件间接推断 | 补主动认识人、主动约见、社交频率题。 |
| `temperament_openness` | 新模式接受度不足 | 补对开放沟通、非传统相处方式、关系实验的接受度题。 |
| `temperament_agreeableness` | 合作/体谅倾向间接 | 补让步、共情、协商时是否优先照顾双方题。 |
| `temperament_risk_tolerance` | 风险耐受不足 | 补不确定关系、暧昧风险、公开风险承受题。 |
| `self_esteem_stability` | 主要依赖比较和面子 | 补被冷落/否定后自我价值是否波动题。 |
| `self_acceptance` | 依赖开放文本，不自动计分 | 补缺点、过去、失败是否能坦白题。 |
| `self_image_management` | 人设维护覆盖不足 | 补是否经营深情/稳定/优秀形象题。 |
| `social_initiative` | 社交主动性不足 | 补主动认识、主动联系、主动组织约会题。 |
| `social_warmth_expression` | 亲和表达不足 | 补表达关心、夸奖、善意反馈题。 |
| `social_solitude_tolerance` | 独处稳定度不足 | 补单独一天无人联系时的反应题。 |
| `boundary_dominance_need` | 支配需求不足 | 补关系中谁定规则、谁掌控节奏题。 |
| `values_spiritual_resonance_need` | 精神共鸣不足 | 补深聊、三观、理解感在长期关系中的权重题。 |
| `stability_self_care` | 生活自理不足 | 补生活混乱、健康、作息、事务处理题。 |
| `stability_life_consistency` | 生活一致性不足 | 补自述生活状态和真实执行差异题。 |
| `risk_dependency_crisis` | 依赖危机不足 | 补分手/冷淡后生活功能是否失衡题。 |

## 6. Q151-Q180 定向补题建议

如果继续补题，不建议继续随机扩展，而应围绕低覆盖维度补 30 题。

### Q151-Q158：基础人格与气质补强

| 题号 | 目标维度 | 题型建议 | 主题 |
| --- | --- | --- | --- |
| Q151 | `temperament_extraversion`、`social_initiative` | `slider` | 主动认识人和主动发起见面 |
| Q152 | `social_energy_level` | `forced_single` | 社交后是充电还是耗电 |
| Q153 | `temperament_openness` | `ranked_multi` | 接受新的相处方式和边界协议 |
| Q154 | `temperament_agreeableness` | `scenario_choice` | 分歧中是否愿意让步和共情 |
| Q155 | `temperament_risk_tolerance` | `axis_2d` | 关系不确定性与风险承受 |
| Q156 | `temperament_emotional_sensitivity` | `slider` | 对语气、表情、回复节奏变化的敏感度 |
| Q157 | `temperament_conscientiousness` | `slider` | 承诺、准时、执行稳定度 |
| Q158 | `temperament_sensation_seeking` | `slider` | 戏剧性、刺激感、反差吸引 |

### Q159-Q165：自我认知与社交表达补强

| 题号 | 目标维度 | 题型建议 | 主题 |
| --- | --- | --- | --- |
| Q159 | `self_esteem_stability` | `scenario_choice` | 被冷落/否定后自我价值波动 |
| Q160 | `self_acceptance` | `primary_with_secondary` | 是否愿意坦白缺点、失败和过去 |
| Q161 | `self_image_management` | `multi_with_primary` | 是否经营深情、稳定、优秀人设 |
| Q162 | `social_warmth_expression` | `slider` | 是否自然表达关心、夸奖和善意 |
| Q163 | `social_solitude_tolerance` | `scenario_choice` | 一天没人联系时是否稳定 |
| Q164 | `values_spiritual_resonance_need` | `weighted_multi` | 精神共鸣在关系中的权重 |
| Q165 | `boundary_dominance_need` | `axis_2d` | 关系节奏和规则由谁掌控 |

### Q166-Q172：现实生活稳定性补强

| 题号 | 目标维度 | 题型建议 | 主题 |
| --- | --- | --- | --- |
| Q166 | `stability_self_care` | `slider` | 生活自理、健康、基础秩序 |
| Q167 | `stability_life_consistency` | `reverse_check` | 自称稳定与实际作息/执行差异 |
| Q168 | `stability_adaptability` | `scenario_choice` | 临时变化、取消约会、计划变动 |
| Q169 | `values_achievement_need` | `weighted_multi` | 事业/学业与关系的权重分配 |
| Q170 | `values_status_comparison` | `slider` | 学历、收入、外貌、圈层比较 |
| Q171 | `family_privacy_boundary` | `scenario_choice` | 家庭介入时能否保护伴侣边界 |
| Q172 | `family_attachment_history` | `reverse_check` | 成长安全感与当前关系反应对照 |

### Q173-Q180：危机模式补强

| 题号 | 目标维度 | 题型建议 | 主题 |
| --- | --- | --- | --- |
| Q173 | `risk_dependency_crisis` | `slider` | 关系不稳时生活功能是否失衡 |
| Q174 | `risk_boundary_violation` | `scenario_choice` | 极度不安时是否越界查证、逼问、跟踪线索 |
| Q175 | `risk_breakdown_tendency` | `primary_with_secondary` | 极端压力下崩溃、失联、失控表达 |
| Q176 | `boundary_manipulation_tendency` | `reverse_check` | 是否用冷淡、测试、奖惩影响对方 |
| Q177 | `trust_projection_tendency` | `reverse_check` | 自己可能隐瞒时是否更怀疑对方 |
| Q178 | `desire_physical_attraction_weight` | `weighted_multi` | 外貌/身体吸引与精神/稳定吸引权重 |
| Q179 | `info_guilt_after_deception` | `scenario_choice` | 隐瞒未暴露时是否内耗、补偿或继续压住 |
| Q180 | 综合低覆盖校验 | `multi_with_primary` | 自我认为最不稳定的低覆盖区域 |

## 7. 是否必须补 Q151-Q180

当前结论：**不是必须立刻补。**

Q001-Q150 已经可以支撑第一版超级真实问卷、报告模板和计分规则。Q151-Q180 的价值是：

- 提高 128维覆盖完整度；
- 减少 Big Five/基础气质类维度空缺；
- 提高现实稳定性和危机模式的可信度；
- 让报告里的“证据不足维度”变少。

如果下一步目标是尽快做可运行原型，应先做：

```text
docs/design/24_questionnaire_json_schema.md
```

如果下一步目标是继续提高真实度，应先补：

```text
Q151-Q180 定向补题
```

## 8. 本轮发现的问题

本轮覆盖率检查没有发现新的严重结构冲突，但确认以下事实：

1. 128维不是每个维度都已经高覆盖；
2. 当前题库重点明显偏向亲密关系、信任、边界、隐瞒、冲突、忠诚和现实压力；
3. 基础人格、普通社交、生活自理、自尊稳定和部分危机模式仍偏薄；
4. 后续若进行 JSON 配置化，应在每个维度字段中保留 `confidence` 和 `evidence_count`，避免把低覆盖维度强行写成高可信报告。

## 9. 下一步建议

建议二选一：

### 路线 A：先配置化

```text
docs/design/24_questionnaire_json_schema.md
```

目标：把题库转换成可实现的数据结构，后续才能接控制台问卷原型。

### 路线 B：先补覆盖

```text
docs/design/18_super_realistic_question_bank_part5.md
```

目标：按本文件的 Q151-Q180 建议补充低覆盖维度。

推荐顺序：先做 24，再决定是否做 part5。因为 JSON schema 会反过来约束题库格式，避免继续写出难以实现的题。
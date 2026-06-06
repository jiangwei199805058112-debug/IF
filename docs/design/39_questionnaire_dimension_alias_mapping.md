# 问卷维度别名映射表

本文档用于把 `docs/design/36_questionnaire_expansion_candidate_pool.md` 中出现的新候选维度、系统变量和报告标签，映射到 `docs/design/16_questionnaire_dimension_table.md` 中已经定义的 128 维主表。

它的目的不是扩展 128 维，而是在后续真正修改 `if_game/data/questionnaire_mvp.json` 前，先解决一个实现风险：

```text
候选题里有很多新变量名，但它们未必已经存在于 128 维主表。
如果直接写进 questionnaire_mvp.json 的 dimensions 字段，scripts/check_questionnaire_dimension_ids.py 可能失败。
```

---

## 1. 核心规则

### 1.1 `dimensions` 只能使用 128 维主表中的正式 ID

后续修改 `questionnaire_mvp.json` 时：

```text
question.dimensions
option.scoring.dimension_effects
```

应优先使用 `docs/design/16_questionnaire_dimension_table.md` 中的正式 ID。

### 1.2 新系统变量可以作为内部字段，但不要直接作为问卷维度

例如：

```text
self_disclosure_willingness
privacy_boundary_strength
safe_but_bored_pattern
communal_orientation
```

这些概念可以继续用于设计文档、报告标签、聚合器输入或调试字段，但在问卷 JSON 的 `dimensions` 中应映射到已有 128 维。

### 1.3 三类映射

| 类型 | 含义 | 后续处理 |
| --- | --- | --- |
| `direct_alias` | 可较稳定地映射到 1-2 个正式维度 | 可直接用于 MVP |
| `composite_alias` | 需要多个正式维度共同表达 | 问卷计分时拆分成多个 dimension_effects |
| `runtime_only` | 更适合作为游戏行为/事件聚合结果，不适合作为问卷维度 | 不写进 questionnaire dimensions |
| `future_dimension_candidate` | 128 维中没有好等价项，未来 160 维可考虑新增 | 当前先映射到近似维度或只做标签 |

---

## 2. 沟通、自我表露与回应性映射

| 候选别名 | 推荐映射到 128 维 | 类型 | 说明 |
| --- | --- | --- | --- |
| `self_disclosure_willingness` | `attachment_vulnerability_fear`、`self_acceptance`、`communication_directness` | `composite_alias` | 高表露通常对应低脆弱恐惧、高自我接纳和较直接表达 |
| `disclosure_depth` | `attachment_vulnerability_fear`、`self_acceptance`、`values_spiritual_resonance_need` | `composite_alias` | 深层表露涉及脆弱暴露、自我接纳和深度交流需求 |
| `disclosure_breadth` | `self_acceptance`、`temperament_openness`、`values_spiritual_resonance_need` | `composite_alias` | 表露话题广度更接近开放性和深度交流需求 |
| `disclosure_pacing` | `attachment_commitment_pace`、`attachment_vulnerability_fear`、`emotion_impulsivity` | `composite_alias` | 表露节奏与承诺节奏、脆弱恐惧和冲动性相关 |
| `over_disclosure_risk` | `emotion_impulsivity`、`temperament_extraversion`、`attachment_closeness_need` | `composite_alias` | 过快表露不是单独维度，可由冲动、外向和亲密需求组合表达 |
| `under_disclosure_gap` | `attachment_vulnerability_fear`、`communication_conflict_avoidance`、`emotion_suppression_tendency` | `composite_alias` | 长期低表露通常来自脆弱恐惧、回避和压抑 |
| `pressure_disclosure_pattern` | `emotion_suppression_tendency`、`risk_breakdown_tendency`、`communication_directness` | `composite_alias` | 崩溃或吵架时才表露，更像压抑后爆发 |
| `reciprocal_disclosure_need` | `attachment_closeness_need`、`values_spiritual_resonance_need`、`trust_baseline` | `composite_alias` | 表露互惠需求来自亲密、共鸣和信任期待 |
| `partner_disclosure_expectation` | `info_transparency_preference`、`attachment_closeness_need`、`trust_suspicion_sensitivity` | `composite_alias` | 希望对方说更多，可能来自亲密需求，也可能来自透明期待或怀疑敏感 |
| `perceived_responsiveness_need` | `emotion_reassurance_need`、`attachment_closeness_need`、`desire_emotional_validation_hunger` | `composite_alias` | 被回应需求可用安抚需求、亲密需求和情绪价值需求表达 |
| `emotional_validation_need` | `emotion_reassurance_need`、`desire_emotional_validation_hunger`、`communication_listening_capacity` | `composite_alias` | 需要被确认感受，主要映射到安抚和情绪价值需求 |
| `privacy_boundary_strength` | `attachment_independence_need`、`digital_phone_privacy_need`、`trust_privacy_trust` | `composite_alias` | 隐私边界强度涉及独立、手机隐私和隐私信任 |
| `secret_tolerance` | `info_transparency_preference`、`trust_baseline`、`attachment_independence_need` | `composite_alias` | 对秘密容忍度可由低透明偏好、高基础信任、高独立需求共同表达 |
| `privacy_boundary_respect` | `boundary_respect`、`trust_privacy_trust`、`risk_boundary_violation` | `composite_alias` | 尊重隐私边界应优先映射到边界尊重和边界侵犯风险的反向 |
| `opener_skill` | `social_warmth_expression`、`communication_listening_capacity`、`temperament_agreeableness` | `composite_alias` | 能让别人敞开心扉，通常来自亲和表达、倾听和宜人性 |
| `listening_quality` | `communication_listening_capacity` | `direct_alias` | 可直接映射到倾听能力 |
| `verbal_affection_need` | `emotion_reassurance_need`、`attachment_closeness_need`、`digital_response_norm` | `composite_alias` | 语言爱意需求暂用安抚、亲密和回应规范表达 |
| `words_actions_consistency_sensitivity` | `moral_commitment_credibility`、`trust_suspicion_sensitivity`、`trust_explanation_acceptance` | `composite_alias` | 言行一致敏感与承诺可信、怀疑敏感、解释接受度相关 |
| `transparency_double_standard_risk` | `boundary_double_standard`、`info_transparency_preference`、`digital_phone_privacy_need` | `composite_alias` | 双标透明应映射到双标倾向，再结合透明偏好与自身隐私需求 |

### 2.1 P0 轻量 4 题建议映射

后续 v0.1.43 如果加入 4 个沟通表露题，建议先使用以下正式维度：

| 候选题 | 建议正式维度 |
| --- | --- |
| Q-COM-01 自我表露意愿 | `attachment_vulnerability_fear`、`self_acceptance`、`communication_directness` |
| Q-COM-05 回应性需求 | `emotion_reassurance_need`、`attachment_closeness_need`、`desire_emotional_validation_hunger` |
| Q-COM-06 哪些事情可以保留不说 | `digital_phone_privacy_need`、`info_transparency_preference`、`trust_privacy_trust`、`attachment_independence_need` |
| Q-COM-10 自己表露 vs 希望对方表露 | `attachment_vulnerability_fear`、`info_transparency_preference`、`boundary_double_standard`、`trust_suspicion_sensitivity` |

---

## 3. 冲突沟通与修复映射

| 候选别名 | 推荐映射到 128 维 | 类型 | 说明 |
| --- | --- | --- | --- |
| `defensive_response` | `communication_defensiveness` | `direct_alias` | 防卫反应已有正式维度 |
| `validation_skill` | `communication_listening_capacity`、`moral_harm_awareness`、`temperament_agreeableness` | `composite_alias` | 感受确认需要听懂、觉察伤害、愿意体谅 |
| `repair_attempt_quality` | `communication_repair_initiative`、`communication_apology_capacity`、`moral_compensation_willingness` | `composite_alias` | 修复质量由主动性、道歉能力和补偿意愿共同表达 |
| `interrupting_tendency` | `communication_listening_capacity`、`emotion_impulsivity`、`communication_defensiveness` | `composite_alias` | 打断倾向可用低倾听、高冲动和高防卫表达 |
| `active_listening_skill` | `communication_listening_capacity` | `direct_alias` | 积极倾听直接映射到倾听能力 |
| `kitchen_sinking` | `trust_old_wound_memory`、`emotion_suppression_tendency`、`risk_repeat_pattern` | `composite_alias` | 翻旧账来自旧伤、长期压抑和重复模式 |
| `old_wound_memory_sensitivity` | `trust_old_wound_memory` | `direct_alias` | 可直接映射到旧伤记忆 |
| `i_statement_skill` | `communication_directness`、`communication_meta_discussion` | `composite_alias` | 第一人称表达需要直接表达和复盘能力 |
| `xyz_statement_skill` | `communication_directness`、`communication_meta_discussion` | `composite_alias` | XYZ 陈述不单独建维度，先用直接沟通和关系复盘能力表达 |
| `behavior_description_accuracy` | `communication_directness`、`communication_meta_discussion`、`self_reflection_capacity` | `composite_alias` | 能描述行为而非攻击人格，需要直接表达和反省能力 |
| `personality_attack_level` | `communication_cruelty_under_conflict` | `direct_alias` | 人格攻击直接映射到冲突伤人倾向 |
| `conflict_timeout_skill` | `emotion_anger_control`、`emotion_recovery_speed`、`communication_repair_initiative` | `composite_alias` | 有效暂停需要愤怒控制、恢复速度和回来修复 |
| `stonewalling_level` | `emotion_shutdown_tendency`、`communication_conflict_avoidance`、`risk_avoidant_disappearance` | `composite_alias` | 石墙由情绪关机、冲突回避和失联风险共同表达 |
| `repair_after_timeout` | `communication_repair_initiative`、`emotion_recovery_speed` | `composite_alias` | 暂停后回来谈，主要看修复主动性和恢复速度 |
| `responsibility_taking` | `moral_responsibility`、`self_reflection_capacity` | `composite_alias` | 责任承担已有道德责任和自我反省支撑 |
| `perception_checking_skill` | `communication_listening_capacity`、`trust_explanation_acceptance`、`self_reflection_capacity` | `composite_alias` | 知觉检验需要倾听、接受解释和反省自己推断 |
| `contempt_signal` | `communication_cruelty_under_conflict`、`moral_harm_awareness` | `composite_alias` | 蔑视风险主要由冲突伤人倾向和低伤害觉察表达 |
| `criticism_intensity` | `communication_cruelty_under_conflict`、`communication_defensiveness` | `composite_alias` | 批评强度可映射到伤人倾向和防卫性 |
| `comfort_skill` | `social_warmth_expression`、`communication_listening_capacity`、`moral_harm_awareness` | `composite_alias` | 安慰能力来自亲和表达、倾听和伤害觉察 |
| `advice_overload` | `communication_listening_capacity`、`temperament_agreeableness` | `composite_alias` | 过度建议暂以低倾听和低体谅处理，不单建维度 |
| `respectful_disagreement` | `communication_directness`、`temperament_agreeableness`、`communication_listening_capacity` | `composite_alias` | 尊重地不同意需要直接、温和和倾听 |
| `dismissive_disagreement` | `communication_cruelty_under_conflict`、`moral_harm_awareness` | `composite_alias` | 轻视式不同意映射到高伤人倾向和低伤害觉察 |

---

## 4. 社会交换、替代选择与依赖映射

| 候选别名 | 推荐映射到 128 维 | 类型 | 说明 |
| --- | --- | --- | --- |
| `comparison_level` | `attachment_closeness_need`、`values_spiritual_resonance_need`、`values_security_need`、`self_validation_need` | `composite_alias` | CL 是期望水平，不是单一维度，只能组合估计 |
| `expected_relationship_standard` | `attachment_closeness_need`、`values_spiritual_resonance_need`、`values_security_need` | `composite_alias` | 关系标准由亲密、安全和精神共鸣需求构成 |
| `high_comparison_level` | `comparison_level` 映射组 | `runtime_only` | 这是报告标签，不应作为 dimensions |
| `gratitude_buffer` | `temperament_agreeableness`、`moral_harm_awareness`、`emotion_recovery_speed` | `future_dimension_candidate` | 128 维中没有“感激缓冲”直接等价项，暂用温和、伤害觉察和恢复速度近似 |
| `entitlement_pressure` | `self_validation_need`、`boundary_control_need`、`values_status_comparison` | `composite_alias` | “我应得更多”的压力可由认可需求、控制和比较意识近似 |
| `comparison_level_alternatives` | `desire_alternative_seeking`、`social_solitude_tolerance`、`values_freedom_need` | `composite_alias` | CLalt 可由替代倾向、独处能力和自由需求近似 |
| `alternative_sensitive` | `desire_alternative_seeking`、`desire_novelty_need` | `composite_alias` | 替代选择敏感不作为正式维度，拆到替代倾向和新鲜感需求 |
| `replacement_confidence` | `self_esteem_stability`、`social_initiative`、`social_solitude_tolerance` | `composite_alias` | 找到新关系或独自生活的信心由自尊、社交主动和孤独耐受近似 |
| `alternative_partner_attraction` | `desire_novelty_need`、`desire_physical_attraction_weight`、`desire_emotional_validation_hunger` | `composite_alias` | 新对象吸引来自新鲜感、身体吸引和情绪价值缺口 |
| `moral_boundary` | `moral_line_clarity`、`desire_loyalty_identity`、`social_boundary_awareness` | `composite_alias` | 面对新对象时的边界由底线、忠诚自我认同和社交边界共同决定 |
| `current_relationship_satisfaction` | 无 | `runtime_only` | 满意度是聚合器/关系状态结果，不是问卷维度 |
| `relationship_investment` | `attachment_commitment_pace`、`values_belonging_need`、`family_relationship_script` | `composite_alias` | 投入倾向可由承诺节奏、归属和关系脚本近似 |
| `breakup_cost_sensitivity` | `attachment_abandonment_anxiety`、`risk_dependency_crisis`、`values_belonging_need` | `composite_alias` | 分开成本敏感和被弃焦虑、依赖危机、归属需求有关 |
| `staying_due_to_cost` | `risk_dependency_crisis`、`values_security_need`、`family_approval_need` | `composite_alias` | 因成本留下不作为正式维度，拆到依赖危机、安全需求和家庭认可 |
| `exit_threat_power` | `boundary_manipulation_tendency`、`risk_sabotage_tendency`、`boundary_control_need` | `composite_alias` | 分手威胁权力属于关系事件/行为倾向，不单独建维度 |
| `fear_of_loss_pattern` | `attachment_abandonment_anxiety`、`risk_dependency_crisis`、`emotion_reassurance_need` | `composite_alias` | 失去恐惧可映射到被弃焦虑、依赖危机和安抚需求 |
| `power_balance_sensitivity` | `boundary_control_need`、`boundary_autonomy_assertion`、`values_freedom_need` | `composite_alias` | 权力敏感涉及控制、自主和自由需求 |
| `freedom_cost` | `values_freedom_need`、`attachment_independence_need` | `composite_alias` | 自由成本直接映射到自由和独立需求 |
| `relationship_investment_tendency` | `attachment_commitment_pace`、`values_belonging_need`、`attachment_reliance_comfort` | `composite_alias` | 投入倾向涉及承诺、归属和依赖舒适度 |
| `autonomy_need` | `attachment_independence_need`、`values_freedom_need`、`boundary_autonomy_assertion` | `composite_alias` | 自主需求已有多维支撑 |
| `dependence_anxiety` | `attachment_abandonment_anxiety`、`risk_dependency_crisis`、`social_dependency` | `composite_alias` | 依赖焦虑来自被弃、依赖危机和社交依赖 |
| `neediness_signal` | `social_dependency`、`emotion_reassurance_need`、`attachment_closeness_need` | `composite_alias` | 需求过高信号可用社交依赖、安抚和亲密需求表达 |
| `relationship_dependence` | `attachment_reliance_comfort`、`social_dependency`、`values_belonging_need` | `runtime_only` | 依赖度最好由问卷初始值 + 事件状态动态计算 |
| `relationship_cost_tolerance` | `emotion_stress_tolerance`、`temperament_risk_tolerance`、`values_security_need` | `composite_alias` | 成本容忍度来自压力耐受、风险耐受和安全需求反向修正 |
| `emotional_cost` | `emotion_stress_tolerance`、`emotion_anxiety_tendency`、`emotion_recovery_speed` | `runtime_only` | 情绪成本是事件结果，不应直接作为问卷维度 |
| `practical_cost` | `stability_resource_availability`、`stability_environmental_pressure`、`stability_time_management` | `runtime_only` | 现实成本来自运行时现实状态，可由稳定性维度提供初始倾向 |
| `emotional_reward` | `attachment_closeness_need`、`desire_emotional_validation_hunger`、`social_warmth_expression` | `composite_alias` | 情绪收益需求可映射到亲密、情绪价值和亲和表达 |
| `practical_reward` | `values_security_need`、`stability_resource_availability`、`values_material_importance` | `composite_alias` | 现实收益需求与安全、资源和物质重视相关 |
| `romantic_reward` | `desire_physical_attraction_weight`、`desire_novelty_need`、`attachment_closeness_need` | `composite_alias` | 浪漫收益由吸引、新鲜和亲密需求共同表达 |
| `growth_reward` | `values_spiritual_resonance_need`、`temperament_openness`、`values_achievement_need` | `composite_alias` | 成长收益对应精神共鸣、开放性和成就需求 |

---

## 5. 接近/回避、新鲜感与动荡映射

| 候选别名 | 推荐映射到 128 维 | 类型 | 说明 |
| --- | --- | --- | --- |
| `approach_motivation` | `desire_novelty_need`、`temperament_sensation_seeking`、`values_spiritual_resonance_need` | `composite_alias` | 接近动机由新鲜、刺激和自我延伸/共鸣需求近似 |
| `avoidance_motivation` | `values_security_need`、`emotion_anxiety_tendency`、`temperament_risk_tolerance` | `composite_alias` | 回避动机由安全需求、焦虑和低风险耐受近似 |
| `boredom_sensitivity` | `desire_novelty_need`、`temperament_sensation_seeking`、`values_spiritual_resonance_need` | `composite_alias` | 沉闷敏感可由新鲜、刺激和精神共鸣需求表达 |
| `routine_tolerance` | `desire_stability_preference`、`values_security_need`、`stability_life_consistency` | `composite_alias` | 日常耐受对应稳定偏好、安全需求和生活一致性 |
| `safe_but_bored_pattern` | 无 | `runtime_only` | 这是关系状态标签，不写入问卷 dimensions |
| `risk_excitement_pattern` | `temperament_sensation_seeking`、`temperament_risk_tolerance`、`desire_novelty_need` | `composite_alias` | 高刺激高风险由刺激寻求、风险耐受和新鲜感需求表达 |
| `relationship_excitement` | 无 | `runtime_only` | 活力和刺激应由事件聚合器动态计算 |
| `relationship_safety_need` | `values_security_need`、`attachment_abandonment_anxiety`、`trust_baseline` | `composite_alias` | 关系安全需求可用安全、被弃焦虑和基础信任表达 |
| `self_expansion_need` | `values_spiritual_resonance_need`、`temperament_openness`、`values_achievement_need` | `composite_alias` | 自我延伸需求对应共鸣、开放和成长/成就 |
| `shared_growth_level` | 无 | `runtime_only` | 共同成长水平是关系运行状态，不是单人问卷维度 |
| `novelty_repair_potential` | `temperament_openness`、`communication_meta_discussion`、`desire_novelty_need` | `composite_alias` | 通过新体验修复关系需要开放性、复盘和新鲜感需求 |
| `turbulence_sensitive` | `stability_adaptability`、`emotion_anxiety_tendency`、`values_security_need` | `composite_alias` | 动荡敏感可用低适应、高焦虑、高安全需求表达 |
| `interdependence_tolerance` | `attachment_reliance_comfort`、`attachment_independence_need`、`values_freedom_need` | `composite_alias` | 相互依赖耐受由依赖舒适度、独立和自由需求共同决定 |
| `future_uncertainty_tolerance` | `temperament_risk_tolerance`、`stability_adaptability`、`values_security_need` | `composite_alias` | 未来不确定耐受由风险耐受、适应能力和安全需求反向修正 |
| `shared_novelty_need` | `desire_novelty_need`、`temperament_openness` | `composite_alias` | 共同新鲜感需求可直接拆成新鲜需求和开放性 |
| `relationship_vitality` | 无 | `runtime_only` | 关系活力是聚合器状态，不写入问卷维度 |
| `external_novelty_pull` | `desire_alternative_seeking`、`desire_novelty_need`、`social_initiative` | `composite_alias` | 外部新鲜感拉力由替代倾向、新鲜需求和社交主动性决定 |
| `routine_comfort_seeker` | `desire_stability_preference`、`values_security_need`、`stability_life_consistency` | `composite_alias` | 稳定日常偏好可由稳定偏好和安全需求表达 |
| `role_transition_pressure` | `attachment_commitment_pace`、`values_freedom_need`、`attachment_intimacy_avoidance` | `composite_alias` | 转正式压力来自承诺节奏、自由需求和回避亲密 |
| `commitment_pacing` | `attachment_commitment_pace` | `direct_alias` | 可直接映射到承诺节奏 |
| `autonomy_adjustment_pressure` | `attachment_independence_need`、`values_freedom_need`、`boundary_autonomy_assertion` | `composite_alias` | 自主调整压力来自独立、自由和自主边界 |
| `honeymoon_decline_belief` | `family_relationship_script`、`desire_stability_preference`、`values_spiritual_resonance_need` | `future_dimension_candidate` | 128 维没有蜜月期信念，先用关系脚本、稳定偏好和共鸣需求近似 |
| `growth_belief` | `family_repetition_awareness`、`communication_meta_discussion`、`values_spiritual_resonance_need` | `future_dimension_candidate` | 成长信念没有直接维度，可用模式觉察、复盘和精神共鸣近似 |

---

## 6. 共有、交换与公平映射

| 候选别名 | 推荐映射到 128 维 | 类型 | 说明 |
| --- | --- | --- | --- |
| `communal_orientation` | `temperament_agreeableness`、`social_warmth_expression`、`attachment_reliance_comfort` | `composite_alias` | 共有倾向由宜人、亲和表达和依赖舒适度近似 |
| `exchange_orientation` | `values_material_importance`、`values_status_comparison`、`self_validation_need` | `future_dimension_candidate` | 128 维没有明确交换倾向，只能用物质/比较/认可需求近似 |
| `short_term_imbalance_tolerance` | `temperament_agreeableness`、`emotion_stress_tolerance`、`attachment_reliance_comfort` | `composite_alias` | 短期不对等容忍来自体谅、压力耐受和依赖舒适 |
| `long_term_fairness_need` | `moral_responsibility`、`boundary_respect`、`values_status_comparison` | `future_dimension_candidate` | 长期公平需求没有直接维度，暂用责任、边界和比较意识近似 |
| `taken_for_granted_sensitive` | `self_validation_need`、`trust_old_wound_memory`、`emotion_suppression_tendency` | `composite_alias` | 被理所当然敏感来自认可需求、旧伤和压抑累积 |
| `felt_appreciation_need` | `self_validation_need`、`desire_emotional_validation_hunger`、`social_warmth_expression` | `composite_alias` | 被看见和感谢需求可映射到认可和情绪价值需求 |
| `household_equity_sensitivity` | `stability_self_care`、`moral_responsibility`、`stability_resource_availability` | `future_dimension_candidate` | 家务公平没有直接维度，暂用生活自理、责任和资源可用性近似 |
| `emotional_labor_sensitivity` | `emotion_reassurance_need`、`communication_repair_initiative`、`trust_old_wound_memory` | `future_dimension_candidate` | 情绪劳动公平没有直接维度，暂用安抚需求、修复主动和旧伤记忆近似 |
| `underbenefit_sensitivity` | `self_validation_need`、`trust_old_wound_memory`、`emotion_suppression_tendency` | `composite_alias` | 获益不足敏感可由认可需求、旧伤和压抑表达 |
| `overbenefit_guilt_tendency` | `moral_harm_awareness`、`moral_responsibility`、`info_guilt_after_deception` | `composite_alias` | 过度获益内疚可由伤害觉察、责任和欺瞒后愧疚近似 |
| `equity_repair_capable` | `communication_meta_discussion`、`communication_repair_initiative`、`moral_compensation_willingness` | `composite_alias` | 公平修复能力来自复盘、修复主动和补偿意愿 |
| `scorekeeping_tendency` | `trust_old_wound_memory`、`emotion_suppression_tendency`、`values_status_comparison` | `composite_alias` | 记账模式来自旧伤、压抑和比较意识 |
| `fairness_restoration_drive` | `communication_directness`、`moral_responsibility`、`communication_meta_discussion` | `composite_alias` | 恢复公平的动机需要表达、责任和复盘能力 |
| `perceived_equity` | 无 | `runtime_only` | 主观公平感是关系状态，不应直接作为问卷维度 |
| `gratitude_expression` | `social_warmth_expression`、`moral_harm_awareness`、`temperament_agreeableness` | `composite_alias` | 感谢表达可由亲和表达、伤害觉察和宜人性表达 |
| `specific_request_clarity` | `communication_directness`、`communication_meta_discussion` | `composite_alias` | 具体请求清晰度由直接沟通和关系复盘能力表达 |

---

## 7. 不应直接写进 `dimensions` 的标签/状态

以下项目更适合作为报告标签、聚合器输出或运行时状态，不建议直接写进问卷 JSON 的 `dimensions`：

```text
safe_but_bored_pattern
risk_excitement_pattern
current_relationship_satisfaction
relationship_dependence
relationship_excitement
relationship_vitality
shared_growth_level
perceived_equity
high_comparison_level
alternative_sensitive
investment_bound
repair_capable
stonewalling_pattern
trust_damage_event
repair_window_open
old_wound_written
short_term_fluctuation
```

处理规则：

```text
问卷测倾向。
事件生成状态。
聚合器生成 delta。
报告层生成标签。
```

---

## 8. 后续接入 `questionnaire_mvp.json` 的操作规则

### 8.1 写 JSON 时的字段规则

当候选题进入 `questionnaire_mvp.json` 时：

```text
question.dimensions 使用正式 128 维 ID。
option.scoring.dimension_effects 使用正式 128 维 ID。
report_tags 可以使用 37 号文档中的标签 ID。
system_notes 或 design_notes 可以保留候选别名。
```

示例：

```json
{
  "id": "Q031",
  "title": "自我表露意愿",
  "dimensions": [
    "attachment_vulnerability_fear",
    "self_acceptance",
    "communication_directness"
  ],
  "design_aliases": [
    "self_disclosure_willingness",
    "disclosure_pacing"
  ]
}
```

### 8.2 计分方向提醒

某些别名是反向关系，不能简单同向加分。

| 别名 | 关键反向关系 |
| --- | --- |
| `self_disclosure_willingness` | 高表露通常对应 `attachment_vulnerability_fear` 下降 |
| `privacy_boundary_respect` | 高尊重对应 `risk_boundary_violation` 下降 |
| `avoidance_motivation` | 高回避常对应 `temperament_risk_tolerance` 下降 |
| `turbulence_sensitive` | 高动荡敏感常对应 `stability_adaptability` 下降 |
| `stonewalling_level` | 高石墙对应 `communication_repair_initiative` 下降 |
| `over_disclosure_risk` | 高过快表露可能与 `emotion_impulsivity` 上升相关 |

### 8.3 测试要求

任何后续问卷题接入必须通过：

```bash
python scripts/check_questionnaire_dimension_ids.py
python tests/questionnaire_loader_test.py
python tests/questionnaire_scoring_test.py
python tests/questionnaire_reporting_test.py
python tests/questionnaire_runner_test.py
python tests/smoke_test.py
```

---

## 9. 未来 160 维候选

以下概念在 128 维中只有近似映射。如果后续扩展到 160 维，可优先考虑新增：

```text
communal_orientation
exchange_orientation
long_term_fairness_need
household_equity_sensitivity
emotional_labor_sensitivity
felt_appreciation_need
self_expansion_need
honeymoon_decline_belief
growth_belief
gratitude_buffer
```

当前阶段不建议立刻扩表。先用本文映射保证 MVP 和标准版可运行。

---

## 10. 一句话总结

```text
39 号文档的作用是把 36 号候选题里的新变量名翻译成 16 号 128 维主表里的正式 ID，避免后续问卷 JSON 直接使用未注册维度导致检查失败。
```

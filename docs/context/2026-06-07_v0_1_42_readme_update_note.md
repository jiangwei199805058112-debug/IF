# README v0.1.42 待补说明

本文档记录 `v0.1.42 relationship_state_aggregator.py 原型` 已完成后的 README 待补内容。

由于当前通过 GitHub 文件接口更新长 README 需要整文件替换，为避免误删历史内容，本次先把待补段落记录在此。后续在本地仓库或 Codex 恢复后，应将以下内容追加到 `README.md` 末尾。

---

## 建议追加到 README 的段落

```markdown
## v0.1.42 关系状态聚合器原型

新增 `if_game/relationship_state_aggregator.py` 和 `tests/relationship_state_aggregator_test.py`，用于将单次关系事件汇总为可测试、可解释、带方向性的关系状态变化。

本版本新增 `RelationshipStateDelta`，输出字段包括：

- `source_id`、`target_id`；
- `trust_delta`、`satisfaction_delta`、`intimacy_delta`、`stability_delta`；
- `repair_chance_delta`、`old_wound_memory_delta`；
- `safety_delta`、`excitement_delta`、`fairness_delta`、`dependence_delta`；
- `report_tags`、`memory_notes`、`debug_reasons`。

新增 `aggregate_relationship_event()`，第一版支持 dict 输入，并实现以下 MVP 裁决规则：

- 隐私边界冲突不等于欺骗；
- 高欺骗和高伤害主要由 `trust_delta` 承担，避免多个系统重复扣信任；
- 石墙会降低修复机会并增加旧伤记忆；
- 高质量修复会提升修复机会；
- 重复事件和修复后再犯会写入 `memory_notes`；
- MVP 先预留 `safety_delta`、`excitement_delta`、`fairness_delta`、`dependence_delta` 字段，方便后续 v0.1.43-v0.1.46 扩展。

测试方式：

```bash
python tests/relationship_state_aggregator_test.py
```

本次仍不接 AI API，不做 UI，不接完整事件引擎，不修改问卷 JSON，也不破坏当前 14 天控制台原型。
```

---

## 已完成提交

```text
75cc702 feat: 增加关系状态聚合器原型
50b98d4 test: 增加关系状态聚合器原型测试
```

## 待办

```text
后续在本地仓库中安全修改 README.md，提交：docs: 更新README v0.1.42 聚合器原型说明
```

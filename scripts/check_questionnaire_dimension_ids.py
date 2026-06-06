"""Check questionnaire docs for unknown 128-dimension IDs.

The checker is intentionally documentation-only. It reads the canonical
dimension table, scans backtick-wrapped tokens in questionnaire design docs,
and reports references that look like dimension IDs but are not in the table.
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DIMENSION_TABLE = ROOT / "docs" / "design" / "16_questionnaire_dimension_table.md"

SCAN_FILES = [
    ROOT / "docs" / "design" / "18_super_realistic_question_bank.md",
    ROOT / "docs" / "design" / "18_super_realistic_question_bank_part2.md",
    ROOT / "docs" / "design" / "18_super_realistic_question_bank_part3.md",
    ROOT / "docs" / "design" / "18_super_realistic_question_bank_part4.md",
    ROOT / "docs" / "design" / "22_questionnaire_scoring_rules.md",
    ROOT / "docs" / "design" / "23_questionnaire_dimension_coverage.md",
    ROOT / "docs" / "design" / "24_questionnaire_json_schema.md",
]

BACKTICK_RE = re.compile(r"`([^`\r\n]+)`")
DIMENSION_ROW_RE = re.compile(r"^\|\s*`([a-z][a-z0-9_]+)`\s*\|")
SNAKE_CASE_RE = re.compile(r"^[a-z][a-z0-9_]*$")
QUESTION_ID_RE = re.compile(r"^Q\d{3}$")

DIMENSION_PREFIXES = (
    "temperament_",
    "self_",
    "emotion_",
    "social_",
    "attachment_",
    "trust_",
    "info_",
    "communication_",
    "boundary_",
    "desire_",
    "moral_",
    "values_",
    "stability_",
    "digital_",
    "family_",
    "risk_",
)

DIMENSION_CONTEXT_MARKERS = (
    "影响维度",
    "维度ID",
    "维度 ID",
    "可映射维度",
    "primary_dimensions",
    "source_dimensions",
    "compared_dimensions",
    "dimension_effects",
    "dimension_scores",
)

IGNORED_TOKENS = {
    # Selection modes and question types.
    "selection_mode",
    "forced_single",
    "multi_select",
    "primary_with_secondary",
    "multi_with_primary",
    "ranked_multi",
    "weighted_multi",
    "slider",
    "axis_2d",
    "scenario_choice",
    "npc_perspective",
    "reverse_check",
    "open_text",
    # Common schema fields.
    "id",
    "version",
    "title",
    "source_docs",
    "default_mode",
    "supported_modes",
    "score_range",
    "default_dimension_score",
    "locale",
    "status",
    "modules",
    "questions",
    "module",
    "module_id",
    "prompt",
    "question_type",
    "required",
    "allow_skip",
    "modes",
    "dimensions",
    "options",
    "dimension_effects",
    "reverse_pair_id",
    "perspective_pair_id",
    "scoring",
    "confidence",
    "report_tags",
    "hidden_tags",
    "visible_tags",
    "reason_tags",
    "notes",
    "order",
    "description",
    "target_question_ids",
    "report_section_id",
    "primary_dimensions",
    "coverage_level",
    "scale",
    "axis",
    "rank_rules",
    "weight_rules",
    "value",
    "label",
    "hidden_tags",
    "visible_tags",
    "risk_tags",
    "strength_tags",
    "gap_tags",
    "module_tags",
    "question_id",
    "primary_choice",
    "secondary_choices",
    "selected_choices",
    "ranked_choices",
    "weights",
    "slider_value",
    "axis_x",
    "axis_y",
    "open_text",
    "skipped",
    "answered_at",
    "base_weight",
    "evidence_quality",
    "enabled",
    "default",
    "affects_weight",
    "low_confidence_policy",
    "factor",
    "min_evidence_count",
    "conflict_count",
    "localization",
    "editor_notes",
    "risk_level",
    "dependency_rules",
    "skip_logic",
    "randomization_group",
    "answer_time_expected",
    "open_text_parse_rules",
    "calibration_stats",
    # Output/profile containers.
    "questionnaire_meta",
    "questionnaire_result",
    "self_report_profile",
    "behavior_profile",
    "dimension_scores",
    "confidence_scores",
    "profile_gap_hints",
    "report_sections",
    "evidence_sources",
    "source_dimensions",
    "report_inputs",
    "profile_tag",
    "summary",
    "confidence_level",
    # Formula and helper names.
    "dimension_score_start",
    "score_delta",
    "option_effect",
    "confidence_factor",
    "primary_choice_weight",
    "secondary_choice_weight",
    "reason_tag_weight",
    "primary_delta",
    "secondary_delta",
    "reason_delta",
    "per_choice_weight",
    "selected_count",
    "other_delta",
    "choice_weight",
    "allocated_points",
    "normalized_weight",
    "raw_weight",
    "raw_weights",
    "centered",
    "x_centered",
    "y_centered",
    "standard_gap",
    "Q_INFO_001",
    # Reason/report tags that share dimension-like prefixes.
    "self_beautification_risk",
    "privacy_gap_risk",
    "communication_gap_risk",
    "loyalty_gap_risk",
    "double_standard_risk",
    "stable_low_drama_pattern",
    "fear_conflict",
    "fear_abandonment",
    "fear_misunderstanding",
    "protect_privacy",
    "protect_freedom",
    "avoid_guilt",
    "think_not_serious",
    "test_partner",
    "retaliation",
    "save_face",
    "avoid_responsibility",
    "seek_reassurance",
    "maintain_image",
    "protect_relationship",
}


@dataclass(frozen=True)
class Reference:
    token: str
    path: Path
    line_no: int
    line: str


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def extract_valid_dimension_ids() -> tuple[set[str], list[str]]:
    in_dimension_section = False
    ids: list[str] = []

    for line in read_lines(DIMENSION_TABLE):
        if line.startswith("## 5. "):
            in_dimension_section = True
            continue
        if in_dimension_section and line.startswith("## 6. "):
            break
        if not in_dimension_section:
            continue

        match = DIMENSION_ROW_RE.match(line)
        if match:
            ids.append(match.group(1))

    return set(ids), ids


def looks_like_dimension_reference(token: str, line: str, valid_ids: set[str]) -> bool:
    if token in valid_ids:
        return True
    if token in IGNORED_TOKENS:
        return False
    if QUESTION_ID_RE.match(token):
        return False
    if not SNAKE_CASE_RE.match(token):
        return False

    has_dimension_prefix = token.startswith(DIMENSION_PREFIXES)
    has_dimension_context = any(marker in line for marker in DIMENSION_CONTEXT_MARKERS)
    return has_dimension_prefix or has_dimension_context


def scan_references(valid_ids: set[str]) -> tuple[list[Reference], list[Reference]]:
    references: list[Reference] = []
    unknown: list[Reference] = []

    for path in SCAN_FILES:
        for line_no, line in enumerate(read_lines(path), start=1):
            for match in BACKTICK_RE.finditer(line):
                token = match.group(1).strip()
                if not looks_like_dimension_reference(token, line, valid_ids):
                    continue

                reference = Reference(token=token, path=path, line_no=line_no, line=line.strip())
                references.append(reference)

                if token not in valid_ids:
                    unknown.append(reference)

    return references, unknown


def print_unknown_references(unknown: list[Reference]) -> None:
    if not unknown:
        print("未识别维度ID列表: 无")
        print("未识别维度ID所在文件和行号: 无")
        return

    by_token: dict[str, list[Reference]] = defaultdict(list)
    for reference in unknown:
        by_token[reference.token].append(reference)

    print("未识别维度ID列表:")
    for token in sorted(by_token):
        print(f"- {token}")

    print("未识别维度ID所在文件和行号:")
    for token in sorted(by_token):
        for reference in by_token[token]:
            print(f"- {relative(reference.path)}:{reference.line_no} `{token}`")
            print(f"  {reference.line}")


def main() -> int:
    valid_ids, raw_ids = extract_valid_dimension_ids()
    duplicate_ids = sorted(token for token, count in Counter(raw_ids).items() if count > 1)
    references, unknown = scan_references(valid_ids)

    print("问卷维度ID一致性检查")
    print(f"合法维度ID总数: {len(valid_ids)}")
    print(f"扫描到的维度引用总数: {len(references)}")

    if duplicate_ids:
        print("维度表重复ID:")
        for token in duplicate_ids:
            print(f"- {token}")

    print_unknown_references(unknown)

    failed = False
    if len(valid_ids) != 128:
        print(f"检查失败: 期望从维度表提取 128 个合法维度ID，实际为 {len(valid_ids)}。")
        failed = True
    if duplicate_ids:
        print("检查失败: 维度表存在重复ID。")
        failed = True
    if unknown:
        print("检查失败: 存在未识别维度ID。")
        failed = True

    if failed:
        return 1

    print("检查通过: 未发现未识别维度ID。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

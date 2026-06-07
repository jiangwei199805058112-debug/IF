from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from if_game.questionnaire.loader import load_mvp_questionnaire
from if_game.questionnaire.scoring import score_questionnaire


CORE_DIMENSIONS = [
    "attachment_abandonment_anxiety",
    "attachment_intimacy_avoidance",
    "attachment_closeness_need",
    "attachment_independence_need",
    "attachment_vulnerability_fear",
]


HIGH_NEED_ANSWERS = [
    {"question_id": "Q001", "primary_choice": "strong_ambiguous", "confidence": 80},
    {"question_id": "Q002", "primary_choice": "online_platform", "confidence": 80},
    {"question_id": "Q003", "primary_choice": "one_to_three_months", "confidence": 80},
    {"question_id": "Q004", "primary_choice": "daily_messages", "confidence": 80},
    {"question_id": "Q005", "primary_choice": "mostly_online", "confidence": 80},
    {"question_id": "Q007", "primary_choice": "partner_public_self_private", "confidence": 75},
    {
        "question_id": "Q008",
        "primary_choice": "stable_relationship",
        "selected_choices": ["stable_relationship", "more_companionship", "clear_future_plan"],
        "confidence": 75,
    },
    {"question_id": "Q009", "primary_choice": "complex_on_off", "confidence": 75},
    {
        "question_id": "Q010",
        "primary_choice": "trust_concealment_betrayal",
        "selected_choices": ["trust_concealment_betrayal", "communication_mismatch"],
        "confidence": 70,
    },
    {"question_id": "Q012", "slider_value": 25, "confidence": 70},
    {
        "question_id": "Q013",
        "primary_choice": "clear_betrayal",
        "selected_choices": ["clear_betrayal", "long_term_lies", "cold_violence_disappear"],
        "confidence": 75,
    },
    {
        "question_id": "Q014",
        "primary_choice": "too_sensitive",
        "selected_choices": ["too_sensitive", "hard_to_express", "over_accommodate"],
        "confidence": 70,
    },
    {
        "question_id": "Q015",
        "primary_choice": "hot_and_cold",
        "selected_choices": ["hot_and_cold", "lied_or_hidden", "no_explanation"],
        "confidence": 70,
    },
    {
        "question_id": "Q016",
        "primary_choice": "soft_but_require_change",
        "secondary_choices": ["easily_fall_back"],
        "confidence": 70,
    },
    {
        "question_id": "Q017",
        "primary_choice": "ask_why",
        "secondary_choices": ["check_clues"],
        "confidence": 80,
    },
    {"question_id": "Q018", "axis_x": 75, "axis_y": 65, "confidence": 75},
    {"question_id": "Q019", "slider_value": 85, "confidence": 75},
    {"question_id": "Q020", "slider_value": 30, "confidence": 75},
    {
        "question_id": "Q021",
        "primary_choice": "pretend_ok",
        "secondary_choices": ["tell_directly"],
        "confidence": 70,
    },
    {"question_id": "Q022", "slider_value": 85, "confidence": 75},
    {"question_id": "Q023", "primary_choice": "careful_reliance", "confidence": 70},
    {"question_id": "Q024", "primary_choice": "accept_with_boundary", "confidence": 70},
    {
        "question_id": "Q025",
        "primary_choice": "stable_meeting_contact",
        "selected_choices": ["stable_meeting_contact", "define_relationship", "family_future_plan"],
        "confidence": 70,
    },
    {"question_id": "Q026", "slider_value": 80, "confidence": 80},
    {
        "question_id": "Q030",
        "primary_choice": "needs_stable_response",
        "selected_choices": ["needs_stable_response", "needs_space", "hides_needs"],
        "confidence": 70,
    },
    {"question_id": "Q-COM-01", "primary_choice": "rarely_unless_asked", "confidence": 70},
    {
        "question_id": "Q-COM-05",
        "primary_choice": "clear_comfort",
        "secondary_choices": ["listen_without_judgment"],
        "confidence": 75,
    },
    {
        "question_id": "Q-COM-06",
        "primary_choice": "full_transparency",
        "selected_choices": ["full_transparency", "ex_contact", "opposite_sex_friends"],
        "confidence": 70,
    },
    {"question_id": "Q-COM-10", "axis_x": 30, "axis_y": 90, "confidence": 75},
]

LOW_NEED_ANSWERS = [
    {"question_id": "Q001", "primary_choice": "plain_chat", "confidence": 80},
    {"question_id": "Q002", "primary_choice": "school_course", "confidence": 80},
    {"question_id": "Q003", "primary_choice": "under_one_week", "confidence": 80},
    {"question_id": "Q004", "primary_choice": "irregular_contact", "confidence": 80},
    {"question_id": "Q005", "primary_choice": "same_city_easy", "confidence": 80},
    {"question_id": "Q007", "primary_choice": "prefer_private", "confidence": 75},
    {
        "question_id": "Q008",
        "primary_choice": "slow_observe",
        "selected_choices": ["slow_observe", "keep_light"],
        "confidence": 75,
    },
    {"question_id": "Q009", "primary_choice": "almost_none", "confidence": 75},
    {
        "question_id": "Q010",
        "primary_choice": "no_important_experience",
        "selected_choices": ["no_important_experience"],
        "confidence": 70,
    },
    {"question_id": "Q012", "slider_value": 75, "confidence": 70},
    {
        "question_id": "Q013",
        "primary_choice": "no_future_plan",
        "selected_choices": ["no_future_plan"],
        "confidence": 75,
    },
    {
        "question_id": "Q014",
        "primary_choice": "cannot_tell",
        "selected_choices": ["cannot_tell"],
        "confidence": 70,
    },
    {
        "question_id": "Q015",
        "primary_choice": "no_clear_pattern",
        "selected_choices": ["no_clear_pattern"],
        "confidence": 70,
    },
    {"question_id": "Q016", "primary_choice": "direct_refusal", "secondary_choices": [], "confidence": 70},
    {"question_id": "Q017", "primary_choice": "assume_busy", "secondary_choices": [], "confidence": 80},
    {"question_id": "Q018", "axis_x": 25, "axis_y": 30, "confidence": 75},
    {"question_id": "Q019", "slider_value": 20, "confidence": 75},
    {"question_id": "Q020", "slider_value": 85, "confidence": 75},
    {"question_id": "Q021", "primary_choice": "tell_directly", "secondary_choices": [], "confidence": 70},
    {"question_id": "Q022", "slider_value": 20, "confidence": 75},
    {"question_id": "Q023", "primary_choice": "natural_reliance", "confidence": 70},
    {"question_id": "Q024", "primary_choice": "pressure_escape", "confidence": 70},
    {
        "question_id": "Q025",
        "primary_choice": "keep_personal_space",
        "selected_choices": ["keep_personal_space"],
        "confidence": 70,
    },
    {"question_id": "Q026", "slider_value": 40, "confidence": 80},
    {
        "question_id": "Q030",
        "primary_choice": "usually_stable",
        "selected_choices": ["usually_stable"],
        "confidence": 70,
    },
    {"question_id": "Q-COM-01", "primary_choice": "shares_important", "confidence": 70},
    {
        "question_id": "Q-COM-05",
        "primary_choice": "no_deep_probe",
        "secondary_choices": ["help_analyze"],
        "confidence": 75,
    },
    {
        "question_id": "Q-COM-06",
        "primary_choice": "phone_chats",
        "selected_choices": ["phone_chats", "past_relationship_details", "sexual_thoughts"],
        "confidence": 70,
    },
    {"question_id": "Q-COM-10", "axis_x": 80, "axis_y": 30, "confidence": 75},
]


def main() -> None:
    config = load_mvp_questionnaire()
    assert len(config["questions"]) == 29
    assert len(HIGH_NEED_ANSWERS) == len(config["questions"])
    assert len(LOW_NEED_ANSWERS) == len(config["questions"])

    result = score_questionnaire(config, HIGH_NEED_ANSWERS)

    assert result["answered_questions"] == len(HIGH_NEED_ANSWERS)
    assert result["completion_rate"] == 1.0

    dimension_scores = result["dimension_scores"]
    evidence_count = result["evidence_count"]

    for dimension in CORE_DIMENSIONS:
        assert dimension in dimension_scores
        assert dimension in evidence_count
        assert 0 <= dimension_scores[dimension] <= 100

    for dimension in {
        "communication_directness",
        "emotion_reassurance_need",
        "info_transparency_preference",
        "digital_phone_privacy_need",
        "boundary_double_standard",
    }:
        assert dimension in dimension_scores
        assert evidence_count[dimension] > 0
        assert 0 <= dimension_scores[dimension] <= 100

    alternate_result = score_questionnaire(config, LOW_NEED_ANSWERS)
    assert (
        result["dimension_scores"]["attachment_abandonment_anxiety"]
        != alternate_result["dimension_scores"]["attachment_abandonment_anxiety"]
    )
    assert (
        result["dimension_scores"]["info_transparency_preference"]
        != alternate_result["dimension_scores"]["info_transparency_preference"]
    )

    print("questionnaire scoring test passed")


if __name__ == "__main__":
    main()

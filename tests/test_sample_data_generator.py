from sample_data_generator import (
    generate_conversation_data,
    generate_survey_data,
)


def test_generated_survey_count():
    survey_data = generate_survey_data(
        participant_count=60,
        random_seed=42,
    )

    assert len(survey_data) == 60


def test_all_conditions_are_generated():
    survey_data = generate_survey_data(
        participant_count=60,
        random_seed=42,
    )

    conditions = set(
        survey_data[
            "experiment_condition"
        ]
    )

    assert conditions == {
        "explicit",
        "brief",
        "control",
    }


def test_conversation_data_matches_participants():
    survey_data = generate_survey_data(
        participant_count=30,
        random_seed=42,
    )

    conversation_data = (
        generate_conversation_data(
            survey_data,
            random_seed=42,
        )
    )

    survey_participants = set(
        survey_data["participant_id"]
    )

    conversation_participants = set(
        conversation_data[
            "participant_id"
        ]
    )

    assert conversation_participants == (
        survey_participants
    )


def test_each_participant_has_two_or_more_turns():
    survey_data = generate_survey_data(
        participant_count=30,
        random_seed=42,
    )

    conversation_data = (
        generate_conversation_data(
            survey_data,
            random_seed=42,
        )
    )

    turn_counts = (
        conversation_data
        .groupby("participant_id")
        .size()
    )

    assert turn_counts.min() >= 2
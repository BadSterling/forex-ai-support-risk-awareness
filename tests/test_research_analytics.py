import pandas as pd

from research_analytics import (
    REQUIRED_SURVEY_COLUMNS,
    add_composite_scores,
    calculate_group_summary,
    validate_columns,
)


def create_test_survey_data():
    return pd.DataFrame(
        {
            "participant_id": [
                "P-1",
                "P-2",
                "P-3",
            ],
            "experiment_condition": [
                "explicit",
                "explicit",
                "control",
            ],
            "experience_level": [
                "New to forex trading",
                "Some trading experience",
                "Experienced trader",
            ],
            "trust_reliable": [4, 3, 5],
            "trust_confident": [4, 3, 4],
            "credibility_clear": [5, 3, 4],
            "risk_awareness": [5, 4, 3],
            "risk_understanding": [4, 4, 3],
            "disclosure_clear": [5, 4, 2],
            "perceived_identity": [
                "Definitely an AI system",
                "Probably an AI system",
                "Not sure",
            ],
            "overall_helpfulness": [
                8,
                7,
                8,
            ],
        }
    )


def test_required_columns_are_valid():
    data = create_test_survey_data()

    is_valid, missing_columns = (
        validate_columns(
            data,
            REQUIRED_SURVEY_COLUMNS,
        )
    )

    assert is_valid is True
    assert missing_columns == []


def test_composite_scores():
    data = create_test_survey_data()

    result = add_composite_scores(data)

    assert "trust_score" in result.columns
    assert (
        "risk_awareness_score"
        in result.columns
    )
    assert "identified_as_ai" in result.columns


def test_first_participant_trust_score():
    data = create_test_survey_data()

    result = add_composite_scores(data)

    expected_score = (
        4 + 4 + 5
    ) / 3

    assert (
        result.loc[0, "trust_score"]
        == expected_score
    )


def test_group_summary_participant_count():
    data = create_test_survey_data()

    result = calculate_group_summary(data)

    explicit_row = result[
        result["experiment_condition"]
        == "explicit"
    ].iloc[0]

    assert explicit_row["participants"] == 2
import pandas as pd


TRUST_COLUMNS = [
    "trust_reliable",
    "trust_confident",
    "credibility_clear",
]


RISK_AWARENESS_COLUMNS = [
    "risk_awareness",
    "risk_understanding",
]


REQUIRED_SURVEY_COLUMNS = {
    "participant_id",
    "experiment_condition",
    "experience_level",
    "trust_reliable",
    "trust_confident",
    "credibility_clear",
    "risk_awareness",
    "risk_understanding",
    "disclosure_clear",
    "perceived_identity",
    "overall_helpfulness",
}


REQUIRED_CONVERSATION_COLUMNS = {
    "participant_id",
    "experiment_condition",
    "detected_intent",
    "risk_level",
    "response_time_ms",
}


def validate_columns(
    data: pd.DataFrame,
    required_columns: set[str],
) -> tuple[bool, list[str]]:
    """
    Check whether all required columns are present.
    """
    missing_columns = sorted(
        required_columns
        - set(data.columns)
    )

    return (
        len(missing_columns) == 0,
        missing_columns,
    )


def add_composite_scores(
    survey_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add mean trust and risk-awareness scores.
    """
    enriched_data = survey_data.copy()

    enriched_data["trust_score"] = (
        enriched_data[TRUST_COLUMNS]
        .mean(axis=1)
    )

    enriched_data[
        "risk_awareness_score"
    ] = (
        enriched_data[
            RISK_AWARENESS_COLUMNS
        ]
        .mean(axis=1)
    )

    enriched_data[
        "identified_as_ai"
    ] = enriched_data[
        "perceived_identity"
    ].isin(
        [
            "Definitely an AI system",
            "Probably an AI system",
        ]
    )

    return enriched_data


def calculate_group_summary(
    survey_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate participant-level summary metrics by condition.
    """
    enriched_data = add_composite_scores(
        survey_data
    )

    group_summary = (
        enriched_data
        .groupby(
            "experiment_condition",
            as_index=False,
        )
        .agg(
            participants=(
                "participant_id",
                "nunique",
            ),
            mean_trust=(
                "trust_score",
                "mean",
            ),
            mean_risk_awareness=(
                "risk_awareness_score",
                "mean",
            ),
            mean_disclosure_clarity=(
                "disclosure_clear",
                "mean",
            ),
            mean_helpfulness=(
                "overall_helpfulness",
                "mean",
            ),
            ai_identification_rate=(
                "identified_as_ai",
                "mean",
            ),
        )
    )

    return group_summary


def calculate_intent_summary(
    conversation_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Count detected intents and calculate their proportions.
    """
    intent_summary = (
        conversation_data[
            "detected_intent"
        ]
        .value_counts()
        .rename_axis(
            "detected_intent"
        )
        .reset_index(
            name="conversation_turns"
        )
    )

    total_turns = max(
        len(conversation_data),
        1,
    )

    intent_summary["proportion"] = (
        intent_summary[
            "conversation_turns"
        ]
        / total_turns
    )

    return intent_summary


def calculate_risk_summary(
    conversation_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Count conversational risk levels.
    """
    risk_order = [
        "LOW",
        "MEDIUM",
        "HIGH",
    ]

    risk_summary = (
        conversation_data[
            "risk_level"
        ]
        .value_counts()
        .reindex(
            risk_order,
            fill_value=0,
        )
        .rename_axis(
            "risk_level"
        )
        .reset_index(
            name="conversation_turns"
        )
    )

    total_turns = max(
        len(conversation_data),
        1,
    )

    risk_summary["proportion"] = (
        risk_summary[
            "conversation_turns"
        ]
        / total_turns
    )

    return risk_summary


def calculate_experience_summary(
    survey_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compare composite scores by experience level.
    """
    enriched_data = add_composite_scores(
        survey_data
    )

    return (
        enriched_data
        .groupby(
            "experience_level",
            as_index=False,
        )
        .agg(
            participants=(
                "participant_id",
                "nunique",
            ),
            mean_trust=(
                "trust_score",
                "mean",
            ),
            mean_risk_awareness=(
                "risk_awareness_score",
                "mean",
            ),
            mean_helpfulness=(
                "overall_helpfulness",
                "mean",
            ),
        )
    )
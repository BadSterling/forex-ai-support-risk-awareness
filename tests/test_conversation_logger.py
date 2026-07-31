import pandas as pd

from conversation_logger import (
    CONVERSATION_COLUMNS,
)


def test_conversation_columns_are_unique():
    assert len(CONVERSATION_COLUMNS) == len(
        set(CONVERSATION_COLUMNS)
    )


def test_required_logging_fields_exist():
    required_fields = {
        "participant_id",
        "experiment_condition",
        "user_message",
        "detected_intent",
        "risk_level",
        "assistant_response",
    }

    assert required_fields.issubset(
        set(CONVERSATION_COLUMNS)
    )


def test_empty_dataframe_uses_expected_columns():
    dataframe = pd.DataFrame(
        columns=CONVERSATION_COLUMNS
    )

    assert list(dataframe.columns) == (
        CONVERSATION_COLUMNS
    )
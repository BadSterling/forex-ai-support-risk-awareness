from datetime import datetime, timezone

import pandas as pd
import streamlit as st


CONVERSATION_COLUMNS = [
    "participant_id",
    "experiment_condition",
    "turn_number",
    "timestamp_utc",
    "experience_level",
    "user_message",
    "detected_intent",
    "risk_level",
    "assistant_response",
    "response_time_ms",
]


def initialise_conversation_log() -> None:
    """
    Create an empty conversation log in session state.
    """
    if "conversation_records" not in st.session_state:
        st.session_state.conversation_records = []


def log_conversation_turn(
    participant_id: str,
    experiment_condition: str,
    experience_level: str,
    user_message: str,
    detected_intent: str,
    risk_level: str,
    assistant_response: str,
    response_time_ms: float,
) -> None:
    """
    Store one complete user-assistant interaction.
    """
    initialise_conversation_log()

    turn_number = (
        len(st.session_state.conversation_records)
        + 1
    )

    record = {
        "participant_id": participant_id,
        "experiment_condition": experiment_condition,
        "turn_number": turn_number,
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "experience_level": experience_level,
        "user_message": user_message,
        "detected_intent": detected_intent,
        "risk_level": risk_level,
        "assistant_response": assistant_response,
        "response_time_ms": round(
            response_time_ms,
            2,
        ),
    }

    st.session_state.conversation_records.append(
        record
    )


def conversation_log_to_dataframe() -> pd.DataFrame:
    """
    Convert current conversation records to a DataFrame.
    """
    initialise_conversation_log()

    return pd.DataFrame(
        st.session_state.conversation_records,
        columns=CONVERSATION_COLUMNS,
    )


def conversation_log_to_csv() -> bytes:
    """
    Export conversation records as UTF-8 CSV.
    """
    dataframe = conversation_log_to_dataframe()

    return dataframe.to_csv(
        index=False
    ).encode("utf-8")
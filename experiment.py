import random
import uuid

import streamlit as st

from config import EXPERIMENT_CONDITIONS


def generate_participant_id() -> str:
    """
    Generate a short anonymous participant identifier.
    """
    return f"P-{uuid.uuid4().hex[:8].upper()}"


def assign_experiment_condition() -> str:
    """
    Randomly assign one disclosure condition.
    """
    return random.choice(
        list(EXPERIMENT_CONDITIONS.keys())
    )


def initialise_experiment_session() -> None:
    """
    Create experiment-related session state values.
    """
    if "participant_id" not in st.session_state:
        st.session_state.participant_id = (
            generate_participant_id()
        )

    if "experiment_condition" not in st.session_state:
        st.session_state.experiment_condition = (
            assign_experiment_condition()
        )

    if "experiment_started" not in st.session_state:
        st.session_state.experiment_started = False

    if "survey_completed" not in st.session_state:
        st.session_state.survey_completed = False


def reset_experiment_session() -> None:
    """
    Remove the current session and assign a new participant.
    """
    keys_to_remove = [
        "participant_id",
        "experiment_condition",
        "experiment_started",
        "survey_completed",
        "messages",
        "conversation_records",
        "survey_response",
        "session_start_time",
    ]

    for key in keys_to_remove:
        st.session_state.pop(key, None)

    initialise_experiment_session()
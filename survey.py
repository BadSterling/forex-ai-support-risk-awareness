from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from config import SURVEY_SCALE


SURVEY_QUESTIONS = {
    "trust_reliable": (
        "I believe the assistant provided reliable information."
    ),
    "trust_confident": (
        "I felt confident relying on the assistant's explanation."
    ),
    "credibility_clear": (
        "The assistant's responses were clear and credible."
    ),
    "risk_awareness": (
        "The conversation increased my awareness of forex trading risks."
    ),
    "risk_understanding": (
        "I better understand how leverage and losses can affect a trader."
    ),
    "disclosure_clear": (
        "It was clear whether I was interacting with an AI system."
    ),
}


def render_likert_question(
    question_key: str,
    question_text: str,
) -> int:
    """
    Render one five-point Likert-scale question.
    """
    return st.radio(
        question_text,
        options=list(SURVEY_SCALE.keys()),
        format_func=lambda value: (
            f"{value} — {SURVEY_SCALE[value]}"
        ),
        horizontal=True,
        key=f"survey_{question_key}",
    )


def render_post_conversation_survey() -> dict | None:
    """
    Display and collect the post-conversation survey.
    """
    st.subheader("Post-Conversation Survey")

    st.caption(
        "Please answer based on your experience in this session."
    )

    with st.form("post_conversation_survey"):
        responses = {}

        for question_key, question_text in (
            SURVEY_QUESTIONS.items()
        ):
            responses[question_key] = (
                render_likert_question(
                    question_key,
                    question_text,
                )
            )

        perceived_identity = st.selectbox(
            "Who or what did you believe you were interacting with?",
            options=[
                "Definitely an AI system",
                "Probably an AI system",
                "Not sure",
                "Probably a human",
                "Definitely a human",
            ],
        )

        overall_helpfulness = st.slider(
            "How helpful was the assistant overall?",
            min_value=0,
            max_value=10,
            value=5,
        )

        open_feedback = st.text_area(
            "Optional feedback",
            placeholder=(
                "What affected your trust or understanding?"
            ),
            max_chars=1000,
        )

        submitted = st.form_submit_button(
            "Submit survey",
            use_container_width=True,
        )

    if not submitted:
        return None

    responses.update(
        {
            "perceived_identity": perceived_identity,
            "overall_helpfulness": overall_helpfulness,
            "open_feedback": open_feedback.strip(),
            "survey_timestamp_utc": datetime.now(
                timezone.utc
            ).isoformat(),
        }
    )

    return responses


def create_survey_dataframe(
    participant_id: str,
    experiment_condition: str,
    experience_level: str,
    survey_response: dict,
) -> pd.DataFrame:
    """
    Convert one survey response into a one-row DataFrame.
    """
    complete_response = {
        "participant_id": participant_id,
        "experiment_condition": experiment_condition,
        "experience_level": experience_level,
        **survey_response,
    }

    return pd.DataFrame(
        [complete_response]
    )


def survey_to_csv(
    participant_id: str,
    experiment_condition: str,
    experience_level: str,
    survey_response: dict,
) -> bytes:
    """
    Export one survey response as CSV.
    """
    dataframe = create_survey_dataframe(
        participant_id=participant_id,
        experiment_condition=experiment_condition,
        experience_level=experience_level,
        survey_response=survey_response,
    )

    return dataframe.to_csv(
        index=False
    ).encode("utf-8")
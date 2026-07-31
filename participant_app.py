from datetime import datetime, timezone
from time import perf_counter

import streamlit as st

from config import (
    APP_TITLE,
    EXPERIENCE_LEVELS,
    EXPERIMENT_CONDITIONS,
    RISK_LEVELS,
)
from conversation_logger import (
    conversation_log_to_csv,
    initialise_conversation_log,
    log_conversation_turn,
)
from experiment import (
    initialise_experiment_session,
    reset_experiment_session,
)
from intent_detector import detect_intent
from response_generator import generate_response
from risk_engine import classify_risk
from survey import (
    render_post_conversation_survey,
    survey_to_csv,
)


initialise_experiment_session()
initialise_conversation_log()


if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("Participant Application")

st.caption(
    "Anonymous forex support conversation and "
    "AI identity-disclosure research session."
)

with st.expander(
    "Study purpose and system limitations"
):
    st.markdown(
        """
        This prototype explores how different forms of AI identity
        disclosure may affect trust, credibility and awareness of
        forex trading risks.

        The system uses a controlled rule-based knowledge base.
        It does not provide personalised financial advice and it
        should not be used to make trading decisions.
        """
    )


participant_id = st.session_state.participant_id

condition_key = (
    st.session_state.experiment_condition
)

condition = EXPERIMENT_CONDITIONS[
    condition_key
]


with st.sidebar:
    st.header("Research Session")

    st.write(
        f"**Participant ID:** `{participant_id}`"
    )

    if st.session_state.experiment_started:
        st.write(
            "**Condition:** Assigned"
        )
    else:
        st.write(
            "**Condition:** Hidden until session begins"
        )

    experience_level = st.selectbox(
        "Trading experience",
        options=EXPERIENCE_LEVELS,
        disabled=(
            st.session_state.experiment_started
        ),
    )

    show_internal_analysis = st.checkbox(
        "Show system analysis",
        value=True,
    )

    st.divider()

    st.markdown("### Supported Topics")

    st.markdown(
        """
        - Forex basics
        - Lot sizes
        - Leverage
        - Margin
        - Spreads
        - Stop-loss orders
        - Loss exposure
        - Guaranteed-profit claims
        """
    )

    st.divider()

    if st.button(
        "Start new anonymous session",
        use_container_width=True,
    ):
        reset_experiment_session()
        st.rerun()


if not st.session_state.experiment_started:
    st.subheader("Participant Information")

    st.info(
        "This prototype records anonymous conversation data, "
        "including questions, detected topics, risk classifications "
        "and survey responses. Do not enter your name, email address, "
        "account number or other personal information."
    )

    consent_confirmed = st.checkbox(
        "I understand that this is an educational research prototype "
        "and agree to continue with anonymous session logging."
    )

    if st.button(
        "Begin conversation",
        disabled=not consent_confirmed,
        type="primary",
    ):
        st.session_state.experiment_started = True
        st.session_state.session_start_time = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )
        st.rerun()

    st.stop()


if condition["message"]:
    st.info(condition["message"])


with st.expander("About this prototype"):
    st.markdown(
        """
        This version uses a transparent rule-based system.

        It detects supported user intents, assigns a conversational
        risk level and selects responses from a controlled forex
        knowledge base.

        Conversation and survey records are stored only in the
        current browser session unless the participant explicitly
        downloads them.
        """
    )


conversation_tab, survey_tab, export_tab = st.tabs(
    [
        "Conversation",
        "Survey",
        "Session Export",
    ]
)


with conversation_tab:
    for message in st.session_state.messages:
        with st.chat_message(
            message["role"]
        ):
            st.markdown(
                message["content"]
            )

            if (
                message["role"] == "assistant"
                and show_internal_analysis
                and "intent" in message
            ):
                with st.expander(
                    "System analysis"
                ):
                    st.write(
                        f"**Detected intent:** "
                        f"{message['intent']}"
                    )

                    st.write(
                        f"**Risk level:** "
                        f"{message['risk_level']}"
                    )

    user_message = st.chat_input(
        "Ask a forex support question"
    )

    if user_message:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        with st.chat_message("user"):
            st.markdown(user_message)

        response_start = perf_counter()

        detected_intent = detect_intent(
            user_message
        )

        risk_level = classify_risk(
            message=user_message,
            intent=detected_intent,
        )

        assistant_response = generate_response(
            intent=detected_intent,
            risk_level=risk_level,
            experience_level=experience_level,
        )

        response_time_ms = (
            perf_counter() - response_start
        ) * 1000

        risk_information = RISK_LEVELS[
            risk_level
        ]

        with st.chat_message("assistant"):
            st.markdown(
                assistant_response
            )

            if risk_level == "HIGH":
                st.error(
                    risk_information["label"]
                )

            elif risk_level == "MEDIUM":
                st.warning(
                    risk_information["label"]
                )

            else:
                st.success(
                    risk_information["label"]
                )

            if show_internal_analysis:
                with st.expander(
                    "System analysis"
                ):
                    st.write(
                        f"**Detected intent:** "
                        f"{detected_intent}"
                    )

                    st.write(
                        f"**Risk level:** "
                        f"{risk_level}"
                    )

                    st.write(
                        "**Risk interpretation:** "
                        f"{risk_information['description']}"
                    )

                    st.write(
                        "**Response generation time:** "
                        f"{response_time_ms:.2f} ms"
                    )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response,
                "intent": detected_intent,
                "risk_level": risk_level,
            }
        )

        log_conversation_turn(
            participant_id=participant_id,
            experiment_condition=condition_key,
            experience_level=experience_level,
            user_message=user_message,
            detected_intent=detected_intent,
            risk_level=risk_level,
            assistant_response=assistant_response,
            response_time_ms=response_time_ms,
        )


with survey_tab:
    completed_turns = len(
        st.session_state.conversation_records
    )

    if completed_turns < 2:
        st.info(
            "Please complete at least two conversation turns "
            "before submitting the survey."
        )

    elif st.session_state.survey_completed:
        st.success(
            "The survey has been completed for this session."
        )

    else:
        survey_response = (
            render_post_conversation_survey()
        )

        if survey_response is not None:
            st.session_state.survey_response = (
                survey_response
            )

            st.session_state.survey_completed = True

            st.success(
                "Thank you. Your anonymous survey response "
                "has been recorded in this browser session."
            )


with export_tab:
    st.subheader("Session Data Export")

    st.write(
        f"**Anonymous participant:** `{participant_id}`"
    )

    st.write(
        f"**Recorded conversation turns:** "
        f"{len(st.session_state.conversation_records)}"
    )

    st.write(
        f"**Survey completed:** "
        f"{'Yes' if st.session_state.survey_completed else 'No'}"
    )

    if st.session_state.conversation_records:
        st.download_button(
            label="Download conversation log",
            data=conversation_log_to_csv(),
            file_name=(
                f"{participant_id}_conversation.csv"
            ),
            mime="text/csv",
            use_container_width=True,
        )

    if (
        st.session_state.survey_completed
        and "survey_response"
        in st.session_state
    ):
        st.download_button(
            label="Download survey response",
            data=survey_to_csv(
                participant_id=participant_id,
                experiment_condition=condition_key,
                experience_level=experience_level,
                survey_response=(
                    st.session_state.survey_response
                ),
            ),
            file_name=(
                f"{participant_id}_survey.csv"
            ),
            mime="text/csv",
            use_container_width=True,
        )

    st.warning(
        "The exported files may contain the questions entered "
        "during this session. Do not enter or export personal, "
        "financial-account or confidential information."
    )
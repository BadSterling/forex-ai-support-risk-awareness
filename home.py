import streamlit as st


st.title(
    "Forex AI Support & Risk Awareness Assistant"
)

st.markdown(
    """
    ### A transparent conversational system for forex education,
    risk communication and AI identity-disclosure research
    """
)

st.info(
    "This portfolio project combines conversational-system design, "
    "financial risk communication, experimental research methods "
    "and statistical data analysis."
)


st.divider()


# -------------------------------------------------------------------
# Project overview
# -------------------------------------------------------------------

st.subheader("Project Overview")

overview_column, research_column = st.columns(2)


with overview_column:
    st.markdown(
        """
        #### The application

        The participant application provides a controlled forex
        customer-support conversation experience.

        It can:

        - Detect supported forex-related questions
        - Adapt explanations to the user's experience level
        - Classify conversational risk
        - Display appropriate risk warnings
        - Record anonymous conversation events
        - Collect post-conversation survey responses
        """
    )


with research_column:
    st.markdown(
        """
        #### The research question

        The prototype supports investigation of the following question:

        > How does disclosing a chatbot's AI identity affect novice
        > users' trust, perceived credibility and risk awareness in
        > forex customer-service conversations?

        Anonymous sessions are randomly assigned to explicit,
        brief or control disclosure conditions.
        """
    )


st.divider()


# -------------------------------------------------------------------
# Main capabilities
# -------------------------------------------------------------------

st.subheader("System Capabilities")

capability_column_1, capability_column_2, capability_column_3 = (
    st.columns(3)
)


with capability_column_1:
    st.markdown(
        """
        #### Conversational Support

        - Streamlit chat interface
        - Forex knowledge base
        - Transparent intent detection
        - Beginner and standard explanations
        - Conversation history
        - Safe fallback responses
        """
    )


with capability_column_2:
    st.markdown(
        """
        #### Risk Awareness

        - Low, medium and high-risk classification
        - Leverage and margin warnings
        - Guaranteed-return claim detection
        - Loss-exposure explanations
        - General educational disclaimers
        - Controlled response generation
        """
    )


with capability_column_3:
    st.markdown(
        """
        #### Research Analytics

        - Anonymous experimental conditions
        - Trust and risk-awareness scales
        - Cronbach's alpha
        - Confidence intervals
        - One-way ANOVA
        - Eta-squared effect sizes
        - Tukey HSD comparisons
        """
    )


st.divider()


# -------------------------------------------------------------------
# Experiment flow
# -------------------------------------------------------------------

st.subheader("Experimental Workflow")

workflow_columns = st.columns(5)

workflow_columns[0].markdown(
    """
    #### 1

    Anonymous session
    """
)

workflow_columns[1].markdown(
    """
    #### 2

    Disclosure condition
    """
)

workflow_columns[2].markdown(
    """
    #### 3

    Forex conversation
    """
)

workflow_columns[3].markdown(
    """
    #### 4

    Trust and risk survey
    """
)

workflow_columns[4].markdown(
    """
    #### 5

    Statistical analysis
    """
)


st.caption(
    "The control condition does not claim that the assistant is "
    "human. System information remains available within the application."
)


st.divider()


# -------------------------------------------------------------------
# Disclosure conditions
# -------------------------------------------------------------------

st.subheader("AI Identity-Disclosure Conditions")

condition_columns = st.columns(3)


with condition_columns[0]:
    st.markdown(
        """
        #### Explicit disclosure

        Clearly explains that the user is interacting with an
        AI support assistant and states that the system may
        provide incomplete or incorrect information.
        """
    )


with condition_columns[1]:
    st.markdown(
        """
        #### Brief disclosure

        Provides a concise statement that the conversation is
        taking place with an AI support assistant.
        """
    )


with condition_columns[2]:
    st.markdown(
        """
        #### Control condition

        Does not display a prominent disclosure banner, while
        still retaining general information about the system
        within the application.
        """
    )


st.divider()


# -------------------------------------------------------------------
# Architecture
# -------------------------------------------------------------------

st.subheader("Technical Architecture")

architecture_column, methodology_column = st.columns(2)


with architecture_column:
    st.markdown(
        """
        #### Modular Python design

        The project separates responsibilities into modules for:

        - Experimental session management
        - Intent detection
        - Risk classification
        - Knowledge-base responses
        - Conversation logging
        - Survey collection
        - Research analytics
        - Statistical testing
        - Automated report generation
        """
    )


with methodology_column:
    st.markdown(
        """
        #### Transparent methodology

        The conversational prototype currently uses predefined
        knowledge and decision rules rather than a generative
        language model.

        This makes the system:

        - Explainable
        - Reproducible
        - Testable
        - Easier to evaluate experimentally
        - Less likely to generate unsupported financial claims
        """
    )


st.divider()


# -------------------------------------------------------------------
# Data warning
# -------------------------------------------------------------------

st.subheader("Data and Research Status")

st.warning(
    "The Research Dashboard includes synthetic demonstration data. "
    "Artificial group differences are included only to test charts, "
    "statistical functions and report generation. They are not real "
    "participant findings."
)

st.markdown(
    """
    The current portfolio version is not configured as a production
    research-data collection platform.

    Conversation records and survey responses remain in the current
    Streamlit browser session unless the user explicitly downloads them.

    Formal research deployment would additionally require:

    - Ethics approval
    - Participant information and consent documentation
    - Secure database storage
    - Access controls
    - Data-retention policies
    - Privacy and withdrawal procedures
    """
)


st.divider()


# -------------------------------------------------------------------
# Navigation
# -------------------------------------------------------------------

st.subheader("Explore the Project")

navigation_columns = st.columns(2)


with navigation_columns[0]:
    st.markdown(
        """
        #### Participant Application

        Experience the anonymous forex support conversation,
        disclosure condition, risk warnings and post-conversation
        survey.
        """
    )

    st.page_link(
        "participant_app.py",
        label="Open Participant Application",
        icon=":material/chat:",
        use_container_width=True,
    )


with navigation_columns[1]:
    st.markdown(
        """
        #### Research Dashboard

        Generate synthetic experimental data, upload CSV files,
        compare disclosure conditions and export statistical reports.
        """
    )

    st.page_link(
        "research_dashboard.py",
        label="Open Research Dashboard",
        icon=":material/analytics:",
        use_container_width=True,
    )


st.divider()


st.caption(
    "This application is intended for educational, research and "
    "portfolio demonstration purposes only. It does not provide "
    "financial advice."
)
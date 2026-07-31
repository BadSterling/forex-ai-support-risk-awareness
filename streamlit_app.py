import streamlit as st


st.set_page_config(
    page_title="Forex AI Support Research System",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)


home_page = st.Page(
    "home.py",
    title="Home",
    icon=":material/home:",
    default=True,
)

participant_page = st.Page(
    "participant_app.py",
    title="Participant Application",
    icon=":material/chat:",
)

research_page = st.Page(
    "research_dashboard.py",
    title="Research Dashboard",
    icon=":material/analytics:",
)


navigation = st.navigation(
    {
        "Project": [
            home_page,
        ],
        "Application": [
            participant_page,
        ],
        "Research Tools": [
            research_page,
        ],
    }
)


with st.sidebar:
    st.divider()

    st.caption(
        "Forex AI Support & Risk Awareness Assistant"
    )

    st.caption(
        "Python · Streamlit · Pandas · SciPy"
    )

    st.caption(
        "Educational and research prototype"
    )


navigation.run()
import streamlit as st

st.set_page_config(
    page_title="Diagnostic Test",
    layout="wide",
)

st.title("Streamlit is working")

st.success("The page rendered successfully.")

st.write("Streamlit version:", st.__version__)
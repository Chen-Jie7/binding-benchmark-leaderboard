import streamlit as st

st.set_page_config(
    page_title="Protein-Ligand Binding Benchmark",
    page_icon=":material/science:",
    layout="wide",
)

pages = [
    st.Page("pages/1_Home.py", title="Home", icon=":material/home:"),
    st.Page("pages/2_Download.py", title="Download Benchmark", icon=":material/download:"),
    st.Page("pages/3_Submit.py", title="Submit Predictions", icon=":material/upload:"),
    st.Page("pages/4_Leaderboard.py", title="Leaderboard", icon=":material/leaderboard:"),
]

nav = st.navigation(pages)
nav.run()

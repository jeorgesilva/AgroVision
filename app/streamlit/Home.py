# app/streamlit/Home.py
import streamlit as st

st.set_page_config(
    page_title="AgroVision",
    page_icon="🌱",
)

st.title("🌱 AgroVision")

st.write(
    "AgroVision is an applied AgTech project combining Computer Vision and Geospatial Analysis to enable precision herbicide application."
)

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    **👈 Select a demo from the sidebar** to see some examples of what AgroVision can do!
    ### Want to learn more?
    - Check out [the source code on GitHub](https://github.com/jeorgesilva/agrovision-ai)
    - Connect with me on [LinkedIn](https://www.linkedin.com/in/jeorgecssilva/)
"""
)

from langchain_openai import ChatOpenAI
import streamlit as st

llm = ChatOpenAI(
    api_key=st.session_state.api_key or "lmstudio",
    max_retries=2,
    base_url=st.session_state.url or "https://api.openai.com/v1/"
)

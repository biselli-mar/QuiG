import logging
import sys
import streamlit as st
import os

if 'url' not in st.session_state:  # Local server URL - LM Studio in this case
    st.session_state.url = "http://localhost:1234/v1/"
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "Moodle Quiz Generator"
os.environ["LANGCHAIN_API_KEY"] = "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"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

main_page = st.Page("st_pages/main.py", title="Main Page", icon="🏠")
prompts_page = st.Page("st_pages/prompts.py", title="Prompts", icon="")
generate_quiz_page = st.Page("st_pages/generate.py", title="Generate Quiz", icon="📝")
llm_page = st.Page("st_pages/llm.py", title="LLM", icon="")

if st.session_state.api_key is None:
    pg = st.navigation({
        "Moodle-Quiz-Generator": [main_page]
    })
else:
    pg = st.navigation({
        "Moodle-Quiz-Generator": [main_page],
        "Generate Quiz": [generate_quiz_page],
        "Configuration": [prompts_page, llm_page]
    })
pg.run()

st.session_state.generated = False

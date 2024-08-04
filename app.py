import logging
import sys
import streamlit as st
import const

if 'url' not in st.session_state:  # Local server URL - LM Studio in this case
    st.session_state.url = "http://localhost:1234/v1/"
if 'api_key' not in st.session_state:
    st.session_state.api_key = None
if 'map_prompt' not in st.session_state:
    st.session_state.map_prompt = const.map_prompt_template
if 'reduce_prompt' not in st.session_state:
    st.session_state.reduce_prompt = const.reduce_prompt_template
if 'generate_query' not in st.session_state:
    st.session_state.generate_query = const.generate_query
if 'generated' not in st.session_state:
    st.session_state.generated = False
if 'quiz' not in st.session_state:
    st.session_state.quiz = None
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

main_page = st.Page("st_pages/main.py", title="Main Page", icon="🏠")
prompts_page = st.Page("st_pages/config_prompts.py", title="Prompts", icon="")
generate_quiz_page = st.Page("st_pages/generate.py", title="Generate Quiz", icon="📝")
llm_page = st.Page("st_pages/config_llm.py", title="LLM", icon="")

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

import logging
import streamlit as st
import json
from const import RECENT_SUMMARIES_PATH
from extraction.extractor import extract_text

st.set_page_config(page_title="Quiz Generator", page_icon="📝")

from st_pages.components.question_generator import question_generator


quiz = None
selected_questions = []


f_recent_summaries = open(RECENT_SUMMARIES_PATH, "r")
recent_summaries = f_recent_summaries.read()
f_recent_summaries.close()

if recent_summaries == "":
    recent_summaries = "[]"
summaries_json = json.loads(recent_summaries)

with st.expander("Recent Summaries"):
    for summary in summaries_json:
        st.text_area(f"{summary['title']} {summary['time']}", summary['summary'], disabled=True, height=200)

def reset_state():
    st.session_state.generated = False
    st.session_state.quiz = None
    logging.info("State reset.")


uploaded_file = st.file_uploader("Upload a document (PDF or LaTeX)",
                                 type=["pdf", "tex"],
                                 accept_multiple_files=False, on_change=reset_state)

if uploaded_file is not None:
    with st.spinner("Extracting text..."):
        text = extract_text(uploaded_file)

    text_input = st.text_area("Text", text, height=300)

    question_generator(text_input)

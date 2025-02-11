import logging
import streamlit as st
import json
from const import RECENT_SUMMARIES_PATH
from extraction.extractor import extract_text

st.set_page_config(page_title="Quiz Generator", page_icon="📝")

from st_pages.components.question_generator import question_generator
from st_pages.components.recent_summaries import recent_summary_selector


quiz = None
selected_questions = []
text = ""
reuse_summary = False

def reset_state(keep_text=False):
    if not keep_text:
        st.session_state.last_summary = None
    st.session_state.file_generated = False
    st.session_state.quiz = None
    logging.info("State reset.")

f_recent_summaries = open(RECENT_SUMMARIES_PATH, "r")
recent_summaries = f_recent_summaries.read()
f_recent_summaries.close()

if recent_summaries == "":
    recent_summaries = "[]"
summaries_json = json.loads(recent_summaries)


with st.expander("Reuse Recent Summaries", expanded=reuse_summary):
    selected_summaries = recent_summary_selector(summaries_json)
    if selected_summaries is not None:
        text = " ".join(selected_summaries)
        reuse_summary = True
        st.session_state.last_summary = text
        reset_state(keep_text=True)

with st.expander("File Upload", expanded=(not reuse_summary)):
    uploaded_file = st.file_uploader("Upload a document (PDF or LaTeX)",
                                 type=["pdf", "tex"],
                                 accept_multiple_files=False, on_change=reset_state)

if reuse_summary:
    question_generator(text, "file_generated")
elif uploaded_file is not None: 
    with st.spinner("Extracting text..."):
        text = extract_text(uploaded_file)
    question_generator(text, "file_generated")
    

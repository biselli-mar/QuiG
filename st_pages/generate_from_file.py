import logging
import streamlit as st

from extraction.extractor import extract_text

from st_pages.components.question_generator import question_generator

st.set_page_config(page_title="Quiz Generator", page_icon="📝")

quiz = None
selected_questions = []


@st.cache(persist=True, allow_output_mutation=True)
def RecentSummaries():
    return []


recent_summaries = RecentSummaries()
st.button("Add to recent summaries", on_click=lambda: recent_summaries.append("yay"))

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

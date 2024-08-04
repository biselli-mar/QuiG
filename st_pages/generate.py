import logging
import streamlit as st
from openai import APIConnectionError

from extraction.extractor import extract_text
from generation.question_generation_chain import generate_questions
from generation.summarization import summarize_docs, split_text
from quiz.export import convert_to_gift
from quiz.question_list import list_questions

st.set_page_config(page_title="Quiz Generator", page_icon="📝")

quiz = None
selected_questions = []


def reset_state():
    st.session_state.generated = False
    st.session_state.quiz = None
    # generate_questions.clear()
    logging.info("State reset.")


uploaded_file = st.file_uploader("Upload a document (PDF or LaTeX)",
                                 type=["pdf", "tex"],
                                 accept_multiple_files=False, on_change=reset_state)

if uploaded_file is not None:
    with st.spinner("Extracting text..."):
        text = extract_text(uploaded_file)

    text_input = st.text_area("Text", text, height=300)

    st.divider()
    st.header("Questions")

    with st.form("generate_questions"):
        num_questions = st.select_slider("Number of questions",
                                         options=range(1, 11), value=5, help="Select the number of questions "
                                                                             "to generate from the text.")
        if st.form_submit_button("Generate"):
            reset_state()
            with st.spinner("Generating questions..."):
                docs = split_text(text_input)
                try:
                    # summarize if text is too long to fit in one request
                    if len(docs) > 1:
                        # very slow, only use if necessary
                        docs = summarize_docs(docs)
                    st.session_state.quiz = generate_questions(docs, num_questions)
                    if st.session_state.quiz is not None:
                        st.session_state.generated = True
                except APIConnectionError:
                    st.error("Connection to server failed. "
                             "Make sure the LLM server is running and reachable at the specified URL.")

    if st.session_state.generated:
        st.write("Generated questions:")
        list_questions(st.session_state.quiz, selected_questions)

        st.download_button("Download selected questions", convert_to_gift(selected_questions),
                           "questions.gift", "text/plain")

import logging
import streamlit as st

from langchain_core.exceptions import OutputParserException
from openai import APIConnectionError, AuthenticationError

from generation.question_generation_chain import generate_questions
from generation.summarization import summarize_docs, split_text
from quiz.export import convert_to_gift
from quiz.question_list import list_questions

selected_questions = []

def reset_state():
    st.session_state.generated = False
    st.session_state.quiz = None
    logging.info("State reset.")

def question_generator(text_input):
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
                    else:
                        docs = docs[0]
                    st.session_state.quiz = generate_questions(docs, num_questions)
                    if st.session_state.quiz is not None:
                        st.session_state.generated = True
                except APIConnectionError:
                    st.error("Connection to server failed. "
                             "Make sure the LLM server is running and reachable at the specified URL.")
                except AuthenticationError:
                    st.error("Invalid OpenAI API key. Please check the API key and try again.")
                except OutputParserException:
                    st.error("Error parsing output. Please try again.")

    if st.session_state.generated:
        st.write("Generated questions:")
        list_questions(st.session_state.quiz, selected_questions)

        st.download_button("Download selected questions", convert_to_gift(selected_questions),
                           "questions.gift", "text/plain")
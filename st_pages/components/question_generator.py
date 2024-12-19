import logging
import streamlit as st
import datetime
import json
from const import RECENT_SUMMARIES_PATH
from langchain_core.exceptions import OutputParserException
from openai import APIConnectionError, AuthenticationError

from generation.question_generation_chain import generate_questions
from generation.summarization import summarize_docs, split_text
from quiz.export import convert_to_gift
from quiz.question_list import list_questions

selected_questions = []

@st.dialog("Save Summary")
def append_summary_dialog(summary):
    with st.form(key="append_summary"):
        title = st.text_input("Title", value="Recent Summary", placeholder="Enter a title for the summary.")
        st.text_area("Text", summary, height=200)
        if st.form_submit_button("Save"):
            f_recent_summaries = open(RECENT_SUMMARIES_PATH, "w")
            summaries_json = json.loads(f_recent_summaries.read())
            f_recent_summaries.close()
            append_summary(summaries_json, summary, title)
            st.write("Summary saved.")
        if st.form_submit_button("Cancel"):
            st.stop()

def append_summary(summaries_json, summary, title = "Recent Summary"):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    summaries_json.append({"time":f"{time_now}","title":f"{title}","summary":summary})
    f_recent_summaries = open(RECENT_SUMMARIES_PATH, "w")
    f_recent_summaries.write(json.dumps(summaries_json))
    f_recent_summaries.close()

st.button("Add to recent summaries", on_click=append_summary, args=("Test",))

def reset_state():
    st.session_state.generated = False
    st.session_state.quiz = None
    logging.info("State reset.")

summary = ""

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
                    summary = docs
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
        with st.expander("Show summary"):
            st.write(summary)
            st.button("Save summary", on_click=append_summary, args=(summary,))
        st.write("Generated questions:")
        list_questions(st.session_state.quiz, selected_questions)

        st.download_button("Download selected questions", convert_to_gift(selected_questions),
                           "questions.gift", "text/plain")
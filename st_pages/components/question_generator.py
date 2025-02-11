import logging
import json
import base64
import streamlit as st
import streamlit.components.v1 as components
from langchain_core.exceptions import OutputParserException
from openai import APIConnectionError, AuthenticationError

from generation.question_generation_chain import generate_questions
from generation.summarization import summarize_docs, split_text
from st_pages.components.recent_summaries import append_summary_dialog
from quiz.export import convert_to_gift
from quiz.question_list import list_questions

selected_questions = []
summary_content = None

def reset_state(generated_property):
    st.session_state[generated_property] = False
    st.session_state.quiz = None
    logging.info("State reset.")


def question_generator(text, generated_property):
    st.divider()
    text_input = st.text_area("Text", text, height=300)
    st.header("Questions")
    with st.form("generate_questions"):
        num_questions = st.select_slider("Number of questions",
                                         options=range(1, 11), value=5, help="Select the number of questions "
                                                                             "to generate from the text.")
        with st.expander("Advanced options"):
            summary_content = st.text_input("Summary Content", placeholder="Enter a prompt to limit what the model focuses on.")
            repeat_generation = st.checkbox("Repeat generation",
                                            help="Automatically download generated questions and restart generation.",
                                            key="repeat_generation_checkbox")
        if st.form_submit_button("Generate"):
            reset_state(generated_property)
            try:
                extract_and_generate(text_input, summary_content, num_questions)
            except Exception as e:
                logging.error("Error during generation: %s", e)
                st.error("An error occurred during question generation")
            if st.session_state.quiz is not None:
                st.session_state[generated_property] = True
                if repeat_generation:
                    download_file(convert_to_gift(st.session_state.quiz.questions), "questions.gift")
            elif repeat_generation:
                st.session_state[generated_property] = True
        

    if st.session_state[generated_property]:
        if repeat_generation:
            def stop_generation():
                nonlocal repeat_generation
                repeat_generation = False
            st.button("Stop repeated generation", on_click=stop_generation)
            while repeat_generation:
                reset_state(generated_property)
                try:
                    extract_and_generate(text_input, summary_content, num_questions)
                except Exception as e:
                    logging.error("Error during repeated generation: %s", e)
                    continue
                if st.session_state.quiz is not None:
                    download_file(convert_to_gift(st.session_state.quiz.questions), "questions.gift")
        else:
            with st.expander("Show summary"):
                st.text_area("Summary", st.session_state.last_summary, height=300)
                st.button("Save summary", on_click=append_summary_dialog)
            st.write("Generated questions:")
            list_questions(st.session_state.quiz, selected_questions)

            st.download_button("Download selected questions", convert_to_gift(selected_questions),
                           "questions.gift", "text/plain")
        
        
def extract_and_generate(text_input, summary_content, num_questions):
    with st.spinner("Generating questions..."):
        docs = split_text(text_input)
        try:
            # summarize if text is too long to fit in one request
            if len(docs) > 1 or (len(docs) > 1 and summary_content is not None and summary_content != ""):
                # very slow, only use if
                docs = summarize_docs(docs, summary_content)
            else:
                docs = docs[0]
            if isinstance(docs, str):
                st.session_state.last_summary = docs
            elif hasattr(docs, "page_content"):
                st.session_state.last_summary = docs.page_content
            st.session_state.quiz = generate_questions(docs, summary_content, num_questions)
        except APIConnectionError:
            st.error("Connection to server failed. "
                     "Make sure the LLM server is running and reachable at the specified URL.")
        except AuthenticationError:
            st.error("Invalid OpenAI API key. Please check the API key and try again.")
        except OutputParserException:
            st.error("Error parsing output. Please try again.")
            
def download_button(text_to_download, download_filename):
    if not isinstance(text_to_download, str):
        # Try JSON encode for everything else
        text_to_download = json.dumps(text_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(text_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(text_to_download).decode()

    dl_link = f"""
    <html>
    <head>
    <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>
    $('<a href="data:text/plain;base64,{b64}" download="{download_filename}">')[0].click()
    </script>
    </head>
    </html>
    """
    return dl_link


def download_file(text: str, filename: str):
    components.html(
        download_button(text, filename),
        height=0,
    )
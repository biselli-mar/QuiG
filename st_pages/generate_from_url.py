import logging
import streamlit as st
import requests
from urllib.parse import quote
from langchain_core.exceptions import OutputParserException
from openai import APIConnectionError, AuthenticationError

from extraction.extractor import extract_text
from generation.question_generation_chain import generate_questions
from generation.summarization import summarize_docs, split_text
from quiz.export import convert_to_gift
from quiz.question_list import list_questions

st.set_page_config(page_title="Quiz Generator", page_icon="📝")

quiz = None
selected_questions = []


def wipe_scraper_settings():
    st.session_state.scraper_url = None
    st.session_state.scraper_key = None
    st.session_state.generated = False
    st.session_state.quiz = None
def reset_state():
    st.session_state.generated = False
    st.session_state.quiz = None
    logging.info("State reset.")


if st.session_state.scraper_key is None:
    with st.form("config"):
        scraper_url_input = st.text_input("Scraper URL", placeholder="https://api.diffbot.com/v3/article",
                                    help="URL of the scraper server. Default is the Diffbot API if left blank.")
        key_input = st.text_input("API Key", type="password",
                                  help="Your Scraper API key if there is one.")

        if not st.session_state.api_key:
            st.info("Please add your API key to continue.", icon="🗝️")

        submitted = st.form_submit_button("Submit")

        if submitted:
            if scraper_url_input != "":
                st.session_state.scraper_url = scraper_url_input
            st.session_state.scraper_key = key_input
            st.rerun()
else:
    st.button("Change scraper settings", on_click=wipe_scraper_settings)
    with st.form("config"):
        url_input = st.text_input("URL", placeholder="https://article-url.com",
                                  help="URL of the article text to generate questions from.")

        submitted = st.form_submit_button("Submit")

        if submitted:
            with st.spinner("Extracting text..."):
                api_url = st.session_state.scraper_url + "?url=" + quote(url_input) + "&token=" + st.session_state.scraper_key
                headers = {"accept": "application/json"}

                try:
                    response = requests.get(api_url, headers=headers)
                    response.raise_for_status()
                except APIConnectionError:
                    st.error("Connection to server failed. "
                             "Make sure the server is running and reachable at the specified URL.")
                except AuthenticationError:
                    st.error("Invalid API key. Please check the API key and try again.")
                except OutputParserException:
                    st.error("Error parsing output. Please try again.")

            st.session_state.scraper_extracted_text = response.json()["objects"][0]["text"]
    
    if st.session_state.scraper_extracted_text is not None:
        text_input = st.text_area("Text", st.session_state.scraper_extracted, height=300)

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

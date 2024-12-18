import streamlit as st
import requests
from urllib.parse import quote
from langchain_core.exceptions import OutputParserException
from openai import APIConnectionError, AuthenticationError

from st_pages.question_generator import question_generator

st.set_page_config(page_title="Quiz Generator", page_icon="📝")

quiz = None
selected_questions = []


def wipe_scraper_settings():
    st.session_state.scraper_url = None
    st.session_state.scraper_key = None
    st.session_state.generated = False
    st.session_state.quiz = None


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
        text_input = st.text_area("Text", st.session_state.scraper_extracted_text, height=300)

        question_generator(text_input)

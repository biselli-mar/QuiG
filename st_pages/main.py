import streamlit as st

st.set_page_config(page_title="Moodle-Quiz-Generator", page_icon="🛩️")
st.title("🛩️ Moodle-Quiz-Generator")

st.write("This app generates quiz questions from a given text. "
         "Upload a PDF or LaTeX document and generate questions based on the extracted text.")
st.write("The generated questions can be downloaded in GIFT format and imported into Moodle.")
st.write("This app uses the OpenAI API for question generation. "
         "To use the app, you either need an API key from OpenAI "
         "or [run this app locally](https://github.com/naedmi/moodle-quiz-generator) "
         "with a self-hosted LLM server. ")
st.write("You can get your OpenAI API key [here](https://platform.openai.com/account/api-keys). "
         "For local deployment, you can put anything as the API key.")

with st.form("config"):
    url_input = st.text_input("URL", placeholder="https://api.openai.com/v1/ or http://localhost:1234/v1/",
                              help="URL of the LLM server. Default is the OpenAI API.")
    key_input = st.text_input("API Key", type="password",
                              help="Your OpenAI API key or any string for local deployment.")

    if not st.session_state.api_key:
        st.info("Please add your API key to continue.", icon="🗝️")

    submitted = st.form_submit_button("Submit")

    if submitted:
        st.session_state.url = url_input
        st.session_state.api_key = key_input
        st.rerun()

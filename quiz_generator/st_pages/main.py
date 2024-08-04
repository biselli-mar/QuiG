import streamlit as st

st.set_page_config(page_title="Moodle-Quiz-Generator", page_icon="🛩️")
st.title("🛩️ Moodle-Quiz-Generator")

st.write("This app generates quiz questions from a given text. "
         "Upload a PDF or LaTeX document and generate questions based on the extracted text.")
st.write("The generated questions can be downloaded in GIFT format and imported into Moodle.")
st.write("The app uses the OpenAI API for question generation. "
         "To use the app, you either need an API key from OpenAI or host a local instance of a LLM server. "
         "You can get your OpenAI API key [here](https://platform.openai.com/account/api-keys). "
         "For local deployment, you can put anything as the API key.")

with st.form("config"):
    url_input = st.text_input("URL", value="http://localhost:1234/v1")
    if not st.session_state.url:
        st.info("Please add the URL of the LLM server to continue.", icon="🌐")

    key_input = st.text_input("API Key", type="password")
    if not st.session_state.api_key:
        st.info("Please add your API key to continue.", icon="🗝️")
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.session_state.url = url_input
        st.session_state.api_key = key_input
        st.rerun()

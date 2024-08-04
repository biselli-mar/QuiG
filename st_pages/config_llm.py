import streamlit as st

st.set_page_config(page_title="Configuration", page_icon=":gear:")
st.title("🛠️ LLM Configuration")

st.write("This app uses the OpenAI API for question generation. You can use the [API Key]"
         "(https://platform.openai.com/account/api-keys) from your OpenAI account "
         "or host a local instance of a LLM server.")

st.divider()
st.subheader("Local Deployment")

st.write("For a local deployment, you can use e.g. [LM Studio](https://lmstudio.ai/) or "
         "[Ollama](https://ollama.com/) or any other LLM server that supports the OpenAI API.")

st.markdown("""#### Recommended LLM Studio Setup
* Model: lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF
* In `Server Model Settings`/`Advanced Configuration`:
  - Context Length: 10000 to 131072 depending on the document size and hardware capabilities
  - Temperature: 0.0
  - _GPU Acceleration_ according to your setup""")


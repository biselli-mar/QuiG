import streamlit as st


def update_prompts():
    st.session_state.map_prompt = st.session_state.map_prompt_input
    st.session_state.reduce_prompt = st.session_state.reduce_prompt_input
    st.session_state.map_prompt_input = st.session_state.map_prompt
    st.session_state.reduce_prompt_input = st.session_state.reduce_prompt


def update_query():
    st.session_state.generate_query = st.session_state.generate_query_input
    st.session_state.generate_query_input = st.session_state.generate_query


st.set_page_config(page_title="Configuration", page_icon=":gear:")
st.title("🛠️ Prompt Configuration")

st.write("This page allows you to configure settings for the quiz generator app.")
st.write("You can modify the templates below to customize the prompts and queries used in the app, "
         "for example to change the language of the prompts.")

st.divider()
st.subheader("Prompts for the map-reduce chain")

st.text_area("Map Prompt Template. Use {text} as a placeholder.",
             value=st.session_state.map_prompt,
             height=250, key="map_prompt_input",
             on_change=update_prompts)
st.text_area("Reduce Prompt Template. Use {text} as a placeholder.",
             value=st.session_state.reduce_prompt,
             height=250, key="reduce_prompt_input",
             on_change=update_prompts)

st.divider()
st.subheader("Query for question generation")

st.text_area("Generate Query. Use {num_questions} and {text} as placeholders.",
             value=st.session_state.generate_query,
             height=150, key="generate_query_input",
             on_change=update_query)

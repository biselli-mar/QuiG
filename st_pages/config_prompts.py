import streamlit as st
from const import map_prompt_template, reduce_prompt_template, generate_query

st.set_page_config(page_title="Configuration", page_icon=":gear:")
st.title("🛠️ Prompt Configuration")

st.write("This page allows you to configure settings for the quiz generator app.")
st.write("You can modify the templates below to customize the prompts and queries used in the app, "
         "for example to change the language of the prompts.")

st.divider()
st.subheader("Prompts for the map-reduce chain")
map_prompt_template = st.text_area("Map Prompt Template. Use {text} as a placeholder.",
                                   value=map_prompt_template, height=200, key="map_prompt_template")
reduce_prompt_template = st.text_area("Reduce Prompt Template. Use {text} as a placeholder.",
                                      value=reduce_prompt_template, height=200, key="reduce_prompt_template")

st.divider()
st.subheader("Query for question generation")
generate_query = st.text_area("Generate Query. Use {num_questions} and {text} as placeholders.",
                              value=generate_query, height=150, key="generate_query")

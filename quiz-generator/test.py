import streamlit as st

form = st.form("my_form")
form.slider("Inside the form")
st.slider("Outside the form")

# Now add a submit button to the form:
form.form_submit_button("Submit")

# generate_questions_prompt = PromptTemplate(input_variables=["text", "num_questions"], template="Du bist ein
# Assistent, der damit beauftragt ist, Quizfragen zu generieren." "Du kannst nur auf Deutsch antworten, ohne Beisätze
# oder unnötige Informationen. \n\n" "Generiere {num_questions} Quizfragen aus dem folgenden Text: \n\n" "{text} \n\n
# " "Fragen:")

# DEFAULT_LLAMA_SEARCH_PROMPT = PromptTemplate(
#     input_variables=["text", "num_questions"],
#     template="""<<SYS>> \n Du bist ein Assistent, der damit beauftragt ist, Quizfragen zu generieren.
#     Du kannst nur auf Deutsch und im JSON-Format antworten, ohne Beisätze oder unnötige Informationen. \n\n
#     Nutze das folgende Format: \n\n
#     {{ "question": "Fragetext", \n
#     "answer": "Antworttext" }} \n\n
#     <</SYS>> \n\n
#     [INST] Generiere {num_questions} Quizfragen aus dem folgenden Text: \n\n {text} \n\n Fragen: \n\n
#     [/INST]""",
# )

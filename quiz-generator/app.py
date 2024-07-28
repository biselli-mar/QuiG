import streamlit as st
from openai import APIConnectionError

from extractor import extract_text_from_pdf, extract_text_from_latex
from main import generate_questions, convert_to_gift, summarize_docs, split_text
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "Moodle Quiz Generator"
os.environ["LANGCHAIN_API_KEY"] = "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"

quiz = None
selected_questions = []

if 'generated' not in st.session_state:
    st.session_state.generated = False

if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = []

if 'quiz' not in st.session_state:
    st.session_state.quiz = None


@st.cache_data(ttl=3600, show_spinner=False)
def extract_text(file):
    if file.type == "application/pdf":
        text = extract_text_from_pdf(file.read())
    else:
        text = extract_text_from_latex(file.read())
    return text


@st.cache_data(ttl=3600, show_spinner=False)
def get_quiz(text, num_questions):
    return generate_questions(text, num_questions)


def list_questions(quiz):
    if not quiz or not quiz.questions:
        return
    for i, q in enumerate(quiz.questions):
        with ((st.container())):
            col1, col2 = st.columns([0.05, 0.95])
            with col1:
                selected = st.checkbox("Select",
                                       key=f"select_{i}",
                                       label_visibility="collapsed")
            with col2:
                with st.expander(f"Frage {i}", expanded=True):
                    q.question = st.text_input("Frage",
                                               value=q.question,
                                               key=f"question_{i}",
                                               label_visibility="collapsed")
                    st.write("Antworten:")
                    for j, answer in enumerate(q.answers):
                        answer_col1, answer_col2 = st.columns([0.02, 0.98])
                        with answer_col1:
                            st.write(chr(65 + j))
                        with answer_col2:
                            q.answers[j] = st.text_input(f"Antwort {j} für Frage {i}",
                                                         value=answer,
                                                         key=f"answer_{i}_{j}",
                                                         label_visibility="collapsed")

                    q.correct_answer = ord(st.selectbox(f"Korrekte Antwort für Frage {i}",
                                                        options=[chr(65 + j) for j in range(len(q.answers))],
                                                        index=q.correct_answer,
                                                        key=f"correct_{i}")) - 65
            if selected:
                selected_questions.append(q)


def main():
    st.title("Quiz-Generator")

    uploaded_file = st.file_uploader("Wählen Sie eine PDF- oder LaTeX-Datei", type=["pdf", "tex"],
                                     accept_multiple_files=False)

    if uploaded_file is not None:
        with st.spinner("Extrahiere Text..."):
            text = extract_text(uploaded_file)
        user_input = st.text_area("Text", text, height=300, key="extracted_text")

        st.divider()
        st.header("Fragen generieren")

        with st.form("generate_questions"):

            num_questions = st.select_slider("Anzahl der Fragen", options=range(1, 11), value=5)
            submitted = st.form_submit_button("Generieren")

            if submitted:
                with st.spinner("Generiere Fragen..."):
                    docs = split_text(user_input)
                    try:
                        # only when text is too long for context window
                        if len(docs) > 1:
                            docs = summarize_docs(docs)
                        summary = docs
                    except APIConnectionError:
                        st.error(f"Verbindung zum API-Server fehlgeschlagen. Stelle sicher, dass der"
                                 " LLM-Server läuft und unter der angegebenen URL erreichbar ist.")
                        return
                    # generate_questions(summary, num_questions)
                    st.session_state.quiz = get_quiz(summary, num_questions)
                    st.session_state.generated = True

        if st.session_state.generated:
            st.write("Generierte Fragen:")
            list_questions(st.session_state.quiz)

            st.download_button("Ausgewählte Fragen herunterladen", convert_to_gift(selected_questions),
                               "questions.gift", "text/plain")


if __name__ == "__main__":
    main()

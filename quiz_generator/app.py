import logging
import sys

import streamlit as st
from openai import APIConnectionError
from pydantic import TypeAdapter

from extractor import extract_text_from_pdf, extract_text_from_latex
from main import generate_questions, convert_to_gift, summarize_docs, split_text
import os

from Quiz import MultipleChoiceQuestion, TrueFalseQuestion, ShortAnswerQuestion, Question, Quiz

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "Moodle Quiz Generator"
os.environ["LANGCHAIN_API_KEY"] = "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"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

quiz = None
selected_questions = []

if 'generated' not in st.session_state:
    st.session_state.generated = False

if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = []

if 'quiz' not in st.session_state:
    st.session_state.quiz = Quiz(questions=[])


@st.cache_data(ttl=3600, show_spinner=False)
def extract_text(file):
    if file.type == "application/pdf":
        text = extract_text_from_pdf(file.read())
    else:
        text = extract_text_from_latex(file.read())

    return text


@st.cache_data(ttl=3600, show_spinner=False)
def get_quiz(_text, num_questions):
    return generate_questions(_text, num_questions)


@st.experimental_fragment()
def show_multiple_choice_question(q, i):
    for j, answer in enumerate(q.answers):
        answer_col1, answer_col2 = st.columns([0.02, 0.98])
        with answer_col1:
            st.write(chr(65 + j))
        with answer_col2:
            q.answers[j] = st.text_input(f"Answer {j}",
                                         value=answer,
                                         key=f"answer_{i}_{j}",
                                         label_visibility="collapsed")
    if st.button("Add answer", key=f"add_answer_{q.question}"):
        q.answers.append("")
    q.correct_answer = ord(st.selectbox("Correct answer",
                                        options=[chr(65 + j) for j in range(len(q.answers))],
                                        index=q.correct_answer,
                                        key=f"correct_{i}")) - 65


@st.experimental_fragment()
def show_true_false_question(q, i):
    answer_col1, answer_col2 = st.columns([0.02, 0.98])
    with answer_col1:
        st.write("A")
        st.write("B")
    with answer_col2:
        st.write("True")
        st.write("False")
    q.correct_answer = TypeAdapter(bool).validate_python(
        st.selectbox("Correct answer",
                     options=["True", "False"],
                     index=q.correct_answer,
                     key=f"correct_{i}"))


@st.experimental_fragment()
def show_short_answer_question(q, i):
    for j, answer in enumerate(q.answers):
        answer_col1, answer_col2 = st.columns([0.02, 0.98])
        with answer_col1:
            st.write(chr(65 + j))
        with answer_col2:
            q.answers[j] = st.text_input(f"Answer {j}",
                                         value=answer,
                                         key=f"answer_{i}_{j}",
                                         label_visibility="collapsed")
    if st.button("Add answer", key=f"add_answer_{q.question}"):
        q.answers.append("")


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
                with st.expander(f"Question {i + 1}", expanded=True):
                    q.question = st.text_input("Frage",
                                               value=q.question,
                                               key=f"question_{i}",
                                               label_visibility="collapsed")
                    st.write("Answer options:")
                    # streamlit dev mode might mess with this because of the way it reloads modules
                    # -> class identities change and isinstance checks fail
                    if isinstance(q, MultipleChoiceQuestion) or isinstance(q, Question):
                        show_multiple_choice_question(q, i)
                    elif isinstance(q, TrueFalseQuestion):
                        show_true_false_question(q, i)
                    elif isinstance(q, ShortAnswerQuestion):
                        show_short_answer_question(q, i)
                    else:
                        st.error("Unknown question type.")
            if selected:
                selected_questions.append(q)


def main():
    st.session_state.generated = False
    get_quiz.clear()
    st.title("Quiz-Generator")

    uploaded_file = st.file_uploader("Upload a document (PDF or LaTeX)",
                                     type=["pdf", "tex"],
                                     accept_multiple_files=False)

    if uploaded_file is not None:
        with st.spinner("Extracting text..."):
            text = extract_text(uploaded_file)
        user_input = st.text_area("Text", text, height=300, key="extracted_text")

        st.divider()
        st.header("Questions")

        with st.form("generate_questions"):
            num_questions = st.select_slider("Number of questions",
                                             options=range(1, 11), value=5)
            if st.form_submit_button("Generate"):
                with st.spinner("Generating questions..."):
                    docs = split_text(user_input)
                    try:
                        # only when text is too long for context window
                        if len(docs) > 1:
                            docs = summarize_docs(docs)
                        st.session_state.quiz = get_quiz(docs, num_questions)
                        st.session_state.generated = True
                    except APIConnectionError:
                        st.error("Connection to server failed. "
                                 "Make sure the LLM server is running and reachable at the specified URL.")
                        return

        if st.session_state.generated:
            st.write("Generated questions:")
            list_questions(st.session_state.quiz)

            st.download_button("Download selected questions", convert_to_gift(selected_questions),
                               "questions.gift", "text/plain")


if __name__ == "__main__":
    main()

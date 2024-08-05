import logging
import streamlit as st
from pydantic import TypeAdapter
from streamlit.errors import StreamlitAPIException

from quiz.quiz import MultipleChoiceQuestion, TrueFalseQuestion, ShortAnswerQuestion


def list_questions(quiz, selected_questions):
    if not quiz or not quiz.questions:
        logging.info("No questions to list.")
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
                    # streamlit dev mode might mess with this because of the way it reloads modules
                    # -> class identities change and isinstance() checks fail on existing objects
                    if isinstance(q, MultipleChoiceQuestion):
                        show_multiple_choice_question(q, i)
                    elif isinstance(q, TrueFalseQuestion):
                        show_true_false_question(q, i)
                    elif isinstance(q, ShortAnswerQuestion):
                        show_short_answer_question(q, i)
                    else:
                        st.error("Unknown question type.")

            if selected:
                selected_questions.append(q)


def show_multiple_choice_question(q, i):
    st.write("Answer options:")
    list_answer_options(q, i)
    try:
        q.correct_answer = ord(st.selectbox("Correct answer",
                                            options=[chr(65 + j) for j in range(len(q.answers))],
                                            index=q.correct_answer,
                                            key=f"correct_{i}")) - 65
    except StreamlitAPIException:
        logging.error(f"Answer index out of bounds for question {i}. Defaulting to 0.")
        q.correct_answer = ord(st.selectbox("Correct answer",
                                            options=[chr(65 + j) for j in range(len(q.answers))],
                                            index=0,
                                            key=f"correct_{i}")) - 65


def show_true_false_question(q, i):
    q.correct_answer = TypeAdapter(bool).validate_python(
        st.selectbox("Correct answer",
                     options=["True", "False"],
                     index=q.correct_answer,
                     key=f"answer_{i}"))


def show_short_answer_question(q, i):
    st.write("Valid answer options:")
    list_answer_options(q, i)


def list_answer_options(q, i):
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
        st.rerun()

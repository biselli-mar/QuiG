import streamlit as st
from extractor import extract_text_from_pdf, extract_text_from_latex
from main import generate_questions, parse_questions, convert_to_gift
from question import Question

# Sample questions
sample_questions = [
    Question("What is the capital of France?", ["Paris", "London", "Berlin", "Madrid"], 0),
    Question("What is 2 + 2?", ["3", "4", "5", "6"], 1),
    Question("What is the largest planet?", ["Earth", "Mars", "Jupiter", "Saturn"], 2)
]
selected_questions = []


def update_text(value):
    st.session_state.text = value


def list_questions(questions):
    for i, q in enumerate(questions):
        with st.container():
            col1, col2 = st.columns([0.05, 0.95])
            with col1:
                selected = st.checkbox("Select",
                                       key=f"select_{i}",
                                       label_visibility="collapsed")
            with col2:
                with st.expander(f"Frage {i}", expanded=True):
                    question_text = st.text_input("Frage",
                                                  value=q.question,
                                                  key=f"question_{i}",
                                                  label_visibility="collapsed")
                    st.write("Antworten:")
                    answers = []
                    for j, answer in enumerate(q.answers):
                        answer_col1, answer_col2 = st.columns([0.02, 0.98])
                        with answer_col1:
                            st.write(chr(65 + j))
                        with answer_col2:
                            answer_text = st.text_input(f"Antwort {chr(65 + j)} für Frage {i}",
                                                        value=answer,
                                                        key=f"answer_{i}_{j}",
                                                        label_visibility="collapsed")
                            answers.append(answer_text)
                    correct_answer = st.selectbox(f"Korrekte Antwort für Frage {i}",
                                                  options=[chr(65 + j) for j in range(len(q.answers))],
                                                  index=q.correct_answer,
                                                  key=f"correct_{i}")
                    if selected:
                        selected_questions.append(Question(question_text, answers, ord(correct_answer) - 65))


def main():
    st.title("Quiz-Generator")

    # Initialize session state
    if 'text' not in st.session_state:
        st.session_state.text = 'original'

    uploaded_file = st.file_uploader("Wählen Sie eine PDF- oder LaTeX-Datei", type=["pdf", "tex"])

    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            with st.spinner('Extrahiere Text aus PDF...'):
                st.session_state.text = extract_text_from_pdf(uploaded_file)
                update_text(st.session_state.text)
        else:
            with st.spinner('Extrahiere Text aus LaTeX...'):
                st.session_state.text = extract_text_from_latex(uploaded_file)
                update_text(st.session_state.text)

        st.text_area("Text", st.session_state.text, height=300, key="extracted_text")

        st.divider()
        st.header("Fragen generieren")

        num_questions = st.select_slider("Anzahl der Fragen", options=range(1, 11), value=5)

        if st.button("Fragen generieren"):
            questions_text = generate_questions(st.session_state.text, num_questions)
            questions = parse_questions(questions_text)
            st.write("Generierte Fragen:")
            list_questions(questions)

        list_questions(sample_questions)  # should be indentend later

        st.download_button("Fragen herunterladen", convert_to_gift(selected_questions), "questions.gift", "text/plain")


if __name__ == "__main__":
    main()

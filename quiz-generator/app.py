import streamlit as st
from extractor import extract_text_from_pdf, extract_text_from_latex
from main import generate_questions, parse_questions, convert_to_gift
from question import Question


def main():
    st.title("Quiz Generator")

    uploaded_file = st.file_uploader("Wählen Sie eine PDF- oder LaTeX-Datei", type=["pdf", "tex"])
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        else:
            text = extract_text_from_latex(uploaded_file)

        st.write("Extrahierter Text:")
        st.text_area("Text", text, height=300)

        num_questions = st.select_slider("Anzahl der Fragen", options=range(1, 11), value=5)

        if st.button("Fragen generieren"):

            questions_text = generate_questions(text, num_questions)
            questions = parse_questions(questions_text)
            st.write("Generierte Fragen:")
            for q in questions:
                st.write(f"Frage: {q['question']}")
                st.write(f"Antwort: {q['answer']}")

            if st.button("In GIFT exportieren"):
                gift_format = convert_to_gift(questions)
                st.download_button("GIFT-Datei herunterladen", gift_format, file_name="quiz.gift")

        selected_questions = []
        # Sample questions
        questions = [
            Question("What is the capital of France?", ["Paris", "London", "Berlin", "Madrid"], 0),
            Question("What is 2 + 2?", ["3", "4", "5", "6"], 1),
            Question("What is the largest planet?", ["Earth", "Mars", "Jupiter", "Saturn"], 2)
        ]
        for i, q in enumerate(questions):
            with st.container():
                col1, col2 = st.columns([0.05, 0.95])
                with col1:
                    selected = st.checkbox(f"Select {i}", key=f"select_{i}", label_visibility="collapsed")
                with col2:
                    with st.expander(f"Question {i}", expanded=True):
                        question_text = st.text_input(f"Question {i}", value=q.question, key=f"question_{i}",
                                                      label_visibility="collapsed")
                        st.write("Answers:")
                        answers = []
                        for j, answer in enumerate(q.answers):
                            answer_col1, answer_col2 = st.columns([0.02, 0.98])
                            with answer_col1:
                                st.write(chr(65 + j))
                            with answer_col2:
                                answer_text = st.text_input(f"Answer {chr(65 + j)} for Question {i}", value=answer,
                                                            key=f"answer_{i}_{j}", label_visibility="collapsed")
                                answers.append(answer_text)
                        correct_answer = st.selectbox(f"Correct Answer for Question {i}",
                                                      options=range(len(q.answers)),
                                                      index=q.correct_answer, 
                                                      key=f"correct_{i}")
                        if selected:
                            selected_questions.append(Question(question_text, answers, correct_answer))

        if st.button("Process Selected Questions"):
            st.write("Selected Questions:")
            for sq in selected_questions:
                st.write(f"Question: {sq.question}")
                st.write(f"Answers: {sq.answers}")
                st.write(f"Correct Answer: {sq.answers[sq.correct_answer]}")


if __name__ == "__main__":
    main()

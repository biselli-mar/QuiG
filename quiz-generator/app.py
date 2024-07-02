import streamlit as st
from extractor import extract_text_from_pdf, extract_text_from_latex
from main import generate_questions, parse_questions, convert_to_gift


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

        if st.button("Fragen generieren"):
            questions_text = generate_questions(text)
            questions = parse_questions(questions_text)
            st.write("Generierte Fragen:")
            for q in questions:
                st.write(f"Frage: {q['question']}")
                st.write(f"Antwort: {q['answer']}")

            if st.button("In GIFT exportieren"):
                gift_format = convert_to_gift(questions)
                st.download_button("GIFT-Datei herunterladen", gift_format, file_name="quiz.gift")


if __name__ == "__main__":
    main()

import streamlit as st
from extractor import extract_text_from_pdf
from main import generate_questions, convert_to_gift
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "Moodle Quiz Generator"
os.environ["LANGCHAIN_API_KEY"] = "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"

# Sample questions
# sample_questions = [
#     Question("What is the capital of France?", ["Paris", "London", "Berlin", "Madrid"], 0),
#     Question("What is 2 + 2?", ["3", "4", "5", "6"], 1),
#     Question("What is the largest planet?", ["Earth", "Mars", "Jupiter", "Saturn"], 2)
# ]
selected_questions = []


@st.cache_data(ttl=3600, show_spinner=False)
def extract_text(file):
    # if file.type == "application/pdf":
    text = extract_text_from_pdf(file)
    # else:
    #    text = extract_text_from_latex(file)
    return text


def update_text(value):
    st.session_state.text = value


def list_questions(questions):
    for i, q in questions: # enumerate(questions):
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
                    for j, answer in q.answers:  # enumerate(q.answers):
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

    # Initialize session state
    # if 'text' not in st.session_state:
    #     st.session_state.text = 'original'

    uploaded_file = st.file_uploader("Wählen Sie eine PDF- oder LaTeX-Datei", type=["pdf", "tex"])

    if uploaded_file is not None:
        with st.spinner("Extrahiere Text..."):
            text = extract_text(uploaded_file.read())
        user_input = st.text_area("Text", text, height=300, key="extracted_text")

        st.divider()
        st.header("Fragen generieren")

        num_questions = st.select_slider("Anzahl der Fragen", options=range(1, 11), value=5)

        if st.button("Fragen generieren"):
            quiz = generate_questions(user_input, num_questions)
            # questions = parse_questions(questions_text)
            st.write("Generierte Fragen:")
            list_questions(quiz.questions)
            st.download_button("Fragen herunterladen", convert_to_gift(selected_questions),
                               "questions.gift", "text/plain")

        # list_questions(sample_questions)  # should be indentend later


if __name__ == "__main__":
    main()

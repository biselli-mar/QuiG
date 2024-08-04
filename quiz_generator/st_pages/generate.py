import logging

import streamlit as st
from langchain.chains.summarize import load_summarize_chain
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_text_splitters import MarkdownTextSplitter
from openai import APIConnectionError
from pydantic import TypeAdapter
import sys

sys.path.append("../")

from Quiz import MultipleChoiceQuestion, TrueFalseQuestion, ShortAnswerQuestion, Quiz, Question
from extractor import extract_text_from_pdf, extract_text_from_latex
from const import CHUNK_SIZE, CHUNK_OVERLAP, MAX_TOKENS

st.set_page_config(page_title="Quiz Generator", page_icon="📝")

quiz = None
selected_questions = []

if 'generated' not in st.session_state:
    st.session_state.generated = False

if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = []

if 'quiz' not in st.session_state:
    st.session_state.quiz = Quiz(questions=[])

# Initialize the ChatOpenAI model with local server URL
llm = ChatOpenAI(
    api_key=st.session_state.api_key or "lmstudio",
    max_retries=2,
    base_url=st.session_state.url or "http://localhost:1234/v1/"
)

# Set up a parser for Quiz object
parser = PydanticOutputParser(pydantic_object=Quiz)

generate_questions_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an assistant tasked with generating quiz questions. You can only respond in the language "
            "used in the input text, "
            "without clauses or unnecessary information.\n{format_instructions}"
        ),
        (
            "human",
            "{query}")
    ]
).partial(format_instructions=parser.get_format_instructions())

#         (
#             "system",
#             "You are an assistant tasked with generating quiz questions. You can only respond in German, "
#             "without clauses or unnecessary information."
#         )


# Combine the prompt template, language model, and parser into a chain
question_chain = generate_questions_prompt | llm | parser


@st.cache_data(ttl=3600, show_spinner=False)
def split_text(text):
    """
    Split the input text into smaller chunks using MarkdownTextSplitter.

    Args:
        text (str): The input text to be split.

    Returns:
        list: A list of document chunks.
    """
    splitter = MarkdownTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP)
    docs = splitter.create_documents([text])
    logging.info("Text split into %s document(s).", len(docs))
    return docs


def summarize_docs(docs):
    """
    Summarize the list of document chunks using a map-reduce chain.

    Args:
        docs (list): The list of document chunks to be summarized.

    Returns:
        str: The summarized text.
    """

    map_prompt = PromptTemplate(template=st.session_state.map_prompt_template, input_variables=["text"])
    reduce_prompt = PromptTemplate(template=st.session_state.reduce_prompt_template, input_variables=["text"])
    sum_chain = load_summarize_chain(
        llm,
        chain_type="map_reduce",
        map_prompt=map_prompt,
        combine_prompt=reduce_prompt,
        token_max=MAX_TOKENS
    )

    logging.info("Invoking map-reduce chain...")
    summary = sum_chain.invoke(docs)
    logging.info("Map-reduce chain finished.")

    logging.info("Summary: %s", summary["output_text"])
    return summary["output_text"]


@st.cache_data(ttl=3600, show_spinner=False)
def generate_questions(_text, num_questions=5):
    """
    Generate quiz questions from the input text.

    Args:
        _text (str): The input text to generate questions from.
        num_questions (int): The number of questions to generate.

    Returns:
        Quiz: The generated quiz object.
    """
    response = question_chain.invoke({
        "query": st.session_state.generate_query.format(num_questions=num_questions,
                                                        text=_text)})
    logging.info("Generated questions: %s", response)
    return response


def convert_to_gift(questions):
    """
    Convert the generated questions to GIFT format.

    Args:
        questions (list): The list of generated questions.

    Returns:
        str: The questions in GIFT format.
    """
    gift_format = ""
    for q in questions:
        gift_format += str(q) + "\n\n"
    return gift_format


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


@st.experimental_fragment()
def list_questions(quiz):
    if not quiz or not quiz.questions:
        print("No questions to list.")
        return
    for i, q in enumerate(quiz.questions):
        with ((st.container())):
            col1, col2 = st.columns([0.05, 0.95])
            with col1:
                selected = st.checkbox("Select",
                                       key=f"select_{i}",
                                       label_visibility="collapsed",
                                       on_change=lambda: st.session_state.selected_questions.append(q)
                                       if q not in st.session_state.selected_questions
                                       else st.session_state.selected_questions.remove(q))
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


get_quiz.clear()
uploaded_file = st.file_uploader("Upload a document (PDF or LaTeX)",
                                 type=["pdf", "tex"],
                                 accept_multiple_files=False)

if uploaded_file is not None:
    with st.spinner("Extracting text..."):
        text = extract_text(uploaded_file)
    user_input = st.text_area("Text", text, height=300, key="extracted_text")

    st.divider()
    st.header("Questions")
    print("generated1?", st.session_state.generated)

    with st.form("generate_questions"):
        num_questions = st.select_slider("Number of questions to generate",
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
                    print("generated2?", st.session_state.generated)
                except APIConnectionError:
                    st.error("Connection to server failed. "
                             "Make sure the LLM server is running and reachable at the specified URL.")
                    st.stop()  # return

    if st.session_state.generated:
        st.write("Generated questions:")
        list_questions(st.session_state.quiz)

        st.download_button("Download selected questions", convert_to_gift(selected_questions),
                           "questions.gift", "text/plain")

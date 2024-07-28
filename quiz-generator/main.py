import logging
import os
import streamlit as st

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_text_splitters import MarkdownTextSplitter
from langchain.chains.summarize import load_summarize_chain
from Quiz import Quiz

# Set the OpenAI API key environment variable
os.environ["OPENAI_API_KEY"] = "x"

# Initialize the ChatOpenAI model with local server URL
llm = ChatOpenAI(
    model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    base_url="http://localhost:1234/v1/",  # Local server URL - LM Studio in this case
)

# Set up a parser for Quiz object
parser = PydanticOutputParser(pydantic_object=Quiz)

query = "Generiere {num_questions} Quizfragen aus dem folgenden Text: \n\n {text}"

generate_questions_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an assistant tasked with generating quiz questions. You can only respond in German, "
            "without clauses or unnecessary information. Wrap the output in `json` tags.\n{format_instructions}"
        ),
        ("human", "{query}")
    ]
).partial(format_instructions=parser.get_format_instructions())

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
        chunk_size=5000,
        chunk_overlap=200)
    docs = splitter.create_documents([text])
    logging.info("Text split into %s documents.", len(docs))
    return docs


def summarize_docs(docs):
    """
    Summarize the list of document chunks using a map-reduce chain.

    Args:
        docs (list): The list of document chunks to be summarized.

    Returns:
        str: The summarized text.
    """
    # add parallel processing
    # https://github.com/langchain-ai/langchain/discussions/21009

    sum_chain = load_summarize_chain(llm, chain_type="map_reduce")

    logging.info("Invoking map-reduce chain...")
    summary = sum_chain.invoke(docs)
    logging.info("Map-reduce chain finished.")

    logging.info("Summary: %s", summary)
    return summary["output_text"]


@st.cache_data(ttl=3600, show_spinner=False)
def generate_questions(text, num_questions=5):
    """
    Generate quiz questions from the input text.

    Args:
        text (str): The input text to generate questions from.
        num_questions (int): The number of questions to generate.

    Returns:
        Quiz: The generated quiz object.
    """
    # run chain for question generation with parsing as Quiz object
    response = question_chain.invoke({"query": query.format(num_questions=num_questions, text=text)})
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

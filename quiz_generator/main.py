import logging
import os

import streamlit as st
from langchain.chains.summarize import load_summarize_chain
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_text_splitters import MarkdownTextSplitter
from Quiz import Quiz

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
LLM = os.getenv("LLM")

# Initialize the ChatOpenAI model with local server URL
llm = ChatOpenAI(
    api_key=API_KEY,
    model=LLM,
    max_retries=2,
    base_url=BASE_URL,  # Local server URL - LM Studio in this case
)

# llm = ChatOpenAI(
#     api_key="ollama",
#     model="llama3.1",
#     base_url="http://localhost:11434/v1/",  # Local server URL - Ollama in this case
# )

# Set up a parser for Quiz object
parser = PydanticOutputParser(pydantic_object=Quiz)

query = "Generiere {num_questions} Quizfragen aus dem folgenden Text:\n{text}"

generate_questions_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an assistant tasked with generating quiz questions. You can only respond in German, "
            "without clauses or unnecessary information.\n{format_instructions}"
        ),
        (
            "human",
            "{query}")
    ]
).partial(format_instructions=parser.get_format_instructions())

# generate_questions_prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are an assistant tasked with generating quiz questions. You can only respond in German, "
#             "without clauses or unnecessary information."
#         ),
#         (
#             "human",
#             "{query}")
#     ]
# ).partial(query=query)


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
        chunk_size=30000,
        chunk_overlap=1000)
    docs = splitter.create_documents([text])
    logging.info("Text split into %s document(s).", len(docs))
    return docs


map_prompt_template = """Im Folgenden befindet sich eine Reihe von Dokumenten:

                        {text}
                        
                        Bitte identifiziere anhand der Liste von Dokumenten die Hauptthemen und wichtige Details.
                        Achte darauf, Beispiele und Definitionen wortgetreu zu übernehmen.
                        
                        Hilfreiche Antwort:"""

map_prompt = PromptTemplate(template=map_prompt_template, input_variables=["text"])

reduce_prompt_template = """Im Folgenden befindet sich eine Reihe von Zusammenfassungen:

                            {text}
                            
                            Nutze die Zusammenfassungen, um sie zu einer endgültigen, 
                            alles umfassenden Zusammenfassung zu kombinieren.
                            
                            Hilfreiche Antwort:"""

reduce_prompt = PromptTemplate(
    template=reduce_prompt_template, input_variables=["text"]
)


def summarize_docs(docs):
    """
    Summarize the list of document chunks using a map-reduce chain.

    Args:
        docs (list): The list of document chunks to be summarized.

    Returns:
        str: The summarized text.
    """

    sum_chain = load_summarize_chain(
        llm,
        chain_type="map_reduce",
        map_prompt=map_prompt,
        combine_prompt=reduce_prompt,
        token_max=5000  # default: 3000
    )

    logging.info("Invoking map-reduce chain...")
    summary = sum_chain.invoke(docs)
    logging.info("Map-reduce chain finished.")

    logging.info("Summary: %s", summary["output_text"])
    return summary["output_text"]


@st.cache_data(ttl=3600, show_spinner=False)  # , hash_funcs={Quiz: lambda x: x.dict()}
def generate_questions(_text, num_questions=5):
    # idee: pro doc eine frage generieren
    """
    Generate quiz questions from the input text.

    Args:
        _text (str): The input text to generate questions from.
        num_questions (int): The number of questions to generate.

    Returns:
        Quiz: The generated quiz object.
    """
    # run chain for question generation with parsing as Quiz object
    response = question_chain.invoke({"query": query.format(num_questions=num_questions, text=_text)})
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

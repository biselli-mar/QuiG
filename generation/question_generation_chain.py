import logging
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
from openai import AuthenticationError

from quiz.quiz import Quiz
from const import system_prompt
from generation import llm

parser = PydanticOutputParser(pydantic_object=Quiz)
generate_questions_prompt = (ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{query}")])
                             .partial(format_instructions=parser.get_format_instructions()))

question_chain = generate_questions_prompt | llm.llm | parser


@st.cache_data(ttl=3600, show_spinner=False)
def generate_questions(_text, question_num=5):
    """
    Generate quiz questions from the input text.

    Args:
        _text (str): The input text to generate questions from.
        question_num (int): The number of questions to generate.

    Returns:
        Quiz: The generated quiz object.
    """
    response = None
    try:
        response = question_chain.invoke({
            "query": st.session_state.generate_query.format(num_questions=question_num,
                                                            text=_text)})
        logging.info("Generated questions: %s", response)
    except AuthenticationError:
        st.error("Invalid OpenAI API key. Please check the API key and try again.")
    except OutputParserException:
        st.error("Error parsing output. Please try again.")
    return response

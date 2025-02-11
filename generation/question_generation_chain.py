import re
import logging
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
import streamlit as st

from quiz.quiz import Quiz
from const import system_prompt
from generation import llm

parser = PydanticOutputParser(pydantic_object=Quiz)
generate_questions_prompt = (ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{query}")])
                             .partial(format_instructions=parser.get_format_instructions()))

def escape_backslashes(s: AIMessage) -> AIMessage:
    s.content = str.replace(s.content, "\\", "\\\\")
    return s

question_chain = generate_questions_prompt | llm.llm | RunnableLambda(func=escape_backslashes) | parser

def generate_questions(_text, content_summary, question_num=5):
    """
    Generate quiz questions from the input text.

    Args:
        _text (str): The input text to generate questions from.
        question_num (int): The number of questions to generate.

    Returns:
        Quiz: The generated quiz object.
    """
    query = st.session_state.generate_query.format(num_questions=question_num, text=_text)
    if content_summary is not None and content_summary != "":
        query = st.session_state.generate_query_limited.format(num_questions=question_num, text=_text,summary_content=content_summary) 
    try:
        response = question_chain.invoke({
            "query": query})
    except OutputParserException as e:
        logging.error("Failed to generate questions: %s", e)
        if e.llm_output:
            text = re.sub(r"\\", "\\\\", e.llm_output)
            logging.info("Re-invoking parser with text: %s", f"{text}")
            response = parser.invoke(text)
        else:
            raise e
    logging.info("Generated questions: %s", response)
    return response

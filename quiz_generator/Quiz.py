from typing import Union
from langchain_core.pydantic_v1 import BaseModel, Field


class Question(BaseModel):
    """Class for storing a question and its answer choices."""
    question: str = Field(..., description="The question")
    answers: list[str] = Field(..., description="List of answer choices")
    correct_answer: int = Field(..., description="Index of the correct answer, from 0 to len(answers)-1")

    def __str__(self):
        newline = "\n"
        gift_format = f"{self.question} {{\n"
        for i, answer in enumerate(self.answers):
            gift_format += f"{'=' if i == self.correct_answer else '~'} {answer}"
            gift_format += newline
        gift_format += "}"

        return gift_format


class MultipleChoiceQuestion(BaseModel):
    """Class for storing a question and its answer choices."""
    question: str = Field(..., description="The question")
    answers: list[str] = Field(..., description="List of answer choices")
    correct_answer: int = Field(..., description="Index of the correct answer, from 0 to len(answers)-1")

    def __str__(self):
        newline = "\n"
        gift_format = f"{self.question} {{\n"
        for i, answer in enumerate(self.answers):
            gift_format += f"{'=' if i == self.correct_answer else '~'}{answer}"
            gift_format += newline
        gift_format += "}"

        return gift_format


class TrueFalseQuestion(BaseModel):
    """Class for storing a true/false question or statement."""
    question: str = Field(..., description="The question")
    correct_answer: bool = Field(..., description="Correct answer (True or False)")

    def __str__(self):
        gift_format = f"{self.question} {{\n"
        gift_format += f"{'TRUE' if self.correct_answer else 'FALSE'}"
        gift_format += f"\n}}"

        return gift_format


class ShortAnswerQuestion(BaseModel):
    """Class for storing a question with a short answer."""
    question: str = Field(..., description="The question")
    answers: list[str] = Field(..., description="Correct answer options")

    def __str__(self):
        gift_format = f"{self.question} {{\n"
        for i, answer in enumerate(self.answers):
            gift_format += f"={answer}"
            gift_format += "\n"
        gift_format += "}"

        return gift_format


class Quiz(BaseModel):
    questions: list[Union[MultipleChoiceQuestion, TrueFalseQuestion, ShortAnswerQuestion]] \
       = Field(..., description="List of questions in the quiz")

    def to_gift(self):
        gift_format = ""
        for i, question in enumerate(self.questions):
            gift_format += str(question) + "\n\n"

        return gift_format

from langchain_core.pydantic_v1 import BaseModel, Field


class Question(BaseModel):
    """Class for storing a question and its answer choices."""
    question: str = Field(..., description="The question")
    answers: list[str] = Field(..., description="List of answer choices (2-4 choices)")
    correct_answer: int = Field(..., description="Index of the correct answer, starting from 0")

    def __str__(self):
        newline = "\n"
        wrong_answers = self.answers[:self.correct_answer] + self.answers[self.correct_answer + 1:]
        return f"{self.question}{{\n={self.answers[self.correct_answer]}\n~{f'{newline}~'.join(wrong_answers)}\n}}"


class Quiz(BaseModel):
    questions: list[Question] = Field(..., description="List of questions in the quiz")

    def to_gift(self):
        gift_format = ""
        for i, question in enumerate(self.questions):
            gift_format += f"::Q{i}:: {question.question}\n"
            for j, answer in enumerate(question.answers):
                gift_format += f"{'=' if j == question.correct_answer else '~'} {answer}\n"
        return gift_format

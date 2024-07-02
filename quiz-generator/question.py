from dataclasses import dataclass


@dataclass
class Question:
    """Class for storing a question and its answer."""
    question: str
    answers: list[str]
    correct_answer: int


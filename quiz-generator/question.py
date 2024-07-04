from dataclasses import dataclass


@dataclass
class Question:
    """Class for storing a question and its answer choices."""
    question: str
    answers: list[str]
    correct_answer: int

    def __str__(self):
        newline = "\n"
        wrong_answers = self.answers[:self.correct_answer] + self.answers[self.correct_answer + 1:]
        return f"{self.question}{{\n={self.answers[self.correct_answer]}\n~{f'{newline}~'.join(wrong_answers)}\n}}"

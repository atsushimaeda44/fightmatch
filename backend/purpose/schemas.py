from pydantic import BaseModel


class QuestionOption(BaseModel):
    id: str
    label: str


class Question(BaseModel):
    id: int
    text: str
    type: str
    options: list[QuestionOption] | None = None


class Answer(BaseModel):
    question_id: int
    answer: str | list[str]

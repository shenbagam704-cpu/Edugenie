from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)

    @field_validator("text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Text cannot be empty.")
        return value


class TextResponse(BaseModel):
    result: str


class QAResponse(BaseModel):
    answer: str


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(min_length=3, max_length=3)


class LearningResource(BaseModel):
    title: str
    type: str
    url: str = ""
    description: str


class LearningStep(BaseModel):
    level: str
    topics: list[str]
    estimated_time: str
    goals: list[str]
    resources: list[LearningResource]


class LearningPathResponse(BaseModel):
    topic: str
    overview: str
    steps: list[LearningStep]

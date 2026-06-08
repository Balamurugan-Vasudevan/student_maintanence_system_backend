from pydantic import BaseModel, Field
from typing   import Optional, List
from datetime import datetime

class OptionModel(BaseModel):
    text:      str
    isCorrect: bool = False

class QuestionModel(BaseModel):
    question: str
    options:  List[OptionModel]

class QuizModel(BaseModel):
    id:           Optional[str]           = Field(default=None, alias="_id")
    user_id:      str
    title:        str
    description:  Optional[str]           = ""
    category:     str
    difficulty:   str
    visibility:   str                     = "public"
    time_limit:   Optional[int]           = None
    passing_score: Optional[int]          = None
    max_attempts: Optional[int]           = None
    questions:    List[QuestionModel]     = []
    status:       str                     = "draft"
    created_at:   Optional[datetime]      = None
    updated_at:   Optional[datetime]      = None

    class Config:
        populate_by_name    = True
        arbitrary_types_allowed = True
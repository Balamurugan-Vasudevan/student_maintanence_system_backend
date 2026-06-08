from pydantic import BaseModel
from typing   import Optional, List
from datetime import datetime

class OptionSchema(BaseModel):
    text:      str
    isCorrect: bool = False

class QuestionSchema(BaseModel):
    question: str
    options:  List[OptionSchema]

class CreateQuizSchema(BaseModel):
    title:         str
    description:   Optional[str]  = ""
    category:      str
    difficulty:    str
    visibility:    Optional[str]  = "public"
    time_limit:    Optional[int]  = None
    passing_score: Optional[int]  = None
    max_attempts:  Optional[int]  = None
    questions:     Optional[List[QuestionSchema]] = []

class UpdateQuizSchema(BaseModel):
    title:         Optional[str]  = None
    description:   Optional[str]  = None
    category:      Optional[str]  = None
    difficulty:    Optional[str]  = None
    visibility:    Optional[str]  = None
    time_limit:    Optional[int]  = None
    passing_score: Optional[int]  = None
    max_attempts:  Optional[int]  = None
    questions:     Optional[List[QuestionSchema]] = None

class QuizResponse(BaseModel):
    id:            str
    user_id:       str
    title:         str
    description:   Optional[str]
    category:      str
    difficulty:    str
    visibility:    str
    time_limit:    Optional[int]
    passing_score: Optional[int]
    max_attempts:  Optional[int]
    questions:     List[QuestionSchema]
    status:        str
    created_at:    Optional[datetime]
    updated_at:    Optional[datetime]
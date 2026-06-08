from fastapi               import APIRouter, Depends
from app.schemas.quiz      import CreateQuizSchema, UpdateQuizSchema
from app.controllers.quiz  import (
    get_all_quizzes, get_quiz,
    create_quiz, update_quiz,
    delete_quiz, publish_quiz
)
from app.middleware.auth   import get_current_user

router = APIRouter(prefix="/api/quiz", tags=["Quiz"])

@router.get("/")
async def list_quizzes(current_user: dict = Depends(get_current_user)):
    return await get_all_quizzes(current_user)

@router.post("/")
async def new_quiz(data: CreateQuizSchema, current_user: dict = Depends(get_current_user)):
    return await create_quiz(data, current_user)

@router.get("/{quiz_id}")
async def single_quiz(quiz_id: str, current_user: dict = Depends(get_current_user)):
    return await get_quiz(quiz_id, current_user)

@router.put("/{quiz_id}")
async def edit_quiz(quiz_id: str, data: UpdateQuizSchema, current_user: dict = Depends(get_current_user)):
    return await update_quiz(quiz_id, data, current_user)

@router.delete("/{quiz_id}")
async def remove_quiz(quiz_id: str, current_user: dict = Depends(get_current_user)):
    return await delete_quiz(quiz_id, current_user)

@router.patch("/{quiz_id}/publish")
async def publish(quiz_id: str, current_user: dict = Depends(get_current_user)):
    return await publish_quiz(quiz_id, current_user)
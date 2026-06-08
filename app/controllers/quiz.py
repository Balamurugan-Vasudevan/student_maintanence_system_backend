from fastapi    import HTTPException, status
from bson       import ObjectId
from datetime   import datetime
from app.database import get_db
from app.schemas.quiz import CreateQuizSchema, UpdateQuizSchema

async def get_all_quizzes(current_user: dict):
    db      = get_db()
    cursor  = db["quizzes"].find({"user_id": current_user["_id"]}).sort("created_at", -1)
    quizzes = await cursor.to_list(length=100)
    for q in quizzes:
        q["id"] = q["_id"]
    return quizzes

async def get_quiz(quiz_id: str, current_user: dict):
    db   = get_db()
    quiz = await db["quizzes"].find_one({"_id": quiz_id})

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if quiz["visibility"] == "private" and quiz["user_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    quiz["id"] = quiz["_id"]
    return quiz

async def create_quiz(data: CreateQuizSchema, current_user: dict):
    db   = get_db()
    quiz = {
        "_id":          str(ObjectId()),
        "user_id":      current_user["_id"],
        "title":        data.title,
        "description":  data.description,
        "category":     data.category,
        "difficulty":   data.difficulty,
        "visibility":   data.visibility,
        "time_limit":   data.time_limit,
        "passing_score": data.passing_score,
        "max_attempts": data.max_attempts,
        "questions":    [q.dict() for q in data.questions],
        "status":       "draft",
        "created_at":   datetime.utcnow(),
        "updated_at":   datetime.utcnow(),
    }
    await db["quizzes"].insert_one(quiz)
    quiz["id"] = quiz["_id"]
    return quiz

async def update_quiz(quiz_id: str, data: UpdateQuizSchema, current_user: dict):
    db   = get_db()
    quiz = await db["quizzes"].find_one({"_id": quiz_id})

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    if quiz["user_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    update_data = {k: v for k, v in data.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()

    if "questions" in update_data:
        update_data["questions"] = [q.dict() for q in data.questions]

    await db["quizzes"].update_one({"_id": quiz_id}, {"$set": update_data})
    updated = await db["quizzes"].find_one({"_id": quiz_id})
    updated["id"] = updated["_id"]
    return updated

async def delete_quiz(quiz_id: str, current_user: dict):
    db   = get_db()
    quiz = await db["quizzes"].find_one({"_id": quiz_id})

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    if quiz["user_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    await db["quizzes"].delete_one({"_id": quiz_id})
    return {"message": "Quiz deleted successfully"}

async def publish_quiz(quiz_id: str, current_user: dict):
    db   = get_db()
    quiz = await db["quizzes"].find_one({"_id": quiz_id})

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    if quiz["user_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    await db["quizzes"].update_one(
        {"_id": quiz_id},
        {"$set": {"status": "published", "updated_at": datetime.utcnow()}}
    )
    updated = await db["quizzes"].find_one({"_id": quiz_id})
    updated["id"] = updated["_id"]
    return updated
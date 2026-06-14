from fastapi              import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib           import asynccontextmanager
from app.database         import connect_db, close_db
from app.routes           import auth, quiz
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()

app = FastAPI(
    title       = "Quiz Builder API",
    description = "Backend for Quiz Builder application",
    version     = "1.0.0",
    lifespan    = lifespan
)

# allow both local and production frontend
origins = [
    "http://localhost:5173",          # local dev
    "http://localhost:3000",          # local dev alt
    os.getenv("FRONTEND_URL", "*"),   # production frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins     = origins,
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

app.include_router(auth.router)
app.include_router(quiz.router)

@app.get("/")
async def root():
    return {"message": "Quiz Builder API is running"}
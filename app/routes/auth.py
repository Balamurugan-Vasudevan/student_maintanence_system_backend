from fastapi            import APIRouter, Depends
from app.schemas.user   import RegisterSchema, LoginSchema
from app.controllers.auth import register_user, login_user, get_me
from app.middleware.auth  import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register")
async def register(data: RegisterSchema):
    return await register_user(data)

@router.post("/login")
async def login(data: LoginSchema):
    return await login_user(data)

@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return await get_me(current_user)
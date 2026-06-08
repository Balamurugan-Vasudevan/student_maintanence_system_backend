from pydantic import BaseModel, EmailStr
from typing   import Optional

class RegisterSchema(BaseModel):
    name:     str
    email:    EmailStr
    password: str

class LoginSchema(BaseModel):
    email:    EmailStr
    password: str

class UserResponse(BaseModel):
    id:    str
    name:  str
    email: str
    token: str

class UserOut(BaseModel):
    id:    str
    name:  str
    email: str
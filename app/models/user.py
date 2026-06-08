from pydantic import BaseModel, EmailStr, Field
from bson    import ObjectId
from typing  import Optional
from datetime import datetime

class UserModel(BaseModel):
    id:         Optional[str]      = Field(default=None, alias="_id")
    name:       str
    email:      EmailStr
    password:   str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
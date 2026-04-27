from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str
    role: str = "operator"

class UserRead(BaseModel):

    model_config = ConfigDict(from_attributes=True)  

    id: int
    email: str
    role: str
    created_at: datetime


class Token(BaseModel):
    access_token:str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email:str | None = None
    role:str | None = None
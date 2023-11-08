from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


class NoteCreate(BaseModel):
    title: str
    description: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: Optional[datetime]


class NoteOut(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    user: UserOut


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Like(BaseModel):
    note_id: int
    is_like: conint(ge=0, le=1)


class NoteOutWithLikes(BaseModel):
    note: NoteOut
    no_of_like: int

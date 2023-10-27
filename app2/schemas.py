from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


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

    # class Config:
    #     orm_mode = True


class NoteOut(BaseModel):
    id: int
    title: str
    description: str
    user_id: int
    user: UserOut  # (exclude=['user.created_at'])  # so  while getting a note user could see its user related info


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None

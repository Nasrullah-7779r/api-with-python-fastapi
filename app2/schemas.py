from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class NoteCreate(BaseModel):
    title: str
    description: str


class NoteOut(BaseModel):
    id: int
    title: str
    description: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    # class Config:
    #     orm_mode = True


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    # class Config:
    #     orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


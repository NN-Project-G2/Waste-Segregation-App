from typing import List, Union

from pydantic import BaseModel
import datetime


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    secret_question_answer: str
    created_on: datetime.datetime

    class Config:
        orm_mode = True

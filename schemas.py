from typing import List, Union

from pydantic import BaseModel
import datetime


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    secret_question_answer: str


class User(UserBase):
    id: int
    created_on: datetime.datetime

    class Config:
        orm_mode = True


class UserPredictionBase(BaseModel):
    user_id: str


class UserPredictionCreate(UserPredictionBase):
    image_s3_path: str
    predicted_label: str
    actual_label: str


class UserPrediction(UserPredictionBase):
    id: int
    created_on: datetime.datetime

    class Config:
        orm_mode = True

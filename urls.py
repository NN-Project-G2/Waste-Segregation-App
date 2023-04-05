import json
import traceback

from typing import List

from fastapi import APIRouter, Request
from sqlalchemy.orm import Session

from . import schemas
from .views import *


router = APIRouter(
    prefix="/api",
    tags=["wasteClassifier"],
    responses={404: {"description": "Not found"}},
)


@router.get("/test")
def test_route():
    return test_view()


@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate):
    return register(user)


@router.post("/login")
def login_user(email: str, password: str):
    return login(email, password)


@router.post("/reset")
def reset_user_password():
    return test_view()


@router.post("/classify")
async def classify_image_route(file: bytes = File()):
    return await classify_view(file)


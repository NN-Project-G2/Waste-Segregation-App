import json
import traceback

from views import *

from fastapi import APIRouter, Request


router = APIRouter(
    prefix="/api",
    tags=["wasteTypeIdentifier"],
    responses={404: {"description": "Not found"}},
)


@router.get("/test")
def test_route():
    return test_view()


@router.get("/register")
def register_user():
    return test_view()


@router.get("/login")
def login_user():
    return test_view()


@router.get("/reset")
def reset_user_password():
    return test_view()


@router.post("/classify")
async def classify_image_route(file: bytes = File()):
    return await classify_view(file)


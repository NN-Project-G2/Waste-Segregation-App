import json
import traceback

from typing import List

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import schemas
from views import *
from database_manager import get_db


templates = Jinja2Templates(directory="webapp")


router = APIRouter(
    tags=["wasteClassifier"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def home(request: Request):
	return templates.TemplateResponse("index.html", {"request":request})


@router.get("/login-register")
async def home(request: Request):
	return templates.TemplateResponse("login-register.html", {"request":request})


@router.get("/app")
async def home(request: Request):
	return templates.TemplateResponse("app.html", {"request":request})


@router.get("/test")
def test_route():
    return test_view()


@router.post("/api/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return register(user, db)


@router.post("/api/login")
async def login_user(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    email = data['email']
    password = data['password']
    return login(email, password, db)


@router.post("/api/reset")
async def reset_user_password(request: Request,  db: Session = Depends(get_db)):
    data = await request.json()

    email = data['email']
    secret_qtn = data['secretQtn']
    secret_ans = data['secretAns']
    secret_qtn_ans = f"{secret_qtn};{secret_ans}"

    new_password = data['newPassword']

    return reset_user_credentials(email, secret_qtn_ans, new_password, db)


@router.post("/api/classify")
async def classify_image_route(file: bytes = File()):
    return await classify_view(file)


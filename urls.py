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
from aws_manager import *


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


@router.get("/test-s3-download")
def test_s3_download():
    download_file("/test/51825003.jpg", "51825003.jpg")
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
async def classify_image_route(request: Request, file: bytes = File()):
    access_token = request.headers.get("Authorization", None)

    if access_token is None:
        raise HTTPException(status_code=422, detail="Authorization key missing")

    status, user_data = user_manager.verify_token(access_token)
    if not status:
        raise HTTPException(status_code=401, detail="Unauthorised")

    return await classify_view(user_data['userId'], file)


@router.post("/api/update-label")
async def update_image_label_route(request: Request):
    access_token = request.headers.get("Authorization", None)

    if access_token is None:
        raise HTTPException(status_code=422, detail="Authorization key missing")

    status, _ = user_manager.verify_token(access_token)
    if not status:
        raise HTTPException(status_code=401, detail="Unauthorised")

    data = await request.json()

    pred_id = data['predictionId']
    new_label = data['expectedLabel']

    return await update_prediction_label(pred_id, new_label)


@router.get("/api/verify-session")
async def verify_session(request: Request):
    try:
        access_token = request.headers.get("Authorization", None)

        if access_token is None:
            raise HTTPException(status_code=422, detail="Authorization key missing")

        status, _ = user_manager.verify_token(access_token)

        return {"tokenValid": status}
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong.")


@router.get("/api/refresh-session")
async def refresh_session(request: Request):
    try:
        refresh_token = request.headers.get("Authorization", None)

        if refresh_token is None:
            raise HTTPException(status_code=422, detail="Authorization key missing")

        status, tokens = user_manager.verify_refresh_token(refresh_token)

        resp = {"tokenValid": status}

        if status:
            resp['accessToken'] = tokens['accessToken']
            resp['refreshToken'] = tokens['refreshToken']

        return resp 
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong.")

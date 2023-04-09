import traceback
import json
import io
import numpy as np

from fastapi import HTTPException, Request, File, Depends
from typing import List
from sqlalchemy.orm import Session

import asyncio

from database_manager import SessionLocal, engine, get_db
import user_manager
import schemas


def test_view():
    try:
        return {"Analysis": "test"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong.")


def register(user: schemas.UserCreate, db: Session):
    try:
        db_user = user_manager.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        return user_manager.create_user(db=db, user=user)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong.")


def login(user_email: str, user_password: str, db: Session):
    try:
        db_user = user_manager.get_user_by_email_password(db, email=user_email, password=user_password)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"userAuthorized": True}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong.")


def reset_user_credentials(user_email: str, secret_qtn_ans: str, new_password: str, db: Session):
    try:
        db_user = user_manager.get_user_by_email_secret_qtn_ans(
            db,
            email=user_email,
            secret_qtn_ans=secret_qtn_ans
        )
        if db_user is None:
            raise HTTPException(status_code=400, detail="Details invalid")

        update_status = user_manager.update_password(db, user_email, new_password)
        
        return {"passwordUpdated": update_status}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong.")


async def classify_view(file: bytes = File()):
    try:
        img = cv2.imdecode(np.frombuffer(file, np.uint8), -1)

        pred_status, pred_class = predict_class(img)

        if not pred_status:
            raise HTTPException(status_code=500, detail="Something went wrong.")

        return {"predictedClass": pred_class}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong.")


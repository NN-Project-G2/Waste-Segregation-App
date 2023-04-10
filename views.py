import traceback
import json
import io
import numpy as np
import cv2

from fastapi import HTTPException, Request, File, Depends
from typing import List
from sqlalchemy.orm import Session

import asyncio

from database_manager import SessionLocal, engine, get_db
import user_manager
import schemas
import models

from aimodel.densenet_waste_classifier import predict_class


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

        access_token = user_manager.generate_token(user_email, db_user.id)
        refresh_token = user_manager.generate_token(user_email, db_user.id, 'refresh')
        
        return {"userAuthorized": True, "accessToken": access_token, "refreshToken": refresh_token}
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


async def classify_view(user_id, file: bytes = File()):
    try:
        img = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)

        print(img.shape)

        pred_status, pred_class, pred_id = predict_class(img, user_id)

        if not pred_status:
            raise HTTPException(status_code=500, detail="Something went wrong.")

        return {"predictedClass": pred_class, "predictionId": pred_id}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong.")


async def update_prediction_label(pred_id: int, actual_label: str, db: Session = SessionLocal()):
    try:
        pred = db.query(models.UserPrediction).filter(models.UserPrediction.id==pred_id).first()

        if pred is None:
            raise HTTPException(status_code=404, detail="Prediction does not exist")

        db.query(models.UserPrediction).filter(models.UserPrediction.id == pred_id).update(
            {
                'actual_label': actual_label
            }
        )
        db.commit()

        return {"status": True}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong.")

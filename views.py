import traceback
import json
import io
import numpy as np

from fastapi import HTTPException, Request, File
import asyncio

from models import User
from model.densenet_waste_classifier import predict_class


def test_view():
    try:
        return {"Analysis": "test"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong.")


def login(email: str, password: str):
    try:

        return {"Analysis": "test"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong.")


def register(email: str, password: str, secret_question: str, secret_answer: str):
    try:
        
        return {"Analysis": "test"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong.")


def reset_user_credentials(email: str, secret_question: str, secret_answer: str):
    try:
        
        return {"Analysis": "test"}
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

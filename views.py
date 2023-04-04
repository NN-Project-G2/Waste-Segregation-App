import traceback
import json

from fastapi import HTTPException, Request, File

import asyncio

from models import User


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
        with open('test.jpg', 'wb+') as f:
            f.write(file)

        pred = "Waste Type"

        return {"predictedLabel": pred}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Something went wrong.")

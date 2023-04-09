import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from urls import router

import models
from database_manager import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

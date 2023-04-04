import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from urls import router

app = FastAPI()

app.include_router(router)

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

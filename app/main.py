
from fastapi import Body, Depends, FastAPI
from .routers import posts,users,auth,vote

from . import models
from .database import engine,get_db
from functools import lru_cache

from fastapi import Depends, FastAPI
from . import config
from fastapi.middleware.cors import CORSMiddleware

from typing_extensions import Annotated


models.Base.metadata.create_all(bind=engine)

app =FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)








        
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}







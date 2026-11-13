from fastapi import FastAPI
from core.database.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    users,
    posts,
    chats
)
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(chats.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "page": "home page"
    }
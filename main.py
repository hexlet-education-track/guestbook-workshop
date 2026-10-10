from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI
from pydantic import BaseModel

from config import settings


def connect():
    return psycopg.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password.get_secret_value(),
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    with connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS messages ("
            "id SERIAL PRIMARY KEY, author TEXT, text TEXT)"
        )
    yield


app = FastAPI(lifespan=lifespan)


class Message(BaseModel):
    author: str
    text: str


@app.get("/")
def index():
    return {"message": settings.greeting}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/messages")
def list_messages():
    with connect() as conn:
        rows = conn.execute(
            "SELECT author, text FROM messages ORDER BY id DESC"
        ).fetchall()
    return [{"author": author, "text": text} for author, text in rows]


@app.post("/messages")
def add_message(message: Message):
    with connect() as conn:
        conn.execute(
            "INSERT INTO messages (author, text) VALUES (%s, %s)",
            (message.author, message.text),
        )
    return {"ok": True}

from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI
from psycopg.rows import dict_row
from pydantic import BaseModel, Field

from config import settings

INIT_SQL = """
CREATE TABLE IF NOT EXISTS messages (
    id         SERIAL PRIMARY KEY,
    author     TEXT NOT NULL,
    text       TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
)
"""


class MessageIn(BaseModel):
    author: str = Field(min_length=1, max_length=100)
    text: str = Field(min_length=1, max_length=1000)


@asynccontextmanager
async def lifespan(app: FastAPI):
    with psycopg.connect(settings.database_url) as conn:
        conn.execute(INIT_SQL)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": settings.greeting}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/messages")
def list_messages():
    with psycopg.connect(settings.database_url, row_factory=dict_row) as conn:
        return conn.execute(
            "SELECT id, author, text, created_at FROM messages ORDER BY id DESC"
        ).fetchall()


@app.post("/messages", status_code=201)
def add_message(message: MessageIn):
    with psycopg.connect(settings.database_url, row_factory=dict_row) as conn:
        return conn.execute(
            "INSERT INTO messages (author, text) VALUES (%s, %s) "
            "RETURNING id, author, text, created_at",
            (message.author, message.text),
        ).fetchone()
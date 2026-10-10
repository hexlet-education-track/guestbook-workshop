# Guestbook

FastAPI and PostgreSQL. Python 3.13.15; dependencies locked with uv.

## Run with Docker

Copy `.env.example` to `.env` and set a random `POSTGRES_PASSWORD`.
`.env` is excluded from Git and the Docker build context.

```powershell
Copy-Item .env.example .env
# Set POSTGRES_PASSWORD in .env
 docker compose up --build -d --wait
```

API: http://localhost:8000; docs: http://localhost:8000/docs.
Only the app port is published. PostgreSQL uses a named volume.
`docker compose down` preserves data; `docker compose down -v` deletes it.

## Local development

```powershell
uv sync --locked
uv run uvicorn main:app --reload
```

Provide a local PostgreSQL instance configured through `.env`.

## API

- `GET /`: greeting
- `GET /health`: service health
- `GET /messages`: messages, newest first
- `POST /messages`: add `{"author": "...", "text": "..."}`

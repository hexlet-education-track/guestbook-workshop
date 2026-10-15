# 📒 guestbook

Гостевая книга на FastAPI + PostgreSQL: можно оставить сообщение и посмотреть все оставленные.
Сервис упакован в Docker, проверяется CI на каждый push, а релизы выходят по git-тегам.

Документы: [RUNBOOK.md](RUNBOOK.md) — что делать, если упало · [CHANGELOG.md](CHANGELOG.md) — что изменилось по версиям.

## Что нужно поставить

- [Docker](https://docs.docker.com/get-docker/) с Compose — чтобы запустить сервис
- [uv](https://docs.astral.sh/uv/) — только для разработки без Docker (тесты, линтер)

## Эндпоинты

| Метод и путь | Что делает |
|---|---|
| `GET /` | приветствие |
| `GET /health` | «жив ли сервис» (базу не трогает) |
| `GET /messages` | все сообщения, новые сверху |
| `POST /messages` | добавить: `{"author": "...", "text": "..."}` |

Интерактивная документация: <http://localhost:8000/docs>.

## Настройки

Все настройки собраны в `config.py` (pydantic-settings). Значения берутся из переменных окружения,
а локально — из файла `.env`. Секреты в репозиторий не попадают: `.env` лежит в `.gitignore`,
шаблон — [`.env.example`](.env.example).

```bash
cp .env.example .env       # затем впишите свой POSTGRES_PASSWORD
```

## Запуск для разработки

```bash
docker compose up --build  # приложение + PostgreSQL, образ собирается из Dockerfile
```

Сервис: <http://localhost:8000>. Наружу проброшен только `app`, данные базы лежат в volume `pgdata`
(переживают `docker compose down`; `down -v` их стирает).

Без Docker (нужна своя база и `DATABASE_URL` в `.env`):

```bash
uv sync
uv run uvicorn main:app
uv run ruff check . && uv run pytest
```

## CI/CD

Файл [`.github/workflows/ci.yml`](.github/workflows/ci.yml):

| Задача | Когда запускается | Что делает |
|---|---|---|
| `check` | каждый push и pull request | Ruff + pytest |
| `publish` | push в `main`, только после зелёного `check` | публикует образ `ghcr.io/<владелец>/<репозиторий>:latest` |
| `release` | push git-тега `vX.Y.Z`, только после зелёного `check` | публикует образ с версией `:vX.Y.Z` |

Красный билд не мержим. В реестр образ попадает только через зелёный CI.

## Как выпустить релиз

Версии по [semver](https://semver.org/lang/ru/): `MAJOR` — ломающие изменения, `MINOR` — новое без поломки старого, `PATCH` — багфикс.

```bash
# 1. В CHANGELOG.md перенесите [Unreleased] в раздел новой версии с датой
# 2. Влейте изменения в main и дождитесь зелёного CI (появится :latest)
git tag -a v1.1.0 -m "Релиз 1.1.0"
git push origin v1.1.0     # обычный git push теги не отправляет
```

После этого в Packages репозитория появится образ `:v1.1.0`.

## Выкат и откат

В проде сервис запускается не из исходников, а из образа **по конкретной версии**
([`compose.prod.yaml`](compose.prod.yaml)). Версия задаётся в `.env`:

```env
GHCR_IMAGE="ghcr.io/ваш-логин/guestbook-workshop"   # только строчные буквы
APP_VERSION="v1.1.0"
```

Если пакет приватный, один раз выполните `docker login ghcr.io` (логин GitHub и токен с правом `read:packages`)
либо сделайте пакет публичным в его настройках.

```bash
# выкат версии из APP_VERSION
docker compose -f compose.prod.yaml up -d

# откат: верните предыдущую версию в .env (APP_VERSION="v1.0.0") и повторите
docker compose -f compose.prod.yaml up -d
```

**Почему откат безопасен.** Код откатывается за секунды, а база — нет: данные уже изменились.
Поэтому изменения схемы делаются только обратно совместимыми: колонку **добавляют** (необязательную),
но не переименовывают и не удаляют. Тогда прежняя версия кода продолжает работать с новой схемой.
Ломающее изменение разбивают на шаги expand → перевод кода → contract.

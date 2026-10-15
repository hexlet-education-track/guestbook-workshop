# Changelog

Все заметные изменения проекта документируются в этом файле.
Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/),
проект следует [семантическому версионированию](https://semver.org/lang/ru/).

## [Unreleased]

## [1.0.0] - 2026-10-15

### Added
- Гостевая книга: `GET /`, `GET /health`, `GET /messages`, `POST /messages`
- Хранение сообщений в PostgreSQL, таблица `messages` создаётся при старте
- Зависимости на uv (`pyproject.toml`, `uv.lock`), Python 3.12 закреплён
- `Dockerfile` и `compose.yaml` (приложение + PostgreSQL, healthcheck, volume)
- Конфигурация через pydantic-settings, секреты в `.env` вне git
- CI: Ruff и pytest на каждый push и pull request
- CD: публикация образа в ghcr.io (`:latest` из `main`, `:vX.Y.Z` по git-тегу)
- `compose.prod.yaml` для запуска из реестра по конкретной версии
- `README.md` и `RUNBOOK.md`
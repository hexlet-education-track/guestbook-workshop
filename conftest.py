import os

# Тесты не ходят в реальную базу: подставляем заглушки до импорта приложения.
os.environ.setdefault("GREETING", "test")
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test")
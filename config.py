from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "guestbook"
    postgres_user: str = "guestbook"
    postgres_password: SecretStr
    greeting: str = "Добро пожаловать в гостевую книгу!"


settings = Settings()

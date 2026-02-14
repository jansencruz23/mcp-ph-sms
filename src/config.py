import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    SMS_API_BASE_URL: str = "https://sms-api-ph-gceo.onrender.com"
    SMS_API_KEY: str
    DB_PATH: str = "sqlite:///data/app.db"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()

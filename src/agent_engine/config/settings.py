from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "AI_AGENT_ENGINE"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: Literal["development", "production", "testing"] = "development"
    DEBUG_MODE: bool = True

    # message conig
    MESSAGE_MIN_LENGTH: int = 1
    MESSAGE_MAX_LENGTH: int = 10000

    # LLM Settings
    OLLAMA_BASE_URL: str = "http://ollama:11434/api/chat"
    DEFAULT_MODEL: str = "gemma:2b"
    MAX_TOKENS_BUDGET: int = 4000
    TEMPERATURE: float = 0.7

    # Flask Settings
    FLASK_SECRET_KEY: str = "super-secret-key-change-in-production"

    # Logging Settings
    LOG_LEVEL: str = "INFO"

    # Database Settings
    DATABASE_URL: str = "sqlite:///data/agent_engine.db"

    # .env file settings
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

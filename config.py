# config.py — all settings loaded from .env
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # JWT
    SECRET_KEY:                  str
    ALGORITHM:                   str   = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int   = 30

    # Gemini
    GEMINI_API_KEY:              str
    GROQ_API_KEY:                str   = ""  
    # Database
    DATABASE_URL:                str   = "sqlite:///./documind.db"

    # Storage
    UPLOAD_DIR:                  str   = "uploads"
    CHROMA_DIR:                  str   = "chroma_db"

    # Limits
    MAX_FILE_SIZE_MB:            int   = 10

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Freight Intelligence & Vessel Optimization System"
    API_V1_STR: str = "/api/v1"

    
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/freight_db"
    )

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()
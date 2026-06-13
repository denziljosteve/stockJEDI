from typing import List, Union, Optional
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "stockJEDI"
    API_V1_STR: str = "/api/v1"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of strings.
    # For development, defaults to localhost origins on common frontend ports.
    # For production, set BACKEND_CORS_ORIGINS in your .env file, e.g.:
    #   BACKEND_CORS_ORIGINS=["https://stockjedi.example.com","https://www.stockjedi.example.com"]
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "stockjedi"
    SQLALCHEMY_DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

    GROQ_API_KEY: str = ""
    DATABASE_URL: Optional[str] = None

    JWT_SECRET: str = ""

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"


settings = Settings()

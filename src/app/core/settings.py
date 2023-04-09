from typing import Any, Dict, List, Optional, Union
from os import path
from jose import constants

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    LOGGING_LEVEL: str
    DOCKER_MODE: bool = False
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=str(values.get("POSTGRES_SERVER"))
            if values.get("POSTGRES_SERVER")
            else "127.0.0.1",
            port="46876",
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    @validator("ALGORITHM")
    def check_algorithm(cls, v: str) -> str:
        if not v in constants.ALGORITHMS.HASHES.keys():
            help_message = [f"\n-{i}" for i in constants.ALGORITHMS.HASHES.keys()]
            raise ValueError(f"Unsoported algorithm use one from below: {help_message}")
        return v

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    STATIC_FILE_URL: str = "static/{username}_{filename}"
    PIPELINE_PATH: str = r"app/pipeline/pipe.zip"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()  # type: ignore

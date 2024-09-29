import logging
import pathlib
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()


class BackendBaseSettings(BaseSettings):
    TITLE: str = "Pypost Application"
    VERSION: str = "0.1.0"
    TIMEZONE: str = "UTC"
    DESCRIPTION: Optional[str] = None
    DEBUG: bool = False

    SERVER_HOST: str
    SERVER_PORT: int
    SERVER_WORKERS: int

    DB_POSTGRES_HOST: str
    DB_MAX_POOL_CON: int
    DB_POSTGRES_NAME: str
    DB_POSTGRES_PASSWORD: str
    DB_POOL_SIZE: int
    DB_POOL_OVERFLOW: int
    DB_POSTGRES_PORT: int
    DB_POSTGRES_SCHEMA: str
    DB_TIMEOUT: int
    DB_POSTGRES_USERNAME: str

    IS_DB_ECHO_LOG: bool
    IS_DB_FORCE_ROLLBACK: bool
    IS_DB_EXPIRE_ON_COMMIT: bool

    LOGGING_LEVEL: int = logging.INFO

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=f"{str(ROOT_DIR)}/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @computed_field
    @property
    def DB_POSTGRES_URI(self) -> str:
        return (
            f"{self.DB_POSTGRES_SCHEMA}://{self.DB_POSTGRES_USERNAME}:{self.DB_POSTGRES_PASSWORD}"
            f"@{self.DB_POSTGRES_HOST}:{self.DB_POSTGRES_PORT}/{self.DB_POSTGRES_NAME}"
        )

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all `FastAPI` class' attributes with the custom values defined in `BackendBaseSettings`.
        """
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
        }

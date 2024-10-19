from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar
from pathlib import Path

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    env_file: ClassVar[Path] = Path(__file__).parent.parent / '.env'
    model_config = SettingsConfigDict(env_file=env_file)

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
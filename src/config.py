from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar
from pathlib import Path

class Settings(BaseSettings):
    DB_NAME: str
    env_file: ClassVar[Path] = Path(__file__).parent.parent / '.env'
    model_config = SettingsConfigDict(env_file=env_file)

settings = Settings()
from typing import List, Union
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    openai_api_key_file: str
    allowed_origins: List[str] = ["*"]


settings = Settings()


def get_openai_api_key():
    with open(settings.openai_api_key_file, 'r') as f:
        return f.read().strip()

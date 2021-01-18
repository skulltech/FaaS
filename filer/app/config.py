from pydantic import BaseSettings


class Settings(BaseSettings):
    storage_directory: str
    base_url: str

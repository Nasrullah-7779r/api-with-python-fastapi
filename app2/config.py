import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_password: str
    database_username: str
    secret_key: str
    algorithm: str

    access_token_expire_minutes: int = 0

    class Config:
        env_file = ".env"


setting = Settings()

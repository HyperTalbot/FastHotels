from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Setting(BaseSettings):
    api_prefix: str = "/api"

    pg_psycopg: str = "postgresql+asyncpg"
    username: str = "hotel_user"
    password: str = "securepassword"
    port: str = "localhost"
    db_name: str = "hotel_booking"

    db_url: str = f"{pg_psycopg}://{username}:{password}@{port}/{db_name}"
    db_echo: bool = False
    # db_echo: bool = True


settings = Setting()

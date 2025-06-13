from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Setting(BaseSettings):
    api_v1_prefix: str = "/api"

    db_url: str = f"sqlite+aiosqlite:///db/fasthotels.db"
    db_echo: bool = False
    # db_echo: bool = True


settings = Setting()

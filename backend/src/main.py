import os
import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.config import settings
from core.models import Base, db_helper
from api import router as router_v1


# асинхронное создание БД
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_prefix)


# решение проблемы с CORS (чтобы бэк передавал данные на фронт)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # или [http://localhost:3000]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# указываем где находятся картинки отелей и комнат
# абсолютный путь до папки static (на уровень выше текущего файла)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


# для запуска проекта по команде: python3 main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

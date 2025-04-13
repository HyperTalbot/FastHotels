from click import echo
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Response

from authx import AuthX, AuthXConfig
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# from db.db import HOTELS

# если использовать тесты, писать так:
# from backend.src.db.db import HOTELS


# создание базового шаблонного приложения FastAPI
app = FastAPI()

# создание движка для БД
engine = create_async_engine(
    "sqlite+aiosqlite:///db/hotels.db",
    echo=True)

# создаем новую сессию для ORM (sqlalchemy)
new_session = async_sessionmaker(engine, expire_on_commit=False)

# конфигурация для JWT токена
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

# получение сессии
async def get_session():
    async with new_session() as session:
        yield session

# и запихиваем полученную сессию в класс, для последующего обращения
SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass

# создание полей в БД
class HotelModel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    owner: Mapped[str]
    description: Mapped[str]

    # запрет на доп поля
    model_config = ConfigDict(extra="forbid")


class OwnerModel(Base):
    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    number: Mapped[str]
    password: Mapped[str]

    # запрет на доп поля
    model_config = ConfigDict(extra="forbid")


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    number: Mapped[str]
    password: Mapped[str]

    # запрет на доп поля
    model_config = ConfigDict(extra="forbid")


# создание БД
@app.post("/setup_db",
          tags=["Отели"],
          summary="Добавить БД")
async def setup_db():
    async with engine.begin() as conn:
        # сначала удаляем все БД
        await conn.run_sync(Base.metadata.drop_all)
        # потом создаем новые 
        await conn.run_sync(Base.metadata.create_all)
    return {"status": True}


# то что будет добавляться в post запросе 
class HotelAddSchema(BaseModel):
    title: str
    owner: str
    description: str | None

    # запрет на доп поля
    model_config = ConfigDict(extra="forbid")

# id добавиться авто, к верхнему классу
class IDHotelAddSchema(HotelAddSchema):
    id: int

# добавление отеля
@app.post("/add_hotels",
          tags=["Отели"],
          summary="Добавить отель")
async def add_hotel(data: HotelAddSchema, session: SessionDep):
    new_hotel = HotelModel(
        title=data.title,
        owner=data.owner,
        description=data.description
    )
    session.add(new_hotel)
    await session.commit()
    return {"status_add_hotel": True}


# получить все отели 
@app.get("/get_hotels",
          tags=["Отели"],
          summary="Получить все отели")
async def get_hotel(session: SessionDep):
    query = select(HotelModel)
    result = await session.execute(query)
    return result.scalars().all()

# получить конкретный отель
# @app.get("/hotels/{hotel_id}", 
#          tags=["Отели"],
#          summary="Получить конкретный отель")
# def get_hotel(hotel_id: int):
#     for hotel in HOTELS:
#         if hotel["id"] == hotel_id:
#             return hotel
#     raise HTTPException(status_code=404, detail="отель не найден")


# для получение отелей из словаря в db.py
# @app.get("/hotels_all", 
#          tags=["Отели"],
#          summary="Получить все отели")
# def get_all_hotels():
#     return HOTELS


# базовый класс пользователя 
class UserLoginSchema(BaseModel):
    username: str
    password: str

    # запрет на доп поля
    model_config = ConfigDict(extra="forbid")


# авторизация с токеном
@app.post("/login",
          tags=["Авторизация"],
          summary="получить JWT токен")
def login(credentials: UserLoginSchema, response: Response):
    if credentials.username == "test" and credentials.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")


# безопасное подключение для авторизации
@app.get("/protected",
         tags=["Авторизация"],
         summary="безопасное подключение для авторизации",
         dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "TOP SECRET"}


# изменить существующий отель
@app.put("/put_hotels/{hotel_id}",
          tags=["Отели"],
          summary="Изменить отель")
async def put_hotel(hotel_id: int, session: SessionDep):
    query = session.get(HotelAddSchema, id)
    result = await session.execute(query)
    await session.commit()
    return result.scalars().all(), {"status_put_hotel": True}
    

# то что будет добавляться в put запросе 
class HotelDeleteSchema(BaseModel):
    id: int
    title: str
    owner: str
    description: str | None

    # запрет на доп поля
    model_config = ConfigDict(extra="forbid")

# id добавиться автоматом, к верхнему классу
# class IDHotelDeleteSchema(HotelDeleteSchema):
#     id: int

# удалить существующий отель
# @app.delete("/delete_hotels",
#           tags=["Отели"],
#           summary="Удалить отель")
# async def delete_hotel(data: HotelDeleteSchema, session: SessionDep):
#     delete_hotel = HotelModel(
#         id=data.id,
#         title=data.title,
#         owner=data.owner,
#         description=data.description
#     )
#     session.delete(delete_hotel)
#     await session.commit()
#     return {"status_delete_hotel": True}

@app.delete("/delete_hotels/{hotel_id}",
          tags=["Отели"],
          summary="Удалить отель")
async def delete_hotel(hotel_id: int, session: SessionDep):
    delete_hotel = session.get(HotelAddSchema, hotel_id)
    if not delete_hotel:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(delete_hotel)
    session.commit()
    return {"status": True}


@app.post("/post_owners",
          tags=["Владельцы"],
          summary="Добавить владельца")
async def post_owners():
    ...


@app.get("/get_owners",
          tags=["Владельцы"],
          summary="Получить владельца")
async def get_owners():
    ...


@app.put("/put_owners",
          tags=["Владельцы"],
          summary="Изменить владельца")
async def put_owners():
    ...


@app.delete("/delete_owners",
          tags=["Владельцы"],
          summary="Удалить владельца")
async def delete_owners():
    ...


@app.post("/post_users",
          tags=["Пользователи"],
          summary="Добавить пользователя")
async def post_user():
    ...


@app.get("/get_users",
          tags=["Пользователи"],
          summary="Получить пользователя")
async def get_user():
    ...


@app.put("/put_user",
          tags=["Пользователи"],
          summary="Изменить пользователя")
async def put_user():
    ...


@app.delete("/delete_user",
          tags=["Пользователи"],
          summary="Удалить пользователя")
async def delete_user():
    ...


# для запуска по команде: python3 main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
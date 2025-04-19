import uvicorn

from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends, Response

from authx import AuthX, AuthXConfig

from sqlalchemy import func, select, insert, update, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from db.db import Base, HotelModel, OwnerModel, UserModel
# если использовать тесты, писать так:
# from backend.src.db.db import HOTELS

from schemas.hotels_schemas import *


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
@app.get("/hotels/{hotel_id}", 
         tags=["Отели"],
         summary="Получить конкретный отель")
def get_hotel(hotel_id: int, session: SessionDep):
    hotel = ...
    if hotel is not None:
        return hotel
    raise HTTPException(status_code=404, detail="отель: {hotel_id} не найден")


# для получение отелей из словаря в db.py
# @app.get("/hotels_all", 
#          tags=["Отели"],
#          summary="Получить все отели")
# def get_all_hotels():
#     return HOTELS


# авторизация с токеном
@app.post("/login",
          tags=["Авторизация"],
          summary="получить JWT токен")
def login(credentials: UserLogin, response: Response):
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


# изменить существующий отель, put заменит все свойства
@app.put("/put_hotels/{hotel_id}",
          tags=["Отели"],
          summary="Изменить отель")
async def put_hotel(hotel_id: int, session: SessionDep):
    query = session.get(HotelAddSchema, id)
    result = await session.execute(query)
    await session.commit()
    return result.scalars().all(), {"status_put_hotel": True}


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
from pydantic import ConfigDict
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from typing import Annotated


# настройка аннотаций
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]


class Base(DeclarativeBase):
    pass

# создание полей в БД отелей
class HotelModel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    owner: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    # запрет на доп поля
    model_config = ConfigDict(extra="forbid")


# БД владельцев
class OwnerModel(Base):
    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    number: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    # запрет на доп поля
    model_config = ConfigDict(extra="forbid")


# БД пользователей
class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    number: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    # запрет на доп поля
    model_config = ConfigDict(extra="forbid")

# HOTELS = [
#     {
#         "id": 1,
#         "title": "Первый",
#         "owner": "ООО Иванов Иван",
#         "description": "простое и краткое описание отеля 1"
#     },
#     {
#         "id": 2,
#         "title": "Второй",
#         "owner": "ООО Петров Петр",
#         "description": "простое и краткое описание отеля 2"
#     }
# ]

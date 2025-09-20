from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List
import json


class RoomBase(BaseModel):
    photos: Optional[List[str]] = []
    title: str
    price_for_night: int
    len_beds: int
    comfort: str


class RoomCreate(RoomBase):
    hotel_id: int


class RoomUpdate(RoomCreate):
    pass


class RoomUpdatePartial(RoomCreate):
    hotel_id: int | None = None
    title: str | None = None
    price_for_night: int | None = None
    len_beds: int | None = None
    comfort: str | None = None
    photos: Optional[List[str]] = []


class Room(RoomBase):
    id: int
    hotel_id: int

    # Для Pydantic v2: читаем атрибуты SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

    @field_validator("photos", mode="before")
    def parse_photos(cls, v):
        # None -> []
        if v is None:
            return []
        # Уже список -> оставить
        if isinstance(v, list):
            return v
        # Строка: пробуем JSON.parse, иначе split по запятой
        if isinstance(v, str):
            s = v.strip()
            try:
                parsed = json.loads(s)
                if isinstance(parsed, list):
                    return [str(x) for x in parsed]
                # если JSON вернул не список, положим один элемент
                return [str(parsed)]
            except Exception:
                # fallback: если строка через запятую
                if "," in s:
                    return [p.strip() for p in s.split(",") if p.strip()]
                return [s] if s else []
        # Иначе — вернуть как есть (возможно неверный тип, тогда Pydantic выдаст ошибку)
        return v


# test json room
"""
{
  "hotel_id": 1,
  "photos": ["/static/rooms/room1.jpeg"],
  "title": "Двухместный номер Standard",
  "price_for_night": 12000,
  "len_beds": 2,
  "comfort": "18 кв.м, Телевизор, Ванна, Душ, Отопление."
}


{
  "hotel_id": 1,
  "photos": ["/static/rooms/room2.jpeg", "/static/rooms/room3.jpeg"],
  "title": "номер Standard",
  "price_for_night": 12500,
  "len_beds": 1,
  "comfort": "Телевизор, Ванна, Душ, Отопление."
}
"""
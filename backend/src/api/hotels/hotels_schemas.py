import json
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List


class HotelBase(BaseModel):
    title: str
    owner_id: int
    photos: List[str] # список URL к фото
    stars: int
    description: str
    address: str
    comfort: str
    rating: float 
    min_price_for_night: int


class HotelCreate(HotelBase):
    pass


class HotelUpdate(HotelCreate):
    pass


class HotelUpdatePartial(BaseModel):
    title: Optional[str] = None
    photos: List[str] = None
    stars: Optional[int] = None
    description: Optional[str] = None
    address: Optional[str] = None
    comfort: Optional[str] = None
    rating: Optional[float] = None
    min_price_for_night: Optional[int] = None
    owner_id: Optional[int] = None


class Hotel(HotelBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    @field_validator("photos", mode="before")
    def parse_photos(cls, v):
        "преобразуем JSON-строку в список"
        if isinstance(v, str):
            try:
                return json.loads(v) # например '["/static/hotel/hotel1.jpeg"]' -> ["..."]
            except json.JSONDecodeError:
                return []
        return v



# test json hotel
"""
{
  "title": "Hotel Amsterdam",
  "owner_id": 1,
  "photos": ["/static/hotels/hotel1.jpeg", "/static/hotels/hotel2.jpeg"],
  "stars": 4,
  "description": "Комфортабельный отель в центре Амстердама.",
  "address": "Prinsengracht 123, Amsterdam",
  "comfort": "Wi-Fi, Parking, Breakfast",
  "rating": 9,
  "min_price_for_night": 12000
}

{
  "title": "Hotel 2",
  "owner_id": 1,
  "photos": ["/static/hotels/hotel3.jpeg"],
  "stars": 5,
  "description": "Комфортабельный отель.",
  "address": "Prinsengracht 123, Amsterdam",
  "comfort": "Parking, Breakfast",
  "rating": 8,
  "min_price_for_night": 12500
}
"""
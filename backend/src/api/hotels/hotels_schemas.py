from pydantic import BaseModel, ConfigDict


class HotelBase(BaseModel):
    title: str
    owner_id: int
    photo: bool
    description: str
    address: str
    comfort: str
    rating: int
    min_price_for_night: int

class HotelCreate(HotelBase):
    pass


class HotelUpdate(HotelCreate):
    pass


class HotelUpdatePartial(HotelCreate):
    title: str | None = None
    photo: bool | None = None
    description: str | None = None
    address: int | None = None
    comfort: str | None = None
    rating: int | None = None
    min_price_for_night: int | None = None


class Hotel(HotelBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

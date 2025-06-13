from pydantic import BaseModel, ConfigDict


class HotelBase(BaseModel):
    name: str
    description: str
    price: int


class HotelCreate(HotelBase):
    pass


class HotelUpdate(HotelCreate):
    pass


class HotelUpdatePartial(HotelCreate):
    name: str | None = None
    description: str | None = None
    price: int | None = None


class Hotel(HotelBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

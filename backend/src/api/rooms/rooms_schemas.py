from pydantic import BaseModel, ConfigDict


class RoomBase(BaseModel):
    hotel_id: int
    photo: bool
    title: str
    price_for_night: int
    len_beds: int
    comfort: str


class RoomCreate(RoomBase):
    pass


class RoomUpdate(RoomCreate):
    pass


class RoomUpdatePartial(RoomCreate):
    title: str | None = None
    price_for_night: int | None = None
    len_beds: int | None = None
    comfort: str | None = None
    photo: bool | None = None


class Room(RoomBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

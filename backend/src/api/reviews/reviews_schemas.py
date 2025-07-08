from pydantic import BaseModel, ConfigDict


class ReviewBase(BaseModel):
    user_id: int
    hotel_id: int
    room_id: int
    rating: float
    text: str
    photo: bool


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewCreate):
    pass


class ReviewUpdatePartial(ReviewCreate):
    rating: float | None = None
    text: str | None = None
    photo: bool | None = None


class Review(ReviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

from pydantic import BaseModel, ConfigDict, Field


# второстепенный класс (например IDHotelAddSchema) нужен:
# для того чтобы пользователь не имел доступ для ID

class HotelBase():
    title: str
    owner: str
    description: str

class HotelAddSchema(HotelBase):
    id: int 

# то что будет добавляться в post запросе 
class HotelCreate(BaseModel):
    pass

    # запрет на доп поля
    model_config = ConfigDict(extra="forbid")


# то что будет добавляться в put запросе 
class HotelUpdate(BaseModel):
    pass

    # запрет на доп поля
    model_config = ConfigDict(extra="forbid")

# частичное обновление 
class HotelUpdatePartial(HotelCreate):
    title: str | None = None
    description: str | None = None
    owner: str | None = None


# id добавиться авто, к верхнему классу
class Hotel(HotelBase):
    id: int


# базовый класс пользователя 
class UserLogin(BaseModel):
    username: str
    password: str

    # запрет на доп поля
    model_config = ConfigDict(extra="forbid")

# id добавиться авто, к верхнему классу
class IDUserLogin(UserLogin):
    id: int

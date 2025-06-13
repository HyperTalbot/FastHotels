from sqlalchemy.orm import Mapped

from .base import Base


class Hotel(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

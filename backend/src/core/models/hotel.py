from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Hotel(Base):
    title = Column(String(30))
    owner_id = Column(Integer, ForeignKey("owners.id"))
    photo = Column(Boolean, default=False)
    description = Column(String(800))
    address = Column(String(100))
    comfort = Column(String(50))
    rating = Column(Float(10))
    min_price_for_night = Column(Integer)

    owner = relationship("Owner", back_populates="hotels", foreign_keys=[owner_id])
    rooms = relationship("Room", back_populates="hotel")
    reviews = relationship("Review", 
                           back_populates="hotel", 
                           cascade="all, delete-orphan") # cascade="all, delete-orphan" - при удалении отеля удаляться все его отзывы

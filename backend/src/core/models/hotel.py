from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base


class Hotel(Base):
    title = Column(String(30), nullable=False)
    owner_id = Column(Integer, ForeignKey("owners.id"))
    photos = Column(Text, nullable=True)
    stars = Column(Integer, nullable=True)
    description = Column(String(800), nullable=False)
    address = Column(String(100), nullable=False)
    comfort = Column(String(50), nullable=True)
    rating = Column(Float(10), nullable=False)
    min_price_for_night = Column(Integer, nullable=False)

    owner = relationship("Owner", back_populates="hotels", foreign_keys=[owner_id])
    rooms = relationship("Room", back_populates="hotel")
    reviews = relationship("Review", 
                           back_populates="hotel", 
                           cascade="all, delete-orphan") # cascade="all, delete-orphan" - при удалении отеля удаляться все его отзывы

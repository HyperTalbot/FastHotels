from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Review(Base):
    user_id = Column(Integer, ForeignKey("users.id"))
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    rating = Column(Float(10))
    text = Column(String(800))
    photo = Column(String, default=False)
   
    user = relationship("User", back_populates="reviews", foreign_keys=[user_id])
    hotel = relationship("Hotel", back_populates="reviews", foreign_keys=[hotel_id])
    room = relationship("Room", back_populates="reviews", foreign_keys=[room_id])

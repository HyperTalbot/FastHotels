from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base


class Room(Base):
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    photos = Column(Text)
    title = Column(String(30))
    price_for_night = Column(Integer)
    len_beds = Column(Integer)
    comfort = Column(String(50))
   
    hotel = relationship("Hotel", back_populates="rooms")
    reviews = relationship("Review", back_populates="room")    

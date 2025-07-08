from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from .base import Base


class Owner(Base):
    name= Column(String(30))
    email= Column(String(50))
    phone = Column(String(20))
    is_verified = Column(Boolean, default=False)
    password= Column(String(128))

    hotels = relationship("Hotel", back_populates="owner")

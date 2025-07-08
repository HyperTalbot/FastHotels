from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    name = Column(String(30))
    email = Column(String(50))
    phone = Column(String(20))
    password = Column(String(128))
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
 
    reviews = relationship("Review", back_populates="user", foreign_keys="Review.user_id")

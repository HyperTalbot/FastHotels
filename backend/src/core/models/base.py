from datetime import datetime
from typing import Annotated

from sqlalchemy import Column, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True, index=True)
    create_at: Mapped[created_at]
    update_at: Mapped[updated_at]

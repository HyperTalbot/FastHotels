from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Hotel

from . import hotels_crud


async def hotel_by_id(
    hotel_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Hotel:
    hotel = await hotels_crud.get_hotel(session=session, hotel_id=hotel_id)
    if hotel is not None:
        return hotel

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Hotel {hotel_id} not found!",
    )

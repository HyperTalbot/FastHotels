from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import hotels_crud
from .hotels_dependencies import hotel_by_id
from .hotels_schemas import Hotel, HotelCreate, HotelUpdate, HotelUpdatePartial

router = APIRouter(tags=["Hotels"])


@router.post(
    "/",
    response_model=Hotel,
    status_code=status.HTTP_201_CREATED,
)
async def create_hotel(
    hotel_in: HotelCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await hotels_crud.create_hotel(session=session, hotel_in=hotel_in)


@router.get("/", response_model=list[Hotel])
async def get_hotels(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await hotels_crud.get_hotels(session=session)


@router.get("/{hotel_id}/", response_model=Hotel)
async def get_hotel(
    hotel: Hotel = Depends(hotel_by_id),
):
    return hotel


@router.put("/{hotel_id}/")
async def update_hotel(
    hotel_update: HotelUpdate,
    hotel: Hotel = Depends(hotel_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await hotels_crud.update_hotel(
        session=session,
        hotel=hotel,
        hotel_update=hotel_update,
    )


@router.patch("/{hotel_id}/")
async def update_hotel_partial(
    hotel_update: HotelUpdatePartial,
    hotel: Hotel = Depends(hotel_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await hotels_crud.update_hotel(
        session=session,
        hotel=hotel,
        hotel_update=hotel_update,
        partial=True,
    )


@router.delete("/{hotel_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(
    hotel: Hotel = Depends(hotel_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await hotels_crud.delete_hotel(session=session, hotel=hotel)

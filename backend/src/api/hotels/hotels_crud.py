from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Hotel

from .hotels_schemas import HotelCreate, HotelUpdate, HotelUpdatePartial


async def get_hotels(session: AsyncSession) -> list[Hotel]:
    stmt = select(Hotel).order_by(Hotel.id)
    result: Result = await session.execute(stmt)
    hotels = result.scalars().all()
    return list(hotels)


async def get_hotel(session: AsyncSession, hotel_id: int) -> Hotel | None:
    return await session.get(Hotel, hotel_id)


async def create_hotel(session: AsyncSession, hotel_in: HotelCreate) -> Hotel:
    hotel = Hotel(**hotel_in.model_dump())
    session.add(hotel)
    await session.commit()
    # await session.refresh(hotel)
    return hotel


async def update_hotel(
    session: AsyncSession,
    hotel: Hotel,
    hotel_update: HotelUpdate | HotelUpdatePartial,
    partial: bool = False, # частично
) -> Hotel:
    for name, value in hotel_update.model_dump(exclude_unset=partial).items():
        setattr(hotel, name, value)
    await session.commit()
    return hotel


async def delete_hotel(
    session: AsyncSession,
    hotel: Hotel,
) -> None:
    await session.delete(hotel)
    await session.commit()

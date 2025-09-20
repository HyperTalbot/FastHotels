import json
from typing import Optional, List
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Hotel


def parse_photos(hotel: Hotel) -> Hotel:
    if isinstance(hotel.photos, str):
        try:
            hotel.photos = json.loads(hotel.photos)
        except json.JSONDecodeError:
            hotel.photos = []
    return hotel


async def get_hotels(
    session: AsyncSession,
    check_in: Optional[str] = None,
    check_out: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    stars: Optional[List[int]] = None,
    sort: Optional[str] = "rating"
) -> List[Hotel]:
    stmt = select(Hotel)

    filters = []
    if min_price is not None:
        filters.append(Hotel.min_price_for_night >= min_price)
    if max_price is not None:
        filters.append(Hotel.min_price_for_night <= max_price)
    if stars:
        filters.append(Hotel.stars.in_(stars))

    if filters:
        stmt = stmt.where(and_(*filters))

    if sort == "price":
        stmt = stmt.order_by(Hotel.min_price_for_night)
    else:
        stmt = stmt.order_by(Hotel.rating.desc())

    result = await session.execute(stmt)
    hotels = result.scalars().all()
    await session.close()
    return [parse_photos(h) for h in hotels]


async def create_hotel(session: AsyncSession, hotel_data):
    data = hotel_data.model_dump()
    data["photos"] = json.dumps(data["photos"])
    hotel = Hotel(**data)
    session.add(hotel)
    await session.commit()
    await session.refresh(hotel)
    await session.close()
    return parse_photos(hotel)


async def get_hotel(session: AsyncSession, hotel_id: int) -> Hotel | None:
    return await session.get(Hotel, hotel_id)


async def update_hotel(
    session: AsyncSession,
    hotel: Hotel,
    hotel_update,
    partial: bool = False,
):
    hotel_data = hotel_update.model_dump(exclude_unset=True)

    if "photos" in hotel_data and hotel_data["photos"] is not None:
        hotel_data["photos"] = json.dumps(hotel_data["photos"])

    for key, value in hotel_data.items():
        setattr(hotel, key, value)

    await session.commit()
    await session.refresh(hotel)
    await session.close()
    return parse_photos(hotel)


async def delete_hotel(session: AsyncSession, hotel: Hotel) -> None:
    await session.delete(hotel)
    await session.commit()
    await session.close()


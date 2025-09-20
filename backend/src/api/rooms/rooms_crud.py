from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Room

from .rooms_schemas import RoomCreate, RoomUpdate, RoomUpdatePartial


async def get_rooms(session: AsyncSession) -> list[Room]:
    stmt = select(Room).order_by(Room.id)
    result: Result = await session.execute(stmt)
    room = result.scalars().all()
    await session.close()
    return list(room)


async def get_room(session: AsyncSession, room_id: int) -> Room | None:
    return await session.get(Room, room_id)


async def get_rooms_by_hotel(hotel_id: int, session: AsyncSession):
    result = await session.execute(
        select(Room).where(Room.hotel_id == hotel_id)
    )
    await session.close()
    return result.scalars().all()


async def create_room(session: AsyncSession, room_in: RoomCreate) -> Room:
    room = Room(**room_in.model_dump())
    if isinstance(room.photos, str): 
        import json
        try:
            room.photos = json.loads(room.photos)
        except Exception: 
            room.photos = [room.photos] 
    session.add(room)
    await session.commit()
    await session.refresh(room)
    await session.close()
    return room


async def update_room(
    session: AsyncSession,
    room: Room,
    room_update: RoomUpdate | RoomUpdatePartial,
    partial: bool = False, # частично
) -> Room:
    for name, value in room_update.model_dump(exclude_unset=partial).items():
        setattr(room, name, value)
    await session.commit()
    await session.close()
    return room


async def delete_room(
    session: AsyncSession,
    room: Room,
) -> None:
    await session.delete(room)
    await session.commit()
    await session.close()

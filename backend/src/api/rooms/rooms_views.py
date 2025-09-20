from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import rooms_crud
from .rooms_dependencies import room_by_id
from .rooms_schemas import Room, RoomBase, RoomUpdate, RoomCreate, RoomUpdatePartial

router = APIRouter(tags=["Rooms"])


@router.post(
    "/",
    response_model=Room,
    status_code=status.HTTP_201_CREATED,
)
async def create_room(
    room_in: RoomCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await rooms_crud.create_room(session=session, room_in=room_in)


@router.get("/", response_model=list[Room])
async def get_rooms(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await rooms_crud.get_rooms(session=session)


@router.get("/{room_id}/", response_model=Room)
async def get_room(
    room: Room = Depends(room_by_id),
):
    return room


@router.put("/{room_id}/")
async def update_room(
    room_update: RoomUpdate,
    room: Room = Depends(room_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await rooms_crud.update_room(
        session=session,
        room=room,
        room_update=room_update,
    )


@router.patch("/{room_id}/")
async def update_room_partial(
    room_update: RoomUpdatePartial,
    room: Room = Depends(room_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await rooms_crud.update_room(
        session=session,
        room=room,
        room_update=room_update,
        partial=True,
    )


@router.delete("/{room_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room: Room = Depends(room_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await rooms_crud.delete_room(session=session, room=room)


# @app.post("/post_users",
#           tags=["Пользователи"],
#           summary="Добавить пользователя")
# async def post_user():
#     ...


# @app.get("/get_users",
#           tags=["Пользователи"],
#           summary="Получить пользователя")
# async def get_user():
#     ...


# @app.put("/put_user",
#           tags=["Пользователи"],
#           summary="Изменить пользователя")
# async def put_user():
#     ...


# @app.delete("/delete_user",
#           tags=["Пользователи"],
#           summary="Удалить пользователя")
# async def delete_user():
#     ...

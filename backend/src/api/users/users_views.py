from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import users_crud
from .users_dependencies import user_by_id
from .users_schemas import User, UserBase, UserUpdate, UserCreate, UserUpdatePartial

router = APIRouter(tags=["Users"])


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await users_crud.create_user(session=session, user_in=user_in)


@router.get("/", response_model=list[User])
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await users_crud.get_users(session=session)


@router.get("/{user_id}/", response_model=User)
async def get_user(
    user: User = Depends(user_by_id),
):
    return user


@router.put("/{user_id}/")
async def update_user(
    user_update: UserUpdate,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await users_crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
    )


@router.patch("/{user_id}/")
async def update_user_partial(
    user_update: UserUpdatePartial,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await users_crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
        partial=True,
    )


@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await users_crud.delete_user(session=session, user=user)


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

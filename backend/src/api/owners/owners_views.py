from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import owners_crud
from .owners_dependencies import owner_by_id
from .owners_schemas import Owner, OwnerBase, OwnerCreate, OwnerUpdate, OwnerUpdatePartial

router = APIRouter(tags=["Owners"])


@router.post(
    "/",
    response_model=Owner,
    status_code=status.HTTP_201_CREATED,
)
async def create_owner(
    owner_in: OwnerCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await owners_crud.create_owner(session=session, owner_in=owner_in)


@router.get("/", response_model=list[Owner])
async def get_owners(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await owners_crud.get_owners(session=session)


@router.get("/{owner_id}/", response_model=Owner)
async def get_owner(
    owner: Owner = Depends(owner_by_id),
):
    return owner


@router.put("/{owner_id}/")
async def update_owner(
    owner_update: OwnerUpdate,
    owner: Owner = Depends(owner_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await owners_crud.update_owner(
        session=session,
        owner=owner,
        owner_update=owner_update,
    )


@router.patch("/{owner_id}/")
async def update_owner_partial(
    owner_update: OwnerUpdatePartial,
    owner: Owner = Depends(owner_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await owners_crud.update_owner(
        session=session,
        owner=owner,
        owner_update=owner_update,
        partial=True,
    )


@router.delete("/{owner_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_owner(
    owner: Owner = Depends(owner_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await owners_crud.delete_owner(session=session, owner=owner)


# @app.post("/post_owners",
#           tags=["Владельцы"],
#           summary="Добавить владельца")
# async def post_owners():
#     ...


# @app.get("/get_owners",
#           tags=["Владельцы"],
#           summary="Получить владельца")
# async def get_owners():
#     ...


# @app.put("/put_owners",
#           tags=["Владельцы"],
#           summary="Изменить владельца")
# async def put_owners():
#     ...


# @app.delete("/delete_owners",
#           tags=["Владельцы"],
#           summary="Удалить владельца")
# async def delete_owners():
#     ...
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Owner

from . import owners_crud


async def owner_by_id(
    owner_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Owner:
    owner = await owners_crud.get_owner(session=session, owner_id=owner_id)
    if owner is not None:
        return owner

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Owner {owner_id} not found!",
    )

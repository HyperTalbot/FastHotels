from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Review

from . import reviews_crud


async def review_by_id(
    review_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Review:
    review = await reviews_crud.get_review(session=session, review_id=review_id)
    if review is not None:
        return review

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Review {review_id} not found!",
    )

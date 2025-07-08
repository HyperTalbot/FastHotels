from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Review

from .reviews_schemas import ReviewCreate, ReviewUpdate, ReviewUpdatePartial


async def get_reviews(session: AsyncSession) -> list[Review]:
    stmt = select(Review).order_by(Review.id)
    result: Result = await session.execute(stmt)
    review = result.scalars().all()
    return list(review)


async def get_review(session: AsyncSession, review_id: int) -> Review | None:
    return await session.get(Review, review_id)


async def create_review(session: AsyncSession, review_in: ReviewCreate) -> Review:
    review = Review(**review_in.model_dump())
    session.add(review)
    await session.commit()
    # await session.refresh(review)
    return review


async def update_review(
    session: AsyncSession,
    review: Review,
    review_update: ReviewUpdate | ReviewUpdatePartial,
    partial: bool = False, # частично
) -> Review:
    for name, value in review_update.model_dump(exclude_unset=partial).items():
        setattr(review, name, value)
    await session.commit()
    return review


async def delete_review(
    session: AsyncSession,
    review: Review,
) -> None:
    await session.delete(review)
    await session.commit()

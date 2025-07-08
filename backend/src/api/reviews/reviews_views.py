from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import reviews_crud
from .reviews_dependencies import review_by_id
from .reviews_schemas import Review, ReviewBase, ReviewUpdate, ReviewCreate, ReviewUpdatePartial

router = APIRouter(tags=["Reviews"])


@router.post(
    "/",
    response_model=Review,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    review_in: ReviewCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await reviews_crud.create_review(session=session, review_in=review_in)


@router.get("/", response_model=list[Review])
async def get_reviews(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await reviews_crud.get_reviews(session=session)


@router.get("/{review_id}/", response_model=Review)
async def get_review(
    review: Review = Depends(review_by_id),
):
    return review


@router.put("/{review_id}/")
async def update_review(
    review_update: ReviewUpdate,
    review: Review = Depends(review_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await reviews_crud.update_review(
        session=session,
        review=review,
        review_update=review_update,
    )


@router.patch("/{review_id}/")
async def update_review_partial(
    review_update: ReviewUpdatePartial,
    review: Review = Depends(review_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await reviews_crud.update_review(
        session=session,
        review=review,
        review_update=review_update,
        partial=True,
    )


@router.delete("/{review_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review: Review = Depends(review_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await reviews_crud.delete_review(session=session, review=review)


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

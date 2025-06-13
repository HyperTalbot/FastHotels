# from typing import Annotated

from fastapi import APIRouter, FastAPI, HTTPException, Depends, Path, status

# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession

# from crud import crud_get_hotel, crud_delete_hotel
# from schemas.hotels_schemas import Hotel, HotelAddSchema
# from db.db import HotelModel
# from db import db_helper
# from db.configs import SessionDep


router = APIRouter(tags=["Отели"])


# добавление отеля
@router.post("/add_hotels",
        #   tags=["Отели"],
          summary="Добавить отель")
async def add_hotel():
    ...


# получить все отели 
@router.get("/get_hotels",
        #   tags=["Отели"],
          summary="Получить все отели")
async def get_hotels():
    ...


# получить конкретный отель
@router.get("/hotels/{hotel_id}", 
        #  tags=["Отели"],
         summary="Получить конкретный отель")
def get_hotel():
    ...


# изменить отель, put заменит все свойства
@router.patch("/patch_hotels/{hotel_id}",
        #   tags=["Отели"],
          summary="Изменить отель")
async def patch_hotel():
    ...


# удалить отель
@router.delete("/delete_hotels/{hotel_id}",
            # tags=["Отели"],
            summary="Удалить отель")
async def delete_hotel():
    ...


# # добавление отеля
# @router.post("/add_hotels",
#           tags=["Отели"],
#           summary="Добавить отель")
# async def add_hotel(data: HotelAddSchema, session: SessionDep):
#     new_hotel = HotelModel(
#         title=data.title,
#         owner=data.owner,
#         description=data.description
#     )
#     session.add(new_hotel)
#     await session.commit()
#     return {"status_add_hotel": True}


# # получить все отели 
# @router.get("/get_hotels",
#           tags=["Отели"],
#           summary="Получить все отели")
# async def get_hotel(session: SessionDep):
#     query = select(HotelModel)
#     result = await session.execute(query)
#     return result.scalars().all()


# # получить конкретный отель
# @router.get("/hotels/{hotel_id}", 
#          tags=["Отели"],
#          summary="Получить конкретный отель")
# def get_hotel(hotel_id: int, session: SessionDep):
#     hotel = ...
#     if hotel is not None:
#         return hotel
#     raise HTTPException(status_code=404, detail="отель: {hotel_id} не найден")


# # для получение отелей из словаря в db.py
# # @app.get("/hotels_all", 
# #          tags=["Отели"],
# #          summary="Получить все отели")
# # def get_all_hotels():
# #     return HOTELS

# # изменить отель, put заменит все свойства
# @router.put("/put_hotels/{hotel_id}",
#           tags=["Отели"],
#           summary="Изменить отель")
# async def put_hotel(hotel_id: int, session: SessionDep):
#     query = session.get(HotelAddSchema, id)
#     result = await session.execute(query)
#     await session.commit()
#     return result.scalars().all(), {"status_put_hotel": True}


# # удалить отель
# # @app.delete("/delete_hotels",
# #           tags=["Отели"],
# #           summary="Удалить отель")
# # async def delete_hotel(data: HotelDeleteSchema, session: SessionDep):
# #     delete_hotel = HotelModel(
# #         id=data.id,
# #         title=data.title,
# #         owner=data.owner,
# #         description=data.description
# #     )
# #     session.delete(delete_hotel)
# #     await session.commit()
# #     return {"status_delete_hotel": True}

# @router.delete("/delete_hotels/{hotel_id}",
#             tags=["Отели"],
#             summary="Удалить отель")
# async def delete_hotel(
#     hotel: Hotel = Depends(product_by_id),
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ) -> None:
#     await crud_delete_hotel(session=session, product=hotel)

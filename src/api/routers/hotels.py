from fastapi import APIRouter, Query, Body

from src.repositories.hotels import HotelsRepository
from src.database import async_session_maker
from src.schemas.hotels import HotelPatch, PaginationDep, HotelAdd

hotels_router = APIRouter(prefix="/hotels", tags=["Отели"])


@hotels_router.get("/hotel")
async def get_hotel(hotel_id: int):

    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@hotels_router.get("/hotels")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Расположение отеля"),
):
    limit = pagination.per_page or 5
    offset = limit * (pagination.page - 1)

    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all_hotels(
            title=title, location=location, limit=limit, offset=offset
        )


@hotels_router.post("/hotels")
async def create_hotel(
        hotel_data: HotelAdd = Body(openapi_examples={
            "1": {
                "summary": "Madrid",
                "value": {
                    "title": "Мадрид",
                    "location": "madrid",
                }
            },
            "2": {
                "summary": "Barcelona",
                "value": {
                    "title": "Барселона",
                    "location": "barcelona",
                }
            }
        })
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

        return {"status": "OK", "data": hotel}


@hotels_router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):

    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@hotels_router.put("/{hotel_id}")
async def put_hotel(hotel_id: int, hotel_data: HotelAdd):

    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
        return {"status": "OK"}


@hotels_router.patch("/{hotel_id}")
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch):

    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()

        return {"status": "OK"}

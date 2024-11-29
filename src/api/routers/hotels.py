from fastapi import APIRouter, Query, Body

from repositories.hotels import HotelsRepository
from src.database import async_session_maker
from src.schemas.hotels import Hotel, HotelPatch, PaginationDep

hotels_router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Лондон", "name": "london"},
    {"id": 2, "title": "Париж", "name": "paris"},
    {"id": 3, "title": "Сочи", "name": "sochi"},
    {"id": 4, "title": "Дубай", "name": "dubai"},
    {"id": 5, "title": "Мальдивы", "name": "maldivi"},
    {"id": 6, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 7, "title": "Москва", "name": "moscow"},
    {"id": 8, "title": "Казань", "name": "kazan"},
    {"id": 9, "title": "Санкт-Петербург", "name": "spb"},
]


@hotels_router.get("/hotels")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Расположение отеля"),
):
    limit = pagination.per_page or 5
    offset = limit * (pagination.page - 1)

    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title, location=location, limit=limit, offset=offset
        )


@hotels_router.post("/hotels")
async def create_hotel(
        hotel_data: Hotel = Body(openapi_examples={
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


@hotels_router.delete("/hotels/{hotel_id}")
async def delete_hotel(hotel_id: int):
    global hotels

    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]

    return {"status": "OK"}


async def update_name_and_or_title(hotel_id: int, new_name: str | None, new_title: str | None) -> bool:

    global hotels

    idx, hotel = next(((index, hotel) for index, hotel in enumerate(hotels) if hotel['id'] == hotel_id), (None, None))

    if idx is not None:
        if new_name:
            hotel['name'] = new_name
        if new_title:
            hotel['title'] = new_title
        hotels[idx] = hotel

        return True
    else:
        return False


@hotels_router.put("/hotels/{hotel_id}")
async def put_hotel(hotel_id: int, data: Hotel):
    # Вызывается та же функция, что и для метода patch, т.к. внутри update_name_and_or_title
    # отрабатывается вариант отсутствия name или title, а т.к. в put в аргументах эти значения обязательны,
    # будут отработаны оба аргумента

    result = update_name_and_or_title(hotel_id, data.name, data.title)
    return {"status": "OK" if result else "Hotel not found"}


@hotels_router.patch("/hotels/{hotel_id}")
async def patch_hotel(hotel_id: int, data: HotelPatch):

    result = update_name_and_or_title(hotel_id, data.name, data.title)
    return {"status": "OK" if result else "Hotel not found"}

from fastapi import APIRouter, Query, Body

from database import hotels
from schemas.hotels import Hotel

hotels_router = APIRouter(prefix="/hotels", tags=["Отели"])


@hotels_router.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="ID отеля"),
        title: str | None = Query(None, description="Название отеля"),
):

    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@hotels_router.post("/hotels")
def create_hotel(
        hotel_data: Hotel = Body(openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "name": "sochi_u_morya",
                }
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай У фонтана",
                    "name": "dubai_fountain",
                }
            }
        })
):

    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {"status": "OK"}


@hotels_router.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):

    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]

    return {"status": "OK"}


def update_name_and_or_title(hotel_id: int, new_name: str | None, new_title: str | None) -> bool:

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
def put_hotel(
        hotel_id: int,
        name: str = Body(),
        title: str = Body(),
):
    # Вызывается та же функция, что и для метода patch, т.к. внутри update_name_and_or_title
    # отрабатывается вариант отсутствия name или title, а т.к. в put в аргументах эти значения обязательны,
    # будут отработаны оба аргумента

    result = update_name_and_or_title(hotel_id, name, title)
    return {"status": "OK" if result else "Hotel not found"}


@hotels_router.patch("/hotels/{hotel_id}")
def patch_hotel(
        hotel_id: int,
        name: str | None = Body(None, description="name отеля"),
        title: str | None = Body(None, description="title отеля"),
):
    result = update_name_and_or_title(hotel_id, name, title)
    return {"status": "OK" if result else "Hotel not found"}

from fastapi import APIRouter, Query, Body

from schemas.hotels import Hotel, HotelPatch

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
def get_hotels(
        id: int | None = Query(None, description="ID отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    global hotels

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
                "summary": "Madrid",
                "value": {
                    "title": "Мадрид",
                    "name": "madrid",
                }
            },
            "2": {
                "summary": "Barcelona",
                "value": {
                    "title": "Барселона",
                    "name": "barcelona",
                }
            }
        })
):
    global hotels

    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })

    return {"status": "OK"}


@hotels_router.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels

    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]

    return {"status": "OK"}


def update_name_and_or_title(hotel_id: int, new_name: str | None, new_title: str | None) -> bool:

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
def put_hotel(hotel_id: int, data: Hotel):
    # Вызывается та же функция, что и для метода patch, т.к. внутри update_name_and_or_title
    # отрабатывается вариант отсутствия name или title, а т.к. в put в аргументах эти значения обязательны,
    # будут отработаны оба аргумента

    result = update_name_and_or_title(hotel_id, data.name, data.title)
    return {"status": "OK" if result else "Hotel not found"}


@hotels_router.patch("/hotels/{hotel_id}")
def patch_hotel(hotel_id: int, data: HotelPatch):

    result = update_name_and_or_title(hotel_id, data.name, data.title)
    return {"status": "OK" if result else "Hotel not found"}

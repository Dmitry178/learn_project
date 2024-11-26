import uvicorn

from fastapi import FastAPI, Query, Body
from starlette.responses import RedirectResponse

app = FastAPI()

hotels = [
    {"id": 1, "name": "london", "title": "London"},
    {"id": 2, "name": "paris", "title": "Paris"},
]


@app.get("/")
def redirect():
    return RedirectResponse("/docs")


@app.get("/hotels")
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


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels

    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}")
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


@app.put("/hotels/{hotel_id}")
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

    # idx, hotel = next(((index, hotel) for index, hotel in enumerate(hotels) if hotel['id'] == hotel_id), (None, None))
    #
    # if idx is not None:
    #     hotel['name'] = name
    #     hotel['title'] = title
    #
    #     return {"status": "OK"}
    # else:
    #     return {"status": "hotel not found"}


@app.patch("/hotels/{hotel_id}")
def patch_hotel(
        hotel_id: int,
        name: str | None = Body(None, description="name отеля"),
        title: str | None = Body(None, description="title отеля"),
):
    result = update_name_and_or_title(hotel_id, name, title)
    return {"status": "OK" if result else "Hotel not found"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)

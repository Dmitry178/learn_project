from fastapi import APIRouter, Query, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomGet, RoomAdd, RoomPatch, RoomAddId

rooms_router = APIRouter(prefix="/hotels", tags=["Номера"])


@rooms_router.get("/{hotel_id}/room")
async def get_room(hotel_id: int, room_id: int):
    """
    Получение данных номера с room_id отеля с hotel_id
    """

    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@rooms_router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, data: RoomGet = Query(None)):
    """
    Получение списка номеров отеля с hotel_id
    """

    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))


@rooms_router.post("/{hotel_id}/room")
async def add_room(
        hotel_id: int,
        room_data: RoomAdd = Body(openapi_examples={
            "1": {
                "summary": "Мадрид, одноместный стандарт",
                "value": {
                    "title": "Мадрид",
                    "description": "Одноместный стандарт",
                    "price": 100,
                    "quantity": 10,
                }
            },
            "2": {
                "summary": "Барселона, двухместный люкс",
                "value": {
                    "title": "Барселона",
                    "description": "Двухместный люкс",
                    "price": 300,
                    "quantity": 1,
                }
            }
        })
):
    """
    Добавление номера в отель
    """

    room_data = RoomAddId(hotel_id=hotel_id, **room_data.model_dump())

    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()

        return {"status": "OK", "data": room}


@rooms_router.delete("/{hotel_id}/room/{room_id}")
async def delete_hotel(hotel_id: int, room_id: int):
    """
    Удаление номера в отеле
    """

    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@rooms_router.put("/{hotel_id}/room")
async def put_hotel(hotel_id: int, room_id: int, room_data: RoomAdd):
    """
    Изменение параметров номера в отеле
    """

    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()

        return {"status": "OK"}


@rooms_router.patch("/{hotel_id}/room")
async def patch_hotel(hotel_id: int, room_id: int, room_data: RoomGet):
    """
    Изменение параметров номера в отеле
    """

    room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))

    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id, exclude_unset=True)
        await session.commit()

        return {"status": "OK"}

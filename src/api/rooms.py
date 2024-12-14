from datetime import date
from fastapi import APIRouter, Body, Query, HTTPException

from src.dependencies import DBDep
from src.exceptions import DateError, HotelNotFound, RoomNotFound, HotelNotFoundHTTP
from src.openapi import add_room
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomsService

rooms_router = APIRouter(prefix="/hotels", tags=["Номера"])


@rooms_router.get("/{hotel_id}/room")
async def get_room(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
    """
    Получение данных номера с room_id отеля с hotel_id
    """

    try:
        return await RoomsService(db).get_room(hotel_id, date_from, date_to)

    except (DateError, HotelNotFound) as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)


@rooms_router.get("/{hotel_id}/rooms/{room_id}")
async def get_rooms(hotel_id: int, room_id: int, db: DBDep):
    """
    Получение списка номеров отеля с hotel_id
    """

    try:
        return await RoomsService(db).get_rooms(hotel_id, room_id)

    except (HotelNotFound, RoomNotFound) as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)


@rooms_router.post("/{hotel_id}/room")
async def add_room(
        hotel_id: int,
        db: DBDep,
        room_data: RoomAdd = Body(openapi_examples=add_room)
):
    """
    Добавление номера в отель
    """

    try:
        room = RoomsService(db).add_room(hotel_id, room_data)
        return {"status": "OK", "data": room}

    except HotelNotFound:
        raise HotelNotFoundHTTP


@rooms_router.put("/{hotel_id}/room/{room_id}")
async def put_hotel(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    """
    Изменение параметров номера в отеле
    """

    try:
        await RoomsService(db).put_hotel(hotel_id, room_id, room_data)
        return {"status": "OK"}

    except (HotelNotFound, RoomNotFound) as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)


@rooms_router.patch("/{hotel_id}/room/{room_id}")
async def patch_hotel(hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep):
    """
    Изменение параметров номера в отеле
    """

    try:
        await RoomsService(db).patch_hotel(hotel_id, room_id, room_data)
        return {"status": "OK"}

    except (HotelNotFound, RoomNotFound) as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)


@rooms_router.delete("/{hotel_id}/room/{room_id}")
async def delete_hotel(hotel_id: int, room_id: int, db: DBDep):
    """
    Удаление номера в отеле
    """

    try:
        await RoomsService(db).delete_hotel(hotel_id, room_id)
        return {"status": "OK"}

    except HotelNotFound:
        raise HotelNotFound

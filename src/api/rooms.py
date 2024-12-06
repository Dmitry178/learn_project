from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomGet, RoomAdd, RoomPatch, RoomAddId, RoomAddRequest, RoomPatchRequest

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

    # return await db.rooms.get_rooms_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@rooms_router.get("/{hotel_id}/rooms/{room_id}")
async def get_rooms(hotel_id: int, room_id: int, db: DBDep):
    """
    Получение списка номеров отеля с hotel_id
    """

    # return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    return await db.rooms.get_room_info(room_id=room_id, hotel_id=hotel_id)


@rooms_router.post("/{hotel_id}/room")
async def add_room(
        hotel_id: int,
        db: DBDep,
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
    room = await db.rooms.add(room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)

    await db.commit()

    return {"status": "OK", "data": room}


@rooms_router.delete("/{hotel_id}/room/{room_id}")
async def delete_hotel(hotel_id: int, room_id: int, db: DBDep):
    """
    Удаление номера в отеле
    """

    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@rooms_router.put("/{hotel_id}/room/{room_id}")
async def put_hotel(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    """
    Изменение параметров номера в отеле
    """

    room_data_put = RoomAddId(hotel_id=hotel_id, **room_data.model_dump())

    await db.rooms.edit(room_data_put, id=room_id, hotel_id=hotel_id)
    await db.rooms_facilities.update_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()

    return {"status": "OK"}


@rooms_router.patch("/{hotel_id}/room/{room_id}")
async def patch_hotel(hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep):
    """
    Изменение параметров номера в отеле
    """

    room_data_patch = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))

    await db.rooms.edit(room_data_patch, id=room_id, exclude_unset=True)
    if room_data.facilities_ids:
        await db.rooms_facilities.update_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()

    return {"status": "OK"}

from datetime import date

from fastapi import APIRouter, Query, Body
from fastapi_cache.decorator import cache

from src.dependencies import DBDep
from src.exceptions import DateError, HotelNotFound, ObjectNotFoundException, HotelNotFoundHTTP, DateErrorHTTP
from src.openapi import create_hotel
from src.schemas.hotels import HotelPatch, PaginationDep, HotelAdd
from src.services.hotels import HotelService

hotels_router = APIRouter(prefix="/hotels", tags=["Отели"])


@hotels_router.get("")
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Расположение отеля"),
        date_from: date = Query(example="2024-12-01"),
        date_to: date = Query(example="2024-12-10"),
):
    try:
        result = await HotelService(db).get_hotels(pagination, title, location, date_from, date_to)
        return result

    except DateError:
        raise DateErrorHTTP


@hotels_router.get("/{hotel_id}")
@cache(expire=10)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)

    except ObjectNotFoundException:
        raise HotelNotFoundHTTP


@hotels_router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples=create_hotel)
):
    hotel = await HotelService(db).create_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@hotels_router.put("/{hotel_id}")
async def put_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    try:
        await HotelService(db).put_hotel(hotel_id, hotel_data)
        return {"status": "OK"}

    except HotelNotFound:
        raise HotelNotFoundHTTP


@hotels_router.patch("/{hotel_id}")
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    try:
        await HotelService(db).patch_hotel(hotel_id, hotel_data)
        return {"status": "OK"}

    except HotelNotFound:
        raise HotelNotFoundHTTP


@hotels_router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    try:
        await HotelService(db).delete_hotel(hotel_id)
        return {"status": "OK"}

    except HotelNotFound:
        raise HotelNotFoundHTTP

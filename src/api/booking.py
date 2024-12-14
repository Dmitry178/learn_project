from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.api.utils import check_hotel_dates
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, DateError
from src.schemas.booking import BookingAdd, BookingPost
from src.schemas.rooms import Room

bookings_router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@bookings_router.post("")
async def create_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAdd = Body()
):
    try:
        await check_hotel_dates(booking_data.date_from, booking_data.date_to)
        room: Room = await db.rooms.get_one(id=booking_data.room_id)

    except (DateError, ObjectNotFoundException) as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)

    price: int = room.price

    booking_post = BookingPost(
        user_id=user_id,
        price=price,
        **booking_data.model_dump()
    )

    try:
        booking = await db.bookings.add_booking(booking_post)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)

    await db.commit()

    return {"status": "OK", "data": booking}


@bookings_router.post("/alt")
async def add_booking_alt(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAdd = Body()
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    room_price: int = room.price

    _booking_data = BookingPost(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )

    try:
        booking = await db.bookings.add_booking_alt(_booking_data, hotel_id=hotel.id)
        await db.commit()
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)

    return {"status": "OK", "data": booking}


@bookings_router.get("")
async def get_all_bookings(
        db: DBDep,
):
    bookings = await db.bookings.get_all()
    return bookings


@bookings_router.get("/me")
async def get_my_bookings(
        user_id: UserIdDep,
        db: DBDep,
):
    bookings = await db.bookings.get_all(user_id=user_id)
    return bookings

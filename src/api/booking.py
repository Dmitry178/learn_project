from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.models import RoomsOrm
from src.schemas.booking import BookingAdd, BookingPost

bookings_router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@bookings_router.post("")
async def create_booking(
        hotel_id: int,
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAdd = Body()
):
    room: RoomsOrm = await db.rooms.get_one_or_none(id=booking_data.room_id)
    price: int = room.price

    booking_post = BookingPost(
        hotel_id=hotel_id,
        user_id=user_id,
        price=price,
        **booking_data.model_dump()
    )

    booking = await db.bookings.add(booking_post)
    await db.commit()

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

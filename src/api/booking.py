from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.booking import BookingAdd, BookingPost

bookings_router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@bookings_router.post("/booking")
async def create_booking(
        hotel_id: int,
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAdd = Body()
):
    booking_post = BookingPost(
        hotel_id=hotel_id,
        user_id=user_id,
        price=100,
        **booking_data.model_dump()
    )

    booking = await db.bookings.add(booking_post)
    await db.commit()

    return {"status": "OK", "data": booking}

from fastapi import APIRouter, Body, HTTPException

from src.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, DateError
from src.schemas.booking import BookingAdd
from src.services.bookings import BookingsService

bookings_router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@bookings_router.post("")
async def create_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAdd = Body()
):
    try:
        booking = await BookingsService(db).create_booking(user_id, booking_data)

    except (DateError, ObjectNotFoundException) as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)

    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)

    return {"status": "OK", "data": booking}


@bookings_router.post("/alt")
async def add_booking_alt(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAdd = Body()
):
    try:
        booking = await BookingsService(db).add_booking_alt(user_id, booking_data)

    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)

    return {"status": "OK", "data": booking}


@bookings_router.get("")
async def get_all_bookings(db: DBDep):
    return await BookingsService(db).get_all_bookings()


@bookings_router.get("/me")
async def get_my_bookings(
        user_id: UserIdDep,
        db: DBDep,
):
    return await BookingsService(db).get_my_bookings(user_id)

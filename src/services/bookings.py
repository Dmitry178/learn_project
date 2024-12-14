from src.utils.utils import DataChecker
from src.dependencies import UserIdDep
from src.schemas.booking import BookingAdd, BookingPost
from src.schemas.rooms import Room
from src.services.base import BaseService


class BookingsService(BaseService):
    async def create_booking(self, user_id: UserIdDep, booking_data: BookingAdd):
        await DataChecker.check_dates(booking_data.date_from, booking_data.date_to)
        room: Room = await self.db.rooms.get_one(id=booking_data.room_id)

        price: int = room.price

        booking_post = BookingPost(
            user_id=user_id,
            price=price,
            **booking_data.model_dump()
        )

        booking = await self.db.bookings.add_booking(booking_post)
        await self.db.commit()
        return booking

    async def add_booking_alt(self, user_id: UserIdDep, booking_data: BookingAdd):
        room = await self.db.rooms.get_one_or_none(id=booking_data.room_id)
        hotel = await self.db.hotels.get_one_or_none(id=room.hotel_id)
        room_price: int = room.price

        _booking_data = BookingPost(
            user_id=user_id,
            price=room_price,
            **booking_data.model_dump(),
        )

        booking = await self.db.bookings.add_booking_alt(_booking_data, hotel_id=hotel.id)
        await self.db.commit()

        return booking

    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_all(user_id=user_id)

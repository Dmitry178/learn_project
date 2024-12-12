from datetime import date

from fastapi import HTTPException
from sqlalchemy import select, func
from starlette import status

from src.database import engine
from src.models import BookingsOrm, RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.booking import BookingPost


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, booking: BookingPost):
        """
        Добавление бронирования (вариант решения без использования существующего кода)
        """

        # получение количества свободных комнат

        '''
        WITH rooms_count AS (
            SELECT room_id, COUNT(*) AS rooms_booked
            FROM bookings
            WHERE date_from <= :date_from AND date_to >= :date_to AND room_id == :room_id
            GROUP BY room_id
        ),
        rooms_left_table AS (
            SELECT quantity - COALESCE(rooms_booked, 0) AS rooms_left
            FROM rooms
            WHERE rooms.id
            LEFT JOIN rooms_count ON rooms.id = rooms_count.room_id
        )
        SELECT * FROM rooms_left_table
        WHERE rooms_left > 0;
        '''

        rooms_count = (
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= booking.date_to,
                BookingsOrm.date_to >= booking.date_from,
                BookingsOrm.room_id == booking.room_id,
            )
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
        )

        rooms_left_table = (
            select(
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .filter(RoomsOrm.id == booking.room_id)
            .cte(name="rooms_left_table")
        )

        query = (
            select(rooms_left_table)
            .select_from(rooms_left_table)
            .filter(rooms_left_table.c.rooms_left > 0)
        )

        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        rooms_left = result.scalar()

        print(f'{rooms_left=}')

        if not rooms_left:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Недостаточно свободных номеров")

        # бронирование
        booking = await self.add(booking)

        return booking

    async def add_booking_alt(self, data: BookingPost, hotel_id: int):
        """
        Альтернативный вариант решения с использованием существующего кода
        """

        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )

        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        if data.room_id in rooms_ids_to_book:
            new_booking = await self.add(data)
            return new_booking
        else:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Недостаточно свободных номеров")

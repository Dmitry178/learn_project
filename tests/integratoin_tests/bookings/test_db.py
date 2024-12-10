from datetime import date

from src.schemas.booking import BookingPost


async def test_add_booking(db):

    print("Добавление бронирования")

    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    print(f'{user_id=}')
    print(f'{room_id=}')

    booking_data = BookingPost(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )

    await db.bookings.add(booking_data)
    await db.commit()

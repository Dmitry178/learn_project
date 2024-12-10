from datetime import date

from src.schemas.booking import BookingPost, BookingPatch


async def test_booking_crud(db):

    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    booking_data = BookingPost(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )

    # тест добавления записи
    booking_added = await db.bookings.add(booking_data)
    assert booking_added
    id_ = booking_added.id

    # тест изменение записи
    booking_data = BookingPatch(
        id=id_,
        date_to=date(year=2024, month=8, day=30),
        price=90,
    )
    await db.bookings.edit(booking_data, exclude_unset=True)
    booking_updated = await db.bookings.get_one_or_none(id=id_)
    assert booking_updated

    booking_compare = BookingPatch(
        id=id_,
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=30),
        price=90,
        total_cost=90 * (date(year=2024, month=8, day=30) - date(year=2024, month=8, day=10)).days
    )
    assert booking_updated.model_dump() == booking_compare.model_dump()

    # тест удаления записи
    await db.bookings.delete(id=id_)
    booking_deleted = await db.bookings.get_one_or_none(id=id_)
    assert not booking_deleted

    await db.commit()

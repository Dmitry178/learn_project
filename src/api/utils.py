from src.exceptions import HotelNotFound, RoomNotFound
from src.utils.db_manager import DBManager


async def check_hotel_available(db: DBManager, hotel_id: int) -> None:
    """
    Проверка наличия отеля
    """

    if not await db.hotels.get_one_or_none(id=hotel_id):
        raise HotelNotFound()


async def check_room_available(db: DBManager, room_id: int) -> None:
    """
    Проверка наличия номера
    """

    if not await db.rooms.get_one_or_none(id=room_id):
        raise RoomNotFound()

from datetime import date

from src.exceptions import HotelNotFound, RoomNotFound, DateError
from src.utils.db_manager import DBManager


class DataChecker:
    @staticmethod
    async def check_dates(date_from: date, date_to: date) -> None:
        """
        Проверка корректности дат заезда и выезда
        """

        if date_from >= date_to:
            raise DateError

    @staticmethod
    async def check_hotel_available(db: DBManager, hotel_id: int) -> None:
        """
        Проверка наличия отеля
        """

        if not await db.hotels.get_one_or_none(id=hotel_id):
            raise HotelNotFound()

    @staticmethod
    async def check_room_available(db: DBManager, room_id: int) -> None:
        """
        Проверка наличия номера
        """

        if not await db.rooms.get_one_or_none(id=room_id):
            raise RoomNotFound()

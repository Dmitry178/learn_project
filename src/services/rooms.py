from datetime import date

from src.utils.utils import DataChecker
from src.exceptions import RoomNotFound
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddId, RoomPatch, RoomPatchRequest, RoomAddRequest
from src.services.base import BaseService


class RoomsService(BaseService, DataChecker):
    async def get_room(self, hotel_id: int, date_from: date, date_to: date):
        """
        Получение данных номера с room_id отеля с hotel_id
        """

        await self.check_dates(date_from, date_to)
        await self.check_hotel_available(self.db, hotel_id)

        # return await db.rooms.get_rooms_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
        result = await self.db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

        return result

    async def get_rooms(self, hotel_id: int, room_id: int):
        """
        Получение списка номеров отеля с hotel_id
        """

        await self.check_hotel_available(self.db, hotel_id)
        await self.check_room_available(self.db, room_id)

        # return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
        result = await self.db.rooms.get_room_info(room_id=room_id, hotel_id=hotel_id)
        if not result:
            raise RoomNotFound()

        return result

    async def add_room(self, hotel_id: int, room_data: RoomAdd):
        """
        Добавление номера в отель
        """

        await self.check_hotel_available(self.db, hotel_id)

        room_data = RoomAddId(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(room_data)

        rooms_facilities_data = \
            [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)

        await self.db.commit()

        return room

    async def put_hotel(self, hotel_id: int, room_id: int, room_data: RoomAddRequest):
        """
        Изменение параметров номера в отеле
        """

        await self.check_hotel_available(self.db, hotel_id)
        await self.check_room_available(self.db, room_id)

        room_data_put = RoomAddId(hotel_id=hotel_id, **room_data.model_dump())

        await self.db.rooms.edit(room_data_put, id=room_id, hotel_id=hotel_id)
        await self.db.rooms_facilities.update_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
        await self.db.commit()

    async def patch_hotel(self, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
        """
        Изменение параметров номера в отеле
        """

        await self.check_hotel_available(self.db, hotel_id)
        await self.check_room_available(self.db, room_id)

        room_data_patch = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))

        await self.db.rooms.edit(room_data_patch, id=room_id, exclude_unset=True)

        if room_data.facilities_ids:
            await self.db.rooms_facilities.update_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)

        await self.db.commit()

    async def delete_hotel(self, hotel_id: int, room_id: int):
        """
        Удаление номера в отеле
        """

        await self.check_hotel_available(self.db, hotel_id)
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

from datetime import date

from src.utils.utils import DataChecker
from src.schemas.hotels import PaginationDep, HotelAdd, HotelPatch
from src.services.base import BaseService


class HotelService(BaseService, DataChecker):
    async def get_hotels(
            self,
            pagination: PaginationDep,
            title: str | None,
            location: str | None,
            date_from: date,
            date_to: date,
    ):
        limit = pagination.per_page or 1
        offset = limit * (pagination.page - 1)

        await self.check_dates(date_from, date_to)

        result = await self.db.hotels.get_hotels_by_date(
            date_from=date_from,
            date_to=date_to,
            title=title,
            location=location,
            limit=limit,
            offset=offset,
        )

        # return await db.hotels.get_all_hotels(title=title, location=location, limit=limit, offset=offset)
        return result

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def put_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.check_hotel_available(self.db, hotel_id)
        await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()

    async def patch_hotel(self, hotel_id: int, hotel_data: HotelPatch):
        await self.check_hotel_available(self.db, hotel_id)
        await self.db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.check_hotel_available(self.db, hotel_id)
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

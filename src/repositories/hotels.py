from datetime import date

from src.models import RoomsOrm
from src.repositories.base import BaseRepository
from sqlalchemy import select, func

from src.database import engine
from src.models.hotels import HotelsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all_hotels(
            self, title: str, location: str, limit: int | None = None, offset: int | None = None
    ) -> list[Hotel]:

        query = select(HotelsOrm.id, HotelsOrm.title, HotelsOrm.location)

        if title:
            query = query.where(func.lower(HotelsOrm.title).contains(title.lower()))

        if location:
            query = query.where(func.lower(HotelsOrm.location).ilike(f'%{location.lower()}%'))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        # return result.mappings().all()
        return [self.schema.model_validate(hotel, from_attributes=True) for hotel in result.mappings().all()]

    async def get_hotels_by_date(
            self,
            date_from: date,
            date_to: date,
            title: str | None = None,
            location: str | None = None,
            limit: int | None = None,
            offset: int | None = None,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = (
            select(self.model)
            .filter(HotelsOrm.id.in_(hotels_ids_to_get))
        )

        if title:
            query = query.where(func.lower(HotelsOrm.title).contains(title.lower()))

        if location:
            query = query.where(func.lower(HotelsOrm.location).ilike(f'%{location.lower()}%'))

        if limit:
            query = (
                query
                .limit(limit)
                .offset(offset)
            )

        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

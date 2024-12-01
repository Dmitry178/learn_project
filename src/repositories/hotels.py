from src.repositories.base import BaseRepository
from sqlalchemy import select, func

from src.database import engine
from src.models.hotels import HotelsOrm
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

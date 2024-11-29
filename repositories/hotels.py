from repositories.base import BaseRepository
from sqlalchemy import select, func, RowMapping

from src.database import engine
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self, location: str, title: str, limit: int | None = None, offset: int | None = None
    ) -> RowMapping:

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

        return result.mappings().all()

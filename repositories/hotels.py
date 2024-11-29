from repositories.base import BaseRepository
from sqlalchemy import select, func, RowMapping, insert

from src.database import engine
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self, title: str, location: str, limit: int | None = None, offset: int | None = None
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

    async def insert_data(self, **data) -> RowMapping:

        stmt = (
            insert(HotelsOrm)
            .values(**data)
            .returning(HotelsOrm)
        )
        result = await self.session.execute(stmt)

        return result.fetchone()[0]

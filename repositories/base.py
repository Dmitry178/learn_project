from pydantic import BaseModel
from sqlalchemy import select, insert, RowMapping


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs) -> RowMapping:
        query = select(self.model)
        result = await self.session.execute(query)
        return result.mappings().all()

    async def get_one_or_none(self, **filter_by) -> RowMapping:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.mappings().one_or_none()

    async def add(self, data: BaseModel) -> RowMapping:

        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()

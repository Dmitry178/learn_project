from pydantic import BaseModel
from sqlalchemy import select, insert, RowMapping, delete, update


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
        return result.mappings().one()

    async def edit(self, data: BaseModel, **filter_by) -> None:

        add_data_stmt = (
            update(self.model)
            .values(**data.model_dump())
            .filter_by(**filter_by)
            # .returning(self.model)
        )
        await self.session.execute(add_data_stmt)
        return None

    async def edit_by_id(self, pk: int, data: BaseModel) -> None:

        add_data_stmt = (
            update(self.model)
            .values(**data.model_dump())
            .filter_by(id=pk)
            # .returning(self.model)
        )
        await self.session.execute(add_data_stmt)

        return None

    async def delete(self, data: BaseModel) -> None:

        delete_stmt = delete(self.model).filter_by(**data.model_dump())
        await self.session.execute(delete_stmt)
        return None

    async def delete_by_id(self, pk: int) -> None:

        delete_stmt = delete(self.model).filter_by(id=pk)
        await self.session.execute(delete_stmt)
        return None

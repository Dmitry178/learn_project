from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import select, insert, RowMapping, delete, update
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = (
            select(self.model)
            .filter(*args)
            .filter_by(**kwargs)
        )
        result = await self.session.execute(query)

        # return result.mappings().all()
        # return [self.schema.model_validate(model) for model in result.scalars().all()]
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException

        return self.mapper.map_to_domain_entity(model)

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()

        if model is None:
            return None

        # return self.schema.model_validate(model, from_attributes=True)
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel) -> RowMapping:
        try:
            add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()

            # return self.schema.model_validate(model, from_attributes=True)
            return self.mapper.map_to_domain_entity(model)

        except IntegrityError as ex:
            print(f"{type(ex.orig.__cause__)=}")
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            else:
                raise ex

    async def add_bulk(self, data: list[BaseModel]) -> None:

        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def add_raw(self, raw_data) -> None:

        add_data_stmt = insert(self.model).values(raw_data)
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:

        edit_data_stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .filter_by(**filter_by)
            # .returning(self.model)
        )
        await self.session.execute(edit_data_stmt)
        return None

    async def edit_by_id(self, id_: int, data: BaseModel, exclude_unset: bool = False) -> None:

        edit_data_stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .filter_by(id=id_)
            # .returning(self.model)
        )
        await self.session.execute(edit_data_stmt)

        return None

    async def delete(self, **filter_by) -> None:

        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
        return None

    async def delete_by_id(self, id_: int) -> None:

        delete_stmt = delete(self.model).filter_by(id=id_)
        await self.session.execute(delete_stmt)
        return None

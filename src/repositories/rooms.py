from datetime import date

from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.database import engine
from src.exceptions import RoomNotFoundException
from src.models import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)

        # return [RoomWithRels.model_validate(model) for model in result.unique().scalars().all()]
        return [RoomDataWithRelsMapper.map_to_domain_entity(model) for model in result.unique().scalars().all()]

    async def get_room_info(
            self,
            room_id: int,
            hotel_id: int,
    ):
        query = (
            select(self.model)
            .options(selectinload(RoomsOrm.facilities))
            .filter(RoomsOrm.id == room_id, RoomsOrm.hotel_id == hotel_id)
        )
        result = await self.session.execute(query)
        result = result.unique().scalars().one_or_none()

        # return RoomWithRels.model_validate(result)
        return RoomDataWithRelsMapper.map_to_domain_entity(result)

    async def get_one_or_none_with_rels(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )

        result = await self.session.execute(query)
        model = result.scalars().one_or_none()

        if model is None:
            return None

        # return RoomWithRels.model_validate(model)
        return RoomDataWithRelsMapper.map_to_domain_entity(model)

    async def get_one_with_rels(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )

        result = await self.session.execute(query)

        try:
            model = result.scalar_one()

        except NoResultFound:
            raise RoomNotFoundException

        return RoomDataWithRelsMapper.map_to_domain_entity(model)

    async def get_filtered_by_date(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        result = self.get_all(RoomsOrm.id.in_(rooms_ids_to_get))

        # return self.get_all(RoomsOrm.id.in_(rooms_ids_to_get))
        return RoomDataWithRelsMapper.map_to_domain_entity(result)

    async def get_rooms_by_date(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        """
        Получение отелей по датам
        """

        '''
        with rooms_count as (
            select room_id, count(*) as rooms_booked from bookings
            where date_from <= '2024-11-07' and date_to >= '2024-07-01'
            group by room_id
        ),
        rooms_left_table as (
            select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
            from rooms
            left join rooms_count on rooms.id = rooms_count.room_id
        )
        select * from rooms_left_table
        where rooms_left > 0;
        '''

        '''
        rooms_count as (
        select room_id, count(*) as rooms_booked from bookings
            where date_from <= '2024-11-07' and date_to >= '2024-07-01'
            group by room_id
        '''

        rooms_count = (
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= date_to,
                BookingsOrm.date_to >= date_from,
            )
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
        )

        '''
        rooms_left_table as (
            select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
            from rooms
            left join rooms_count on rooms.id = rooms_count.room_id
        )
        '''

        rooms_left_table = (
            select(
                RoomsOrm.id.label("room_id"),
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )

        '''
        select * from rooms_left_table
        where rooms_left > 0
        '''

        query = (
            select(rooms_left_table)
            .select_from(rooms_left_table)
            .filter(rooms_left_table.c.rooms_left > 0)
        )

        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        rooms_ids_for_hotel = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            .subquery(name="rooms_ids_for_hotel")
        )

        rooms_ids_to_get = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(
                rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(rooms_ids_for_hotel),
            )
        )

        return await self.get_all(RoomsOrm.id.in_(rooms_ids_to_get))

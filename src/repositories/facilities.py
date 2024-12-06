from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert

from src.models import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomsFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacility

    async def update_facilities(self, room_id: int, facilities_ids: list):
        """
        Обновление удобств в номерах
        """

        delete_stmt = (
            delete(self.model)
            .where(
                self.model.room_id == room_id,
                ~self.model.facility_id.in_(facilities_ids)
            )
        )

        data = [{"room_id": room_id, "facility_id": facility_id} for facility_id in facilities_ids]
        insert_stmt = insert(self.model).values(data).on_conflict_do_nothing(index_elements=["room_id", "facility_id"])

        await self.session.execute(insert_stmt)
        await self.session.execute(delete_stmt)

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]) -> None:
        """
        Обновление удобств в номерах (альтернативный вариант из курса)
        """

        get_current_facilities_ids_query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )
        res = await self.session.execute(get_current_facilities_ids_query)

        current_facilities_ids: list[int] = res.scalars().all()

        ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_insert: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:
            delete_m2m_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_delete),
                )
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        if ids_to_insert:
            insert_m2m_facilities_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert])
            )
            await self.session.execute(insert_m2m_facilities_stmt)

from sqlalchemy import delete
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

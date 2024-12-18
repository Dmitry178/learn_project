from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import some_test_task


class FacilitiesService(BaseService):
    async def get_facilities(self):
        """
        Получение всех удобств
        """

        return await self.db.facilities.get_all()

        # facilities_from_cache = await redis_manager.get("facilities")
        #
        # if not facilities_from_cache:
        #     print("Чтение из базы данных")
        #     facilities = await db.facilities.get_all()
        #     facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        #     facilities_json = json.dumps(facilities_schemas)
        #     await redis_manager.set("facilities", facilities_json, 10)
        #     return facilities
        #
        # else:
        #     facilities_dicts = json.loads(facilities_from_cache)
        #     return facilities_dicts

    async def post_facility(self, facility_data: FacilityAdd):
        """
        Добавления нового удобства
        """

        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()

        # some_test_task.delay()

        return facility

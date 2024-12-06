from pydantic import BaseModel, ConfigDict

from src.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []

    
class RoomAdd(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomAddId(RoomAdd):
    hotel_id: int


class Room(RoomAddId):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RoomGet(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomPatch(RoomGet):
    hotel_id: int


class RoomPatchRequest(RoomGet):
    facilities_ids: list[int] = []


class RoomWithRels(Room):
    facilities: list[Facility]

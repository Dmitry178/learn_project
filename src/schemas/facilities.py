from pydantic import BaseModel, ConfigDict


class FacilityAdd(BaseModel):
    title: str


class Facility(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomsFacility(BaseModel):
    id: int
    room_id: int
    facility_id: int

    model_config = ConfigDict(from_attributes=True)

from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingAdd(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingPost(BookingAdd):
    user_id: int
    price: int


class Booking(BookingAdd):
    id: int
    user_id: int
    price: int
    total_cost: int

    model_config = ConfigDict(from_attributes=True)


class BookingPatch(BaseModel):
    id: int
    user_id: int | None = None
    room_id: int | None = None
    date_from: date | None = None
    date_to: date | None = None
    price: int | None = None
    total_cost: int | None = None

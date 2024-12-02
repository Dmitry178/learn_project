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

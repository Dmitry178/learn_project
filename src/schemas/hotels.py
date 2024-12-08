from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel, Field


class HotelAdd(BaseModel):
    title: str
    location: str


class Hotel(BaseModel):
    id: int
    title: str
    location: str


class HotelPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, le=30)]


PaginationDep = Annotated[PaginationParams, Depends()]

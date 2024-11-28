from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    name: str


class HotelPatch(BaseModel):
    title: str | None = Field(None)
    name: str | None = Field(None)


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(None, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, le=30)]


PaginationDep = Annotated[PaginationParams, Depends()]

from fastapi import Depends, HTTPException, Request
from typing import Annotated

from src.database import async_session_maker
from src.services.auth import AuthServices
from src.utils.db_manager import DBManager


def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token", None)
    if not access_token:
        raise HTTPException(status_code=401, detail="Token not found")
    return access_token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    decoded_token = AuthServices().decode_token(token)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Token error")

    user_id = decoded_token.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not found")

    return user_id


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]

# ruff: noqa: E402

import json
import pytest

from httpx import AsyncClient, ASGITransport
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()
# mock.patch("src.cache.cache_decorator.my_cache", lambda *args, **kwargs: lambda f: f).start()

from src.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *  # noqa
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> DBManager:
    # async with DBManager(session_factory=async_session_maker_null_pool) as db:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):

    with open('tests/mock_hotels.json', 'r') as file:
        mock_hotels = json.load(file)

    with open('tests/mock_rooms.json', 'r') as file:
        mock_rooms = json.load(file)

    print("Очистка базы данных")

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print("Добавление исходных данных")

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_raw(mock_hotels)
        await db_.rooms.add_raw(mock_rooms)
        await db_.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    response = await ac.post(
        "/auth/register",
        json={
            "email": "test@user.com",
            "password": "12345"
        }
    )
    assert response.status_code == 200, "Ошибка создания пользователя"


@pytest.fixture(scope="session")
async def aac(register_user, ac):
    # authenticated_ac
    response = await ac.post(
        "/auth/login",
        json={
            "email": "test@user.com",
            "password": "12345"
        }
    )
    assert response.status_code == 200, "Пользователь не создан"
    assert "access_token" in ac.cookies, "Кука не создана"
    yield ac

import pytest

from src.utils.db_manager import DBManager
from tests.conftest import get_db_null_pool


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-02", "2024-08-11", 200),
    (1, "2024-08-03", "2024-08-12", 200),
    (1, "2024-08-04", "2024-08-13", 200),
    (1, "2024-08-05", "2024-08-14", 200),
    (1, "2024-08-06", "2024-08-15", 409),
    (1, "2024-08-17", "2024-08-25", 200),
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, aac):

    # room_id = (await db.rooms.get_all())[0].id
    response = await aac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        result = response.json()
        assert isinstance(result, dict)
        assert result["status"] == "OK"
        assert "data" in result


@pytest.fixture(scope="module")
async def db_m() -> DBManager:
    async for db_m in get_db_null_pool():
        yield db_m


@pytest.fixture(scope="module")
async def delete_bookings():
    # await db_m.bookings.delete()
    # await db_m.commit()
    # yield
    # pass
    async for db_ in get_db_null_pool():
        await db_.bookings.delete()
        await db_.commit()


@pytest.mark.parametrize("room_id, date_from, date_to, status_code, num_bookings", [
    (1, "2024-08-01", "2024-08-10", 200, 1),
    (1, "2024-08-02", "2024-08-11", 200, 2),
    (1, "2024-08-03", "2024-08-12", 200, 3),
    (1, "2024-08-04", "2024-08-13", 200, 4),
    (1, "2024-08-05", "2024-08-14", 200, 5),
    (1, "2024-08-06", "2024-08-15", 409, 5),
    (1, "2024-08-17", "2024-08-25", 200, 6),
])
async def test_add_and_get_bookings(
        room_id, date_from, date_to, status_code, num_bookings,
        delete_bookings, aac
):
    response_bookings = await aac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response_bookings.status_code == status_code

    response_me = await aac.get("/bookings/me")
    assert response_me.status_code == 200
    json_data = response_me.json()
    assert isinstance(json_data, list)
    assert len(response_me.json()) == num_bookings

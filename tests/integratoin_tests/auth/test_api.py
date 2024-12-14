import pytest

from src.schemas.users import UserRequestAdd

email = "email@example.com"
password = "1234"


async def test_create_user(ac):
    """
    Тестирование регистрации пользователя
    """

    # регистрация пользователя
    data = UserRequestAdd(
        email=email,
        password=password
    )

    response = await ac.post(
        "/auth/register",
        json=data.model_dump()
    )
    assert response.status_code == 200, "Ошибка статуса первичного создания пользователя"
    assert response.json()["status"] == "OK", "Ошибка операции создания пользователя"

    # повторная регистрация пользователя
    response = await ac.post(
        "/auth/register",
        json=data.model_dump()
    )
    assert response.status_code == 409, "Ошибка статуса повторного пользователя"


@pytest.mark.parametrize("email_, password_, status_code", [
    (f"1{email}", password, 401),
    (email, f"1{password}", 401),
    (email, password, 200),
    ("email@1234", "password", 422),
])
async def test_login(email_: str, password_: str, status_code: int, ac):
    """
    Тестирование входа пользователя (логина) и получения информации о пользователе
    """

    # попытка логина
    response = await ac.post(
        "/auth/login",
        json={"email": email_, "password": password_}
    )
    assert response.status_code == status_code

    if response.status_code != 200:
        return

    # получение данных пользователя
    response = await ac.get("/auth/user_info")
    assert response.status_code == status_code
    if response.status_code == 200:
        json_data = response.json()
        assert "password" not in json_data
        assert "hashed_password" not in json_data
        json_data = json_data["user"]
        assert json_data["email"] == email_
        assert "id" in json_data


async def test_logout(ac):
    """
    Тестирование выхода (логаута)
    """

    # вход
    response = await ac.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "access_token" in ac.cookies

    # проверка информации о пользователе
    response = await ac.get("/auth/user_info")
    assert response.status_code == 200
    assert "user" in response.json()

    # выход
    response = await ac.post("/auth/logout")
    assert response.status_code == 200

    # проверка информации о пользователе
    response = await ac.get("/auth/user_info")
    assert response.status_code == 401
    assert "access_token" not in ac.cookies

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
    assert response.status_code == 200, "Ошибка статуса повторного пользователя"
    assert response.json()["status"] == "Ошибка создания пользователя", "Пользователь не должен быть создан"


@pytest.mark.parametrize("email_, password_, status_code", [
    (f"1{email}", password, 401),
    (email, f"1{password}", 401),
    (email, password, 200),
])
async def test_login(email_, password_, status_code, ac):
    """
    Тестирование входа пользователя (логина) и получения информации о пользователе
    """

    # попытка логина
    data = UserRequestAdd(
        email=email_,
        password=password_
    )
    response = await ac.post(
        "/auth/login",
        json=data.model_dump()
    )
    assert response.status_code == status_code

    # получение данных пользователя
    response = await ac.get("/auth/user_info")
    assert response.status_code == status_code


async def test_logout(ac):
    """
    Тестирование выхода (логаута)
    """

    # вход
    response = await ac.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    assert "access_token" in response.json()

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

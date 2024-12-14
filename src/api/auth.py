from fastapi import APIRouter, HTTPException, Response

from src.dependencies import UserIdDep, DBDep
from src.exceptions import UserExists, UserNotFound, PasswordIncorrect, ObjectNotFoundException, UserNotFoundHTTP
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@auth_router.post("/login")
async def login_user(response: Response, data: UserRequestAdd, db: DBDep):
    """
    Логин пользователя
    """

    # bcrypt 3.2.0

    try:
        access_token = await AuthService(db).login_user(response, data)
        return {"access_token": access_token}

    except (UserNotFound, PasswordIncorrect) as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)

    except Exception:
        raise HTTPException(status_code=401, detail="Ошибка получения пользователя")


@auth_router.post("/logout")
async def logout_user(response: Response):
    """
    Выход пользователя
    """

    await AuthService().logout_user(response)
    return {"status": "OK"}


@auth_router.post("/register")
async def register_user(data: UserRequestAdd, db: DBDep):
    """
    Регистрация пользователя
    """

    try:
        await AuthService(db).register_user(data)
        return {"status": "OK"}

    except UserExists as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)


@auth_router.get("/user_info")
async def user_info(user_id: UserIdDep, db: DBDep):
    """
    Получение информации об аутентифицированном пользователе
    """

    try:
        user = await AuthService(db).user_info(user_id)
        return {"user": user}

    except ObjectNotFoundException:
        raise UserNotFoundHTTP

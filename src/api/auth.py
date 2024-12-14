from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import UserExists, UserNotFound
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@auth_router.post("/login")
async def login_user(response: Response, data: UserRequestAdd, db: DBDep):
    """
    Логин пользователя
    """

    # bcrypt 3.2.0

    try:
        user = await db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise UserNotFound

    except UserNotFound as ex:
        raise HTTPException(status_code=401, detail=ex.detail)

    except Exception:
        raise HTTPException(status_code=401, detail="Ошибка получения пользователя")

    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="User password incorrect")

    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)

    return {"access_token": access_token}


@auth_router.post("/logout")
async def logout_user(response: Response):
    """
    Выход пользователя
    """

    response.delete_cookie("access_token")
    return {"status": "OK"}


@auth_router.post("/register")
async def register_user(data: UserRequestAdd, db: DBDep):
    """
    Регистрация пользователя
    """

    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

    try:
        if await db.users.get_one_or_none(email=data.email):
            raise UserExists()

        await db.users.add(new_user_data)
        await db.commit()
        return {"status": "OK"}

    except UserExists as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)


@auth_router.get("/user_info")
async def user_info(user_id: UserIdDep, db: DBDep):
    """
    Получение информации об аутентифицированном пользователе
    """

    user = await db.users.get_one_or_none(id=user_id)
    return {"user": user}

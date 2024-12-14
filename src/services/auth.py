import jwt

from datetime import datetime, timezone, timedelta
from fastapi import Response
from passlib.context import CryptContext

from src.config import settings
from src.exceptions import UserNotFound, PasswordIncorrect, UserExists
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.base import BaseService


class AuthServices:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, algorithms=settings.JWT_ALGORITHM, key=settings.JWT_SECRET_KEY)
            return payload
        except:  # noqa
            return {}


class AuthService(BaseService):
    async def login_user(self, response: Response, data: UserRequestAdd):
        """
        Логин пользователя
        """

        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise UserNotFound

        if not AuthServices().verify_password(data.password, user.hashed_password):
            raise PasswordIncorrect

        access_token = AuthServices().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)

        return access_token

    @staticmethod
    async def logout_user(response: Response):
        """
        Выход пользователя
        """

        response.delete_cookie("access_token")

    async def register_user(self, data: UserRequestAdd):
        """
        Регистрация пользователя
        """

        hashed_password = AuthServices().hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

        if await self.db.users.get_one_or_none(email=data.email):
            raise UserExists()

        await self.db.users.add(new_user_data)
        await self.db.commit()

    async def user_info(self, user_id: int):
        """
        Получение информации об аутентифицированном пользователе
        """

        return await self.db.users.get_one(id=user_id)

from fastapi import HTTPException


class BaseCustomException(Exception):
    detail = "Неожиданная ошибка"
    status_code = 400

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args)


class ObjectNotFoundException(BaseCustomException):
    detail = "Объект не найден"
    status_code = 404


class ObjectAlreadyExistsException(BaseCustomException):
    detail = "Объект уже существует"


class AllRoomsAreBookedException(BaseCustomException):
    detail = "Не осталось свободных номеров"
    status_code = 404


class RoomNotFoundException(BaseCustomException):
    detail = "Комната не найдена"
    status_code = 404


class UserExists(BaseCustomException):
    detail = "Пользователь уже зарегистрирован"
    status_code = 409


class UserNotFound(BaseCustomException):
    detail = "Пользователь не найден"
    status_code = 404


class PasswordIncorrect(BaseCustomException):
    detail = "Пароль пользователя неверный"
    status_code = 401


class DateError(BaseCustomException):
    detail = "Даты указаны неверно"


class HotelNotFound(BaseCustomException):
    detail = "Отель не найден"
    status_code = 404


class RoomNotFound(BaseCustomException):
    detail = "Комната не найдена"
    status_code = 404


DateErrorHTTP = HTTPException(status_code=400, detail="Даты указаны неверно")
FacilityExistsHTTP = HTTPException(status_code=409, detail="Такое удобство уже существует")
HotelNotFoundHTTP = HTTPException(status_code=404, detail="Отель не существует")
UserNotFoundHTTP = HTTPException(status_code=404, detail="Пользователь не найден")

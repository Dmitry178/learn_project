class BookingsException(Exception):
    detail = "Неожиданная ошибка"
    status_code = 400

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args)


class ObjectNotFoundException(BookingsException):
    detail = "Объект не найден"
    status_code = 404


class AllRoomsAreBookedException(BookingsException):
    detail = "Не осталось свободных номеров"
    status_code = 404


class UserExists(BookingsException):
    detail = "Пользователь уже зарегистрирован"
    status_code = 409


class UserNotFound(BookingsException):
    detail = "Пользователь не найден"
    status_code = 404


class DateError(BookingsException):
    detail = "Даты указаны неверно"


class HotelNotFound(BookingsException):
    detail = "Отель не найден"
    status_code = 404


class RoomNotFound(BookingsException):
    detail = "Комната не найдена"
    status_code = 404

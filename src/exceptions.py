class BookingsException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args)


class ObjectNotFoundException(BookingsException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(BookingsException):
    detail = "Не осталось свободных номеров"

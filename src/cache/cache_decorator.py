import hashlib
import json
import pickle
import re

from functools import wraps

from src.init import redis_manager


def hash_params(params: dict):
    """
    Хеширование параметров
    """

    # переводим параметры в строку
    json_str = json.dumps(sorted(params), default=str)

    # убираем данные, заключенные в угловые скобки,
    # таким образом убираются различные зависимости, остаётся всё остальное
    cleaned_str = re.sub(r'<[^>]*>', '', json_str)

    # хеширование результата для использования в качестве ключа
    result = hashlib.md5(cleaned_str.encode()).hexdigest()

    return result


def my_cache(expire: int = 10):
    """
    Кеширование результатов работы эндпоинта в redis
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):

            # создаём ключ для redis на основе хеширования входящих параметров
            key = hash_params(kwargs)
            redis_data = await redis_manager.get(key)

            if redis_data:
                # в redis есть данные, возвращаем их
                print('Используется кэш')
                return pickle.loads(redis_data)
            else:
                # в redis нет данных, вызываем функцию, помещаем данные в redis
                print('Запускается эндпоинт')
                result = await func(*args, **kwargs)
                await redis_manager.set(key, pickle.dumps(result), expire=expire)
                return result

        return wrapper
    return decorator

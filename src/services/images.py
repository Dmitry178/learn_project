import shutil

from fastapi import UploadFile, BackgroundTasks

from src.tasks.tasks import resize_image_celery, resize_image_bg_tasks


class ImagesService:
    @staticmethod
    async def upload_image_celery(file: UploadFile):
        """
        Загрузка и обработка изображения через celery
        """

        image_path = f"src/static/images/{file.filename}"

        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        resize_image_celery.delay(image_path)

    @staticmethod
    async def upload_image_bg_tasks(file: UploadFile, background_tasks: BackgroundTasks):
        """
        Загрузка и обработка изображения через background tasks
        """

        image_path = f"src/static/images/{file.filename}"

        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        background_tasks.add_task(resize_image_bg_tasks, image_path)

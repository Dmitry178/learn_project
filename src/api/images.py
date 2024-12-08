import shutil

from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.tasks.tasks import resize_image_bg_tasks, resize_image_celery

images_router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@images_router.post("/celery")
def upload_image_celery(file: UploadFile):
    """
    Загрузка и обработка изображения через celery
    """

    image_path = f"src/static/images/{file.filename}"

    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image_celery.delay(image_path)


@images_router.post("/bg_tasks")
def upload_image_bg_tasks(file: UploadFile, background_tasks: BackgroundTasks):
    """
    Загрузка и обработка изображения через background tasks
    """

    image_path = f"src/static/images/{file.filename}"

    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    background_tasks.add_task(resize_image_bg_tasks, image_path)

from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.images import ImagesService

images_router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@images_router.post("/celery")
async def upload_image_celery(file: UploadFile):
    """
    Загрузка и обработка изображения через celery
    """

    await ImagesService().upload_image_celery(file)
    return {"status": "OK"}


@images_router.post("/bg_tasks")
async def upload_image_bg_tasks(file: UploadFile, background_tasks: BackgroundTasks):
    """
    Загрузка и обработка изображения через background tasks
    """

    await ImagesService().upload_image_bg_tasks(file, background_tasks)
    return {"status": "OK"}

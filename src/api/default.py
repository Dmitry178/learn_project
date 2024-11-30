from fastapi import APIRouter
from starlette.responses import RedirectResponse

default_router = APIRouter()


@default_router.get("/", include_in_schema=False, summary="Редирект на Swagger UI")
def redirect():
    return RedirectResponse("/docs")

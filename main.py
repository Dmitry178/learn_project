import uvicorn

from fastapi import FastAPI

from routers.hotels import hotels_router
from routers.load import load_router

app = FastAPI()

app.include_router(hotels_router)
app.include_router(load_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)

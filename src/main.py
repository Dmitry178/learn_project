import uvicorn

from fastapi import FastAPI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.default import default_router
from src.api.auth import auth_router
from src.api.hotels import hotels_router
from src.api.load import load_router

app = FastAPI()

app.include_router(default_router)
app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(load_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)

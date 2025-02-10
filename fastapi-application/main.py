import uvicorn
from fastapi import FastAPI

from config import settings
from api import router as api_router

app = FastAPI()
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        host=settings.run.host,
        port=settings.run.port,
    )

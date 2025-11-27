from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.db import init_db
from src.api.router import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Lead Distribution Service",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}

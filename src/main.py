from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="CRM System",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}

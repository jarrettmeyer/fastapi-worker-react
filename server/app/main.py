from fastapi import Depends, FastAPI, Request
from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator
from psycopg import AsyncConnection
import logging
from . import database

logging.basicConfig(
    format="%(levelname)s: %(name)s - %(message)s",
    level=logging.DEBUG,
)
log = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """FastAPI lifespan (startup/shutdown) event."""

    # Startup events
    log.debug("Startup FastAPI server")

    yield

    # Shutdown events
    log.debug("Shutdown FastAPI server")

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index():
    return {"status":"ok"}


@app.get("/tasks")
async def get_tasks(request: Request):
    offset = int(request.query_params.get("offset", "0"))
    limit = int(request.query_params.get("limit", "100"))
    return await database.get_tasks(offset=offset, limit=limit)


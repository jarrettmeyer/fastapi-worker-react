from fastapi import Depends, FastAPI, Request
from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator
from psycopg import AsyncConnection
import logging
from . import database
from uuid import UUID

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
async def get_tasks(offset: int = 0, limit: int = 100):
    return await database.get_tasks(offset=offset, limit=limit)


@app.get("/tasks/{task_id}")
async def get_task(task_id: UUID):
    log.debug(f"get task by id: {task_id}")
    return await database.get_task_by_id(task_id)


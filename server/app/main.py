from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncIterator
from .database import get_db_connection_pool
import logging

logging.basicConfig(
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
log = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """FastAPI lifespan (startup/shutdown) event."""

    # Startup events
    log.debug("Startup FastAPI server")
    db_connection_pool = get_db_connection_pool()
    await db_connection_pool.open()

    yield

    # Shutdown events
    log.debug("Shutdown FastAPI server")
    await db_connection_pool.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index():
    return {"status":"ok"}



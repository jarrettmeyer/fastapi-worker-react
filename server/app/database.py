import logging
from datetime import datetime
from functools import lru_cache
from typing import List, Optional
from uuid import UUID

from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool, ConnectionPool
from pydantic import BaseModel

from .config import POSTGRES_CONNECTION_STRING

log = logging.getLogger(__name__)


class Task(BaseModel):
    task_id: Optional[UUID]
    descr: Optional[str]
    created_ts: Optional[datetime]
    updated_ts: Optional[datetime]
    status: Optional[str]


@lru_cache()
def get_async_connection_pool() -> AsyncConnectionPool:
    """Get async connection pool for database operations."""
    return AsyncConnectionPool(
        conninfo=POSTGRES_CONNECTION_STRING,
        open=False,
    )


@lru_cache()
def get_connection_pool() -> ConnectionPool:
    return ConnectionPool(
        conninfo=POSTGRES_CONNECTION_STRING,
        open=False,
    )


async def get_tasks(offset: int = 0, limit: int = 100) -> List[Task]:
    """Get a paginated list of tasks."""
    pool = get_async_connection_pool()
    await pool.open()
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=class_row(Task)) as cursor:
            query = """
                SELECT t.*
                FROM public.tasks t
                ORDER BY t.updated_ts DESC
                OFFSET %(offset)s
                LIMIT %(limit)s;
            """
            params = {
                "offset": offset,
                "limit": limit,
            }
            await cursor.execute(query=query, params=params)
            return await cursor.fetchall()

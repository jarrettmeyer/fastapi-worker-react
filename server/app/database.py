from psycopg import AsyncConnection
from psycopg.rows import TupleRow
from typing import Any, AsyncGenerator, List, cast
from .models import Task
from psycopg_pool import AsyncConnectionPool
from fastapi import Request
from .config import POSTGRES_CONNECTION_STRING


def get_db_connection_pool() -> AsyncConnectionPool:
    """Get database connection pool for psycopg.

    This connection pool will be opened in the FastAPI server startup lifespan event."""
    return AsyncConnectionPool(
        conninfo=POSTGRES_CONNECTION_STRING,
        open=False,
    )


async def get_db_connection(request: Request) -> AsyncGenerator[AsyncConnection]:
    """Get database connection from the database connection pool."""
    db_connection_pool = cast(AsyncConnectionPool, request.state.db_connection_pool)
    async with db_connection_pool.connection() as conn:
        yield conn

async def list_tasks(start: int = 0, take: int = 100) -> List[Task]:
    return []

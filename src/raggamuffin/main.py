import asyncio

from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel


def get_engine() -> Engine:
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

    return create_async_engine(sqlite_url, echo=True)


async def async_main() -> None:
    engine = get_engine()

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


def main():
    asyncio.run(async_main())

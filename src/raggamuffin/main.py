import asyncio
import logging
from pathlib import Path

from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel

from raggamuffin.handlers import DocumentHandler

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
MAX_DOCS = 100


def get_engine() -> Engine:
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

    return create_async_engine(sqlite_url, echo=True)


async def async_main() -> None:
    engine = get_engine()

    # async_sessionmaker: a factory for new AsyncSession objects.
    # expire_on_commit - don't expire objects after transaction commit
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    logger.info("Preparing document batch")
    h = DocumentHandler(Path.home())
    doc_count = 0
    docs = []
    for doc in h.get_documents():
        if doc_count == MAX_DOCS:
            break

        docs.append(doc)
        doc_count += 1

        logger.info("Added %d documents", doc_count)

    logger.info("Adding docs to database")
    async with async_session() as session:
        async with session.begin():
            session.add_all(docs)

    logger.info("Clean up session")
    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


def main():
    asyncio.run(async_main())

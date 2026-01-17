"""Main entry point for raggamuffin."""

import asyncio
import logging
from pathlib import Path

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel

# Import all models to ensure they're registered with SQLModel.metadata
from raggamuffin import models  # noqa: F401
from raggamuffin.handlers import DocumentHandler

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
MAX_DOCS = 100


def get_engine() -> AsyncEngine:
    """Create async database engine."""
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

    return create_async_engine(sqlite_url, echo=True)


async def async_main() -> None:
    """Main async entry point."""
    engine = get_engine()

    # async_sessionmaker: a factory for new AsyncSession objects.
    # expire_on_commit - don't expire objects after transaction commit
    # Kept for future use when document loading is implemented
    _ = async_sessionmaker(engine, expire_on_commit=False)

    # Create all tables from the models package
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    logger.info("Database tables created")

    # TODO: Update document loading to work with new schema
    # The new schema requires:
    # 1. Create SourceType records
    # 2. Create Source records
    # 3. Create DocumentTable + TextDocumentTable pairs
    #
    # Example:
    # source_type = SourceTypeTable(slug="file")
    # source = SourceTable(source_type_id=source_type.id)
    # doc = DocumentTable(type="text_document", source_id=source.id)
    # text_doc = TextDocumentTable(id=doc.id, text="...")

    logger.info("Preparing document batch (currently disabled - schema updated)")
    h = DocumentHandler(Path.home())
    for _ in h.get_documents():
        pass  # Handler now just logs, doesn't yield documents

    logger.info("Clean up session")
    await engine.dispose()


def main() -> None:
    """Sync entry point."""
    asyncio.run(async_main())

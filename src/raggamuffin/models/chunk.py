"""Chunk table for document chunking/RAG."""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import LargeBinary
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from raggamuffin.models.document import DocumentTable


class ChunkTable(SQLModel, table=True):
    """Chunk of a document for embedding/retrieval."""

    __tablename__ = "chunk"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    document_id: uuid.UUID = Field(foreign_key="document.id", index=True)

    # Chunk-specific fields
    sequence: int = Field(default=0, index=True)  # Order within document
    start_offset: Optional[int] = Field(default=None)  # Character offset
    end_offset: Optional[int] = Field(default=None)
    text: str

    # Embeddings for this chunk (use sa_type to avoid shared Column instances)
    sparse_embedding: Optional[bytes] = Field(default=None, sa_type=LargeBinary)
    dense_embedding: Optional[bytes] = Field(default=None, sa_type=LargeBinary)

    # Relationship
    document: "DocumentTable" = Relationship(back_populates="chunks")

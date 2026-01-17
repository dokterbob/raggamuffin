"""Document hierarchy: Document, TextDocument, and Image tables.

Uses Joined Table Inheritance - a base `document` table with joined tables
for type-specific fields (text_document, image).
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON, LargeBinary
from sqlmodel import Field, Relationship, SQLModel

from raggamuffin.models.base import DatedMixin, EmbeddableMixin

if TYPE_CHECKING:
    from raggamuffin.models.chunk import ChunkTable
    from raggamuffin.models.document_set import DocumentSetDocumentLink
    from raggamuffin.models.entity import EntityTable
    from raggamuffin.models.reference import SourceTable


# ============================================================================
# Link Tables
# ============================================================================


class DocumentCreatorLink(SQLModel, table=True):
    """Link table: Document <-> Entity (creators, many-to-many)."""

    __tablename__ = "document_creator_link"

    document_id: uuid.UUID = Field(foreign_key="document.id", primary_key=True)
    creator_id: uuid.UUID = Field(foreign_key="entity.id", primary_key=True)

    document: "DocumentTable" = Relationship(back_populates="creator_links")
    creator: "EntityTable" = Relationship(back_populates="created_documents")


# ============================================================================
# Document Tables (Joined Table Inheritance)
# ============================================================================


class DocumentTable(DatedMixin, EmbeddableMixin, SQLModel, table=True):
    """Base document table.

    Type-specific data is stored in joined tables (text_document, image).
    """

    __tablename__ = "document"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    type: str = Field(index=True)  # Discriminator: "text_document", "image", etc.
    source_id: uuid.UUID = Field(foreign_key="source.id", index=True)
    metadata_json: Optional[str] = Field(default=None, sa_type=JSON)

    # Relationships
    source: "SourceTable" = Relationship(back_populates="documents")
    creator_links: list[DocumentCreatorLink] = Relationship(back_populates="document")
    chunks: list["ChunkTable"] = Relationship(back_populates="document")
    document_set_links: list["DocumentSetDocumentLink"] = Relationship(
        back_populates="document"
    )

    # Joined table relationships
    text_document: Optional["TextDocumentTable"] = Relationship(
        back_populates="document",
        sa_relationship_kwargs={"uselist": False},
    )
    image: Optional["ImageTable"] = Relationship(
        back_populates="document",
        sa_relationship_kwargs={"uselist": False},
    )

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "document",
    }


class TextDocumentTable(SQLModel, table=True):
    """Joined table for text documents."""

    __tablename__ = "text_document"

    id: uuid.UUID = Field(foreign_key="document.id", primary_key=True)
    text: str

    # Back-reference to base document
    document: DocumentTable = Relationship(
        back_populates="text_document",
        sa_relationship_kwargs={"uselist": False},
    )

    # Event type joined tables
    message: Optional["MessageTable"] = Relationship(
        back_populates="text_document",
        sa_relationship_kwargs={"uselist": False},
    )
    meeting: Optional["MeetingTable"] = Relationship(
        back_populates="text_document",
        sa_relationship_kwargs={"uselist": False},
    )


class ImageTable(SQLModel, table=True):
    """Joined table for images."""

    __tablename__ = "image"

    id: uuid.UUID = Field(foreign_key="document.id", primary_key=True)
    width: Optional[int] = Field(default=None)
    height: Optional[int] = Field(default=None)
    data: bytes = Field(sa_type=LargeBinary)

    # Back-reference to base document
    document: DocumentTable = Relationship(
        back_populates="image",
        sa_relationship_kwargs={"uselist": False},
    )


# Forward references for event types (defined in event.py)
if TYPE_CHECKING:
    from raggamuffin.models.event import MeetingTable, MessageTable

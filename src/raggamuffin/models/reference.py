"""Reference types: SourceType and Source tables."""

import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from raggamuffin.models.document import DocumentTable
    from raggamuffin.models.entity import EntitySourceLink


class SourceTypeTable(SQLModel, table=True):
    """Database table for source types."""

    __tablename__ = "source_type"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    slug: str = Field(index=True, unique=True)

    # Relationships
    sources: list["SourceTable"] = Relationship(back_populates="source_type")


class SourceTable(SQLModel, table=True):
    """Database table for sources."""

    __tablename__ = "source"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    source_type_id: uuid.UUID = Field(foreign_key="source_type.id", index=True)

    # Relationships
    source_type: SourceTypeTable = Relationship(back_populates="sources")
    entity_links: list["EntitySourceLink"] = Relationship(back_populates="source")
    documents: list["DocumentTable"] = Relationship(back_populates="source")

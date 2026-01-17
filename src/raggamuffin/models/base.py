"""Base mixins for SQLModel persistence classes.

These mixins provide common fields shared across multiple table types.
They should be mixed into SQLModel classes with `table=True`.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import LargeBinary
from sqlmodel import Field, SQLModel


class DatedMixin(SQLModel):
    """Mixin for created/modified timestamps."""

    created: Optional[datetime] = Field(default=None)
    modified: Optional[datetime] = Field(default=None)


class EmbeddableMixin(SQLModel):
    """Mixin for embedding storage as BLOBs.

    Embeddings are stored as raw bytes. Use numpy's tobytes()/frombuffer()
    for serialization.
    """

    # Use sa_type instead of sa_column to avoid shared Column instances
    sparse_embedding: Optional[bytes] = Field(default=None, sa_type=LargeBinary)
    dense_embedding: Optional[bytes] = Field(default=None, sa_type=LargeBinary)
    summary: Optional[str] = Field(default=None)


class EventMixin(SQLModel):
    """Mixin for event types with a date."""

    event_date: datetime = Field(index=True)

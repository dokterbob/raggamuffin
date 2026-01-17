"""Document set hierarchy: DocumentSet and Conversation tables.

Uses Single Table Inheritance - DocumentSet and Conversation share the
`document_set` table with a `type` discriminator column.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from raggamuffin.models.document import DocumentTable


# ============================================================================
# Link Tables
# ============================================================================


class DocumentSetDocumentLink(SQLModel, table=True):
    """Link table: DocumentSet <-> Document (many-to-many)."""

    __tablename__ = "document_set_document_link"

    document_set_id: uuid.UUID = Field(foreign_key="document_set.id", primary_key=True)
    document_id: uuid.UUID = Field(foreign_key="document.id", primary_key=True)
    order: int = Field(default=0)  # Optional: ordering within set

    document_set: "DocumentSetTable" = Relationship(back_populates="document_links")
    document: "DocumentTable" = Relationship(back_populates="document_set_links")


# ============================================================================
# DocumentSet Tables (Single Table Inheritance)
# ============================================================================


class DocumentSetTable(SQLModel, table=True):
    """Document set table using Single Table Inheritance.

    Use type="document_set" for generic sets, type="conversation" for conversations.
    Conversation-specific fields (start_date, end_date) are null for non-conversations.
    """

    __tablename__ = "document_set"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    type: str = Field(index=True, default="document_set")  # Discriminator

    # Conversation-specific fields (null for base DocumentSet)
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)

    # Relationships
    document_links: list[DocumentSetDocumentLink] = Relationship(
        back_populates="document_set"
    )


# Type alias for clarity - Conversation is a DocumentSetTable with type="conversation"
ConversationTable = DocumentSetTable

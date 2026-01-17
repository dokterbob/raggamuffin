"""Event types: Message and Meeting tables.

Message and Meeting are event types that extend TextDocument.
They use joined table inheritance from text_document.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from raggamuffin.models.base import EventMixin

if TYPE_CHECKING:
    from raggamuffin.models.document import TextDocumentTable
    from raggamuffin.models.entity import EntityTable


# ============================================================================
# Link Tables
# ============================================================================


class MeetingParticipantLink(SQLModel, table=True):
    """Link table: Meeting <-> Entity (participants, many-to-many)."""

    __tablename__ = "meeting_participant_link"

    meeting_id: uuid.UUID = Field(foreign_key="meeting.id", primary_key=True)
    participant_id: uuid.UUID = Field(foreign_key="entity.id", primary_key=True)

    meeting: "MeetingTable" = Relationship(back_populates="participant_links")
    participant: "EntityTable" = Relationship(back_populates="meeting_participations")


# ============================================================================
# Event Tables (Joined from TextDocument)
# ============================================================================


class MessageTable(EventMixin, SQLModel, table=True):
    """Message event - joined table extending text_document."""

    __tablename__ = "message"

    id: uuid.UUID = Field(foreign_key="text_document.id", primary_key=True)
    sender_id: uuid.UUID = Field(foreign_key="entity.id", index=True)
    recipient_id: uuid.UUID = Field(foreign_key="entity.id", index=True)
    content: str

    # Relationships
    text_document: "TextDocumentTable" = Relationship(
        back_populates="message",
        sa_relationship_kwargs={"uselist": False},
    )
    sender: "EntityTable" = Relationship(
        back_populates="sent_messages",
        sa_relationship_kwargs={"foreign_keys": "[MessageTable.sender_id]"},
    )
    recipient: "EntityTable" = Relationship(
        back_populates="received_messages",
        sa_relationship_kwargs={"foreign_keys": "[MessageTable.recipient_id]"},
    )


class MeetingTable(EventMixin, SQLModel, table=True):
    """Meeting event - joined table extending text_document."""

    __tablename__ = "meeting"

    id: uuid.UUID = Field(foreign_key="text_document.id", primary_key=True)
    transcript: Optional[str] = Field(default=None)

    # Relationships
    text_document: "TextDocumentTable" = Relationship(
        back_populates="meeting",
        sa_relationship_kwargs={"uselist": False},
    )
    participant_links: list[MeetingParticipantLink] = Relationship(
        back_populates="meeting"
    )

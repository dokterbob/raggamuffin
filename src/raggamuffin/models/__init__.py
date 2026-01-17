"""SQLModel persistence layer.

This package contains SQLModel table definitions that correspond to
the Pydantic domain types in types.py.

Re-exports all models for convenient imports:
    from raggamuffin.models import DocumentTable, PersonTable, ...
"""

# Base mixins
from raggamuffin.models.base import DatedMixin, EmbeddableMixin, EventMixin

# Chunk
from raggamuffin.models.chunk import ChunkTable

# Document hierarchy
from raggamuffin.models.document import (
    DocumentCreatorLink,
    DocumentTable,
    ImageTable,
    TextDocumentTable,
)

# Document sets
from raggamuffin.models.document_set import (
    ConversationTable,
    DocumentSetDocumentLink,
    DocumentSetTable,
)

# Entity hierarchy
from raggamuffin.models.entity import (
    EntitySourceLink,
    EntityTable,
    OrganizationHierarchyLink,
    OrganizationPersonLink,
    OrganizationTable,
    PersonTable,
)

# Event types
from raggamuffin.models.event import (
    MeetingParticipantLink,
    MeetingTable,
    MessageTable,
)

# Reference types
from raggamuffin.models.reference import SourceTable, SourceTypeTable

__all__ = [
    # Mixins
    "DatedMixin",
    "EmbeddableMixin",
    "EventMixin",
    # Reference
    "SourceTypeTable",
    "SourceTable",
    # Entity
    "EntityTable",
    "PersonTable",
    "OrganizationTable",
    "EntitySourceLink",
    "OrganizationPersonLink",
    "OrganizationHierarchyLink",
    # Document
    "DocumentTable",
    "TextDocumentTable",
    "ImageTable",
    "DocumentCreatorLink",
    # Chunk
    "ChunkTable",
    # Event
    "MessageTable",
    "MeetingTable",
    "MeetingParticipantLink",
    # DocumentSet
    "DocumentSetTable",
    "ConversationTable",
    "DocumentSetDocumentLink",
]

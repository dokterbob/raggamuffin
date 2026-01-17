"""Domain types for the raggamuffin application.

This module defines Pydantic models for the API/domain layer.
SQLModel persistence classes in models/ extend these types.
"""

import abc
import uuid
from datetime import datetime
from typing import Any, ClassVar, Dict, Optional

import jinja2
import numpy as np
from pydantic import BaseModel, ConfigDict

jinja_env = jinja2.Environment(
    loader=jinja2.PackageLoader("raggamuffin"),
    autoescape=True,
    enable_async=True,
)

# Type aliases
Embedding = np.ndarray
MetaData = Dict[str, str | int | float]


# ============================================================================
# Behavior Mixins
# ============================================================================


class DatedMixin(BaseModel):
    """Mixin for created/modified timestamps."""

    created: Optional[datetime] = None
    modified: Optional[datetime] = None


class EmbeddableMixin(BaseModel):
    """Mixin for sparse/dense embeddings."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    sparse_embedding: Optional[Embedding] = None
    dense_embedding: Optional[Embedding] = None

    def generate_embeddings(self) -> None:
        raise NotImplementedError


class TextEmbeddableMixin(BaseModel):
    """Mixin for text content that can be embedded and summarized."""

    text: str
    summary: Optional[str] = None

    def get_text(self) -> str:
        return self.text

    def get_context(self) -> Dict[str, Any]:
        return dict(self)

    def generate_summary(self) -> None:
        raise NotImplementedError


class EventMixin(BaseModel):
    """Mixin for event types with a date."""

    event_date: datetime


# ============================================================================
# Reference Types
# ============================================================================


class SourceType(BaseModel):
    """Type/category of a source."""

    uuid: uuid.UUID
    slug: str


class Source(BaseModel):
    """A reference to a source of data."""

    uuid: uuid.UUID
    type: SourceType


# ============================================================================
# Entity Types
# ============================================================================


class Entity(DatedMixin, EmbeddableMixin, BaseModel, abc.ABC):
    """Abstract base for Person and Organization."""

    uuid: uuid.UUID
    name: str
    sources: set[Source] = set()


class Person(Entity):
    """A person entity."""

    pass


class Organization(Entity):
    """An organization entity with hierarchical relationships."""

    persons: set[Person] = set()
    parents: "set[Organization]" = set()
    children: "set[Organization]" = set()


# ============================================================================
# Document Types
# ============================================================================


class Document(DatedMixin, EmbeddableMixin, BaseModel, abc.ABC):
    """Abstract base for all documents."""

    uuid: uuid.UUID
    source: Source
    metadata: MetaData = {}
    creators: set[Person] = set()


class TextDocument(Document, TextEmbeddableMixin):
    """A text-based document."""

    template: ClassVar[jinja2.Template] = jinja_env.get_template("text_document.jinja")


class Image(Document):
    """An image document."""

    width: Optional[int] = None
    height: Optional[int] = None
    data: bytes

    template: ClassVar[jinja2.Template] = jinja_env.get_template("image.jinja")


# ============================================================================
# Event Types (compose mixins to avoid diamond inheritance)
# ============================================================================


class Message(DatedMixin, EmbeddableMixin, TextEmbeddableMixin, EventMixin, BaseModel):
    """A message event - composes mixins instead of diamond inheritance."""

    uuid: uuid.UUID
    source: Source
    metadata: MetaData = {}
    creators: set[Person] = set()
    sender: Person
    recipient: Person
    content: str

    template: ClassVar[jinja2.Template] = jinja_env.get_template("message.jinja")

    def __str__(self) -> str:
        return f"Message from {self.sender} to {self.recipient} on {self.event_date}"


class Meeting(DatedMixin, EmbeddableMixin, TextEmbeddableMixin, EventMixin, BaseModel):
    """A meeting event - composes mixins instead of diamond inheritance."""

    uuid: uuid.UUID
    source: Source
    metadata: MetaData = {}
    creators: set[Person] = set()
    transcript: Optional[str] = None
    participants: set[Person] = set()

    template: ClassVar[jinja2.Template] = jinja_env.get_template("meeting.jinja")


# ============================================================================
# Document Collections
# ============================================================================


class DocumentSet(BaseModel, abc.ABC):
    """Abstract base for document collections."""

    uuid: uuid.UUID
    documents: set[Document] = set()

    template: ClassVar[jinja2.Template] = jinja_env.get_template("document_set.jinja")


class Conversation(DocumentSet):
    """A conversation is a time-bounded document set."""

    start_date: datetime
    end_date: datetime

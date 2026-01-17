import abc
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

import jinja2
import numpy as np
from pydantic import BaseModel

jinja_env = jinja2.Environment(
    loader=jinja2.PackageLoader("raggamuffin"),
    autoescape=True,
    enable_async=True,
)


class Dated(BaseModel, abc.ABC):
    created: Optional[datetime]
    modified: Optional[datetime]


Embedding = np.array[np.number]


class Embeddable(BaseModel, abc.ABC):
    sparse_embedding = Optional[Embedding]
    dense_embedding = Optional[Embedding]

    @abc.abstractmethod
    def generate_embeddings(self):
        pass


class TextEmbeddable(Embeddable, abc.ABC):
    template: jinja2.Template

    summary: Optional[str]

    def get_text(self) -> str:
        context = self.get_context()
        return self.template.render(context)

    def get_context(self) -> Dict[str, Any]:
        return dict(self)

    def generate_embeddings(self):
        raise NotImplementedError

    def generate_summary(self):
        raise NotImplementedError


class SourceType(BaseModel):
    uuid: uuid.UUID
    slug: str


class Source(BaseModel):
    uuid: uuid.UUID
    type: SourceType


class Entity(Dated, Embeddable, abc.ABC):
    uuid: uuid.UUID
    name: str
    sources: set[Source]


class Person(Entity):
    pass


class Organization(Entity):
    persons: set[Person]
    parents: "set[Organization]"
    children: "set[Organization]"


MetaData = Dict[str, str | int | float]


class Document(Dated, Embeddable, abc.ABC):
    uuid: uuid.UUID
    source: Source
    metadata: MetaData
    creators: set[Person]


class TextDocument(Document, TextEmbeddable):
    text: str

    def get_text(self) -> str:
        return self.text

    template = jinja_env.get_template("text_document.jinja")


class Image(Document):
    width: Optional[int]
    height: Optional[int]
    data: bytes

    template = jinja_env.get_template("image.jinja")

    def generate_embeddings(self):
        raise NotImplementedError


class Event(Dated, abc.ABC):
    date: datetime


class Message(Event, TextDocument, TextEmbeddable):
    sender: Person
    recipient: Person
    content: str

    def __str__(self) -> str:
        return f"Message from {self.sender} to {self.recipient} on {self.date}"

    template = jinja_env.get_template("message.jinja")


class Meeting(Event, Document, TextEmbeddable):
    transcript: Optional[str]
    participants: set[Person]

    template = jinja_env.get_template("meeting.jinja")


class DocumentSet(BaseModel, abc.ABC):
    uuid: uuid.UUID
    set: Document

    template = jinja_env.get_template("document_set.jinja")


class Conversation(DocumentSet):
    start_date: datetime
    end_date: datetime
    """Start and end creation time"""

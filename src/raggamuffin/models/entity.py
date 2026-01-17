"""Entity hierarchy: Person and Organization tables.

Uses Single Table Inheritance - Person and Organization share the `entity` table
with a `type` discriminator column.
"""

import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from raggamuffin.models.base import DatedMixin, EmbeddableMixin

if TYPE_CHECKING:
    from raggamuffin.models.document import DocumentCreatorLink
    from raggamuffin.models.event import MeetingParticipantLink, MessageTable
    from raggamuffin.models.reference import SourceTable


# ============================================================================
# Link Tables
# ============================================================================


class EntitySourceLink(SQLModel, table=True):
    """Link table: Entity <-> Source (many-to-many)."""

    __tablename__ = "entity_source_link"

    entity_id: uuid.UUID = Field(foreign_key="entity.id", primary_key=True)
    source_id: uuid.UUID = Field(foreign_key="source.id", primary_key=True)

    entity: "EntityTable" = Relationship(back_populates="source_links")
    source: "SourceTable" = Relationship(back_populates="entity_links")


class OrganizationPersonLink(SQLModel, table=True):
    """Link table: Organization <-> Person (many-to-many)."""

    __tablename__ = "organization_person_link"

    organization_id: uuid.UUID = Field(foreign_key="entity.id", primary_key=True)
    person_id: uuid.UUID = Field(foreign_key="entity.id", primary_key=True)

    organization: "EntityTable" = Relationship(
        back_populates="organization_persons",
        sa_relationship_kwargs={
            "foreign_keys": "[OrganizationPersonLink.organization_id]"
        },
    )
    person: "EntityTable" = Relationship(
        back_populates="person_organizations",
        sa_relationship_kwargs={"foreign_keys": "[OrganizationPersonLink.person_id]"},
    )


class OrganizationHierarchyLink(SQLModel, table=True):
    """Link table: Organization parent <-> child (self-referential many-to-many)."""

    __tablename__ = "organization_hierarchy_link"

    parent_id: uuid.UUID = Field(foreign_key="entity.id", primary_key=True)
    child_id: uuid.UUID = Field(foreign_key="entity.id", primary_key=True)

    parent: "EntityTable" = Relationship(
        back_populates="child_links",
        sa_relationship_kwargs={
            "foreign_keys": "[OrganizationHierarchyLink.parent_id]"
        },
    )
    child: "EntityTable" = Relationship(
        back_populates="parent_links",
        sa_relationship_kwargs={"foreign_keys": "[OrganizationHierarchyLink.child_id]"},
    )


# ============================================================================
# Entity Tables (Single Table Inheritance)
# ============================================================================


class EntityTable(DatedMixin, EmbeddableMixin, SQLModel, table=True):
    """Entity table using Single Table Inheritance.

    Use type="person" for people, type="organization" for organizations.
    Organization-specific relationships work for both but are typically
    empty for Person entities.
    """

    __tablename__ = "entity"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    type: str = Field(index=True, default="entity")  # Discriminator
    name: str = Field(index=True)

    # Relationships
    source_links: list[EntitySourceLink] = Relationship(back_populates="entity")

    # Organization-specific relationships (empty for Person)
    organization_persons: list[OrganizationPersonLink] = Relationship(
        back_populates="organization",
        sa_relationship_kwargs={
            "foreign_keys": "[OrganizationPersonLink.organization_id]"
        },
    )
    person_organizations: list[OrganizationPersonLink] = Relationship(
        back_populates="person",
        sa_relationship_kwargs={"foreign_keys": "[OrganizationPersonLink.person_id]"},
    )
    parent_links: list[OrganizationHierarchyLink] = Relationship(
        back_populates="child",
        sa_relationship_kwargs={"foreign_keys": "[OrganizationHierarchyLink.child_id]"},
    )
    child_links: list[OrganizationHierarchyLink] = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={
            "foreign_keys": "[OrganizationHierarchyLink.parent_id]"
        },
    )

    # Document relationships
    created_documents: list["DocumentCreatorLink"] = Relationship(
        back_populates="creator"
    )
    sent_messages: list["MessageTable"] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs={"foreign_keys": "[MessageTable.sender_id]"},
    )
    received_messages: list["MessageTable"] = Relationship(
        back_populates="recipient",
        sa_relationship_kwargs={"foreign_keys": "[MessageTable.recipient_id]"},
    )
    meeting_participations: list["MeetingParticipantLink"] = Relationship(
        back_populates="participant"
    )


# Type aliases for clarity - Person and Organization are EntityTable with type discriminator
PersonTable = EntityTable
OrganizationTable = EntityTable

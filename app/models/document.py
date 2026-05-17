from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.monitor_assignment import MonitorAssignment

class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: int | None = Field(default=None, primary_key=True)
    original_filename: str = Field(nullable=False)
    content_type: str = Field(nullable=False)
    extension: str = Field(nullable=False)
    size_bytes: int = Field(nullable=False)
    assignment_id: int = Field(foreign_key="monitor_assignments.id")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    assignment: "MonitorAssignment" = Relationship(back_populates="documents")
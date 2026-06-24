from datetime import datetime, timezone
from typing import TYPE_CHECKING
from beanie import Document, Link
from pydantic import Field

if TYPE_CHECKING:
    from app.models.monitor_assignment import MonitorAssignment


class DocumentMetadata(Document):
    original_filename: str
    content_type: str
    extension: str
    size_bytes: int

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    assignment: Link["MonitorAssignment"]

    class Settings:
        name = "documents_metadata"

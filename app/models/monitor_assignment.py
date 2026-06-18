from enum import unique

from beanie import Document, Link
from typing import TYPE_CHECKING
from pymongo import IndexModel, ASCENDING
from pydantic import Field

if TYPE_CHECKING:
    from app.models.monitor import Monitor
    from app.models.classroom import Classroom
    from app.models.feedback import Feedback
    from app.models.document_metadata import DocumentMetadata

class MonitorAssignment(Document):
    weekly_hours: int

    monitor: Link["Monitor"]
    classroom: Link["Classroom"]
    feedbacks: list[Link["Feedback"]] = Field(default_factory=list)
    documents: list[Link["Document"]] = Field(default_factory=list)

    class Settings:
        name = "monitor_assignments"

        indexes = [
            IndexModel(
                [("monitor", ASCENDING), ("classroom", ASCENDING)],
                unique=True,
                name="unique_monitor_classroom"
            ),
        ]
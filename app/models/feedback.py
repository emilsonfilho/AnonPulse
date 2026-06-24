from datetime import datetime, timezone
from typing import TYPE_CHECKING, Annotated
from pydantic import Field
from beanie import Document, Link
from app.core.enums import MessageType

if TYPE_CHECKING:
    from app.models.monitor_assignment import MonitorAssignment
    from app.models.enrollment import Enrollment


class Feedback(Document):
    registration: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    text: str
    rating: int

    assignment: Link["MonitorAssignment"]
    type: MessageType

    class Settings:
        name = "feedbacks"
        indexes = [("text", "text")]

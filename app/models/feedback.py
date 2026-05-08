from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.monitor_assignment import MonitorAssignment
    from app.models.enrollment import Enrollment
    from app.models.feedback_type import FeedbackType

class Feedback(SQLModel, table=True):
    __tablename__ = "feedbacks"

    id: int | None = Field(default=None, primary_key=True)
    assignment_id: int = Field(foreign_key="monitor_assignments.id")
    enrollment_id: int = Field(foreign_key="enrollments.id")
    type_id: int = Field(foreign_key="feedback_types.id")
    data_submissao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    texto_feedback: str
    rating: int | None

    assignment: "MonitorAssignment" =  Relationship(back_populates="feedbacks")
    enrollment: "Enrollment" = Relationship(back_populates="feedbacks")
    type: "FeedbackType" = Relationship(back_populates="feedbacks")


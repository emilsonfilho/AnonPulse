from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.monitor import Monitor
    from app.models.classroom import Classroom
    from app.models.feedback import Feedback

class MonitorAssignment(SQLModel, table=True):
    __tablename__ = "monitor_assignments"

    id: int | None = Field(default=None, primary_key=True)
    weekly_hours: int
    monitor_id: int = Field(foreign_key="monitors.id")
    classroom_id: int = Field(foreign_key="classrooms.id")

    monitor: "Monitor" = Relationship(back_populates="assignments")
    classroom: "Classroom" = Relationship(back_populates="assignments")
    feedbacks: list["Feedback"] = Relationship(back_populates="assignment")



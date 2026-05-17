from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.monitor import Monitor
    from app.models.classroom import Classroom
    from app.models.feedback import Feedback
    from app.models.document import Document

class MonitorAssignment(SQLModel, table=True):
    __tablename__ = "monitor_assignments"
    __table_args__ = (
        UniqueConstraint("monitor_registration", "classroom_cod", name="unique_monitor_classroom"),
    )

    id: int | None = Field(default=None, primary_key=True)
    weekly_hours: int
    monitor_registration: str = Field(foreign_key="monitors.registration")
    classroom_cod: str = Field(foreign_key="classrooms.cod")

    monitor: "Monitor" = Relationship(back_populates="assignments")
    classroom: "Classroom" = Relationship(back_populates="assignments")
    feedbacks: list["Feedback"] = Relationship(back_populates="assignment")
    documents: list["Document"] = Relationship(back_populates="assignment")



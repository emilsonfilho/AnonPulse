from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models.classroom import Classroom
    from app.models.feedback import Feedback

class Enrollment(SQLModel, table=True):
    __tablename__ = "enrollments"

    id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="students.id")
    classroom_cod: str = Field(foreign_key="classrooms.cod")
    is_active: bool = Field(default=True)
    enrolled_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    student: "Student" = Relationship(back_populates="enrollments")
    classroom: "Classroom" = Relationship(back_populates="enrollments")
    feedbacks: list["Feedback"] = Relationship(back_populates="enrollment")
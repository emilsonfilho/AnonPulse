from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models.classroom import Classroom

class Enrollment(SQLModel, table=True):
    __tablename__ = "enrollments"

    id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="students.id")
    classroom_id: int = Field(foreign_key="classrooms.id")
    status: str
    enrolled_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    student: "Student" = Relationship(back_populates="enrollments")
    classroom: "Classroom" = Relationship(back_populates="enrollments")
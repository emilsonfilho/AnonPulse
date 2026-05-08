from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.subject import Subject
    from app.models.professor import Professor
    from app.models.enrollment import Enrollment
    from app.models.monitor_assignment import MonitorAssignment

class Classroom(SQLModel, table=True):
    __tablename__ = "classrooms"

    id: int | None = Field(default=None, primary_key=True)
    semester: str
    subject_id: int = Field(foreign_key="subjects.id")
    professor_id: int = Field(foreign_key="professors.id")

    subject: "Subject" = Relationship(back_populates="classrooms")
    professor: "Professor" = Relationship(back_populates="classrooms")
    enrollments: list["Enrollment"] = Relationship(back_populates="classroom")
    assignments: list["MonitorAssignment"] = Relationship(back_populates="classroom")

from typing import TYPE_CHECKING, Annotated
from beanie import Document, Link, Indexed
from pydantic import Field

if TYPE_CHECKING:
    from app.models.subject import Subject
    from app.models.professor import Professor
    from app.models.enrollment import Enrollment
    from app.models.monitor_assignment import MonitorAssignment


class Classroom(Document):

    cod: Annotated[str, Indexed(unique=True)]

    subject: Link["Subject"]
    professor: Link["Professor"]
    enrollments: list[Link["Enrollment"]] = Field(default_factory=list)
    assignments: list[Link["MonitorAssignment"]] = Field(default_factory=list)

    class Settings:
        name = "classrooms"
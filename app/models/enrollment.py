from datetime import datetime, timezone
from typing import TYPE_CHECKING
from pydantic import Field
from beanie import Document, Link
from pymongo import IndexModel, ASCENDING

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models.classroom import Classroom


class Enrollment(Document):
    is_active: bool = Field(default=True)
    enrolled_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    student: Link["Student"]
    classroom: Link["Classroom"]

    class Settings:
        name = "enrollments"

        indexes = [
            IndexModel(
                [("student", ASCENDING), ("classroom", ASCENDING)],
                unique=True,
                name="unique_student_classroom",
            )
        ]

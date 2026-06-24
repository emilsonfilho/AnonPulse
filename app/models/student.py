from beanie import Document, Link, Indexed
from typing import TYPE_CHECKING, Annotated
from pydantic import Field

if TYPE_CHECKING:
    from app.models.enrollment import Enrollment


class Student(Document):
    registration: Annotated[str, Indexed(unique=True)]

    enrollments: list[Link["Enrollment"]] = Field(default_factory=list)

    class Settings:
        name = "students"

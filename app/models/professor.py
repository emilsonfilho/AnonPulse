from beanie import Document, Link
from typing import TYPE_CHECKING
from pydantic import Field

if TYPE_CHECKING:
    from app.models.classroom import Classroom

class Professor(Document):
    name: str
    email: str

    classrooms: list[Link["Classroom"]] = Field(default_factory=list)

    class Settings:
        name = "professors"
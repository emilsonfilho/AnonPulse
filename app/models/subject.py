from typing import TYPE_CHECKING, Annotated
from beanie import Document, Link, Indexed
from pydantic import Field

if TYPE_CHECKING:
    from app.models.classroom import Classroom

class Subject(Document):
    cod: Annotated[str, Indexed(unique=True)]
    name: str

    classrooms: list[Link["Classroom"]]  = Field(default_factory=list)

    class Settings:
        name = "subjects"
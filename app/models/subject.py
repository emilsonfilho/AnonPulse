from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.classroom import Classroom

class Subject(SQLModel, table=True):
    __tablename__ = "subjects"

    cod: str = Field(primary_key=True)
    name: str

    classrooms: list["Classroom"] = Relationship(back_populates="subject")
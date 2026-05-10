from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.classroom import Classroom

class Professor(SQLModel, table=True):
    __tablename__ = "professors"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str

    classrooms: list["Classroom"] = Relationship(back_populates="professor")
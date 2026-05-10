from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.enrollment import Enrollment

class Student(SQLModel, table=True):
    __tablename__ = "students"

    id: int | None = Field(default=None, primary_key=True)
    registration: str = Field(unique=True)

    enrollments: list["Enrollment"] = Relationship(back_populates="student")
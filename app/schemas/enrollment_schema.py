from typing import Annotated, Any

from beanie import PydanticObjectId
from pydantic import BaseModel, Field, model_validator
from datetime import datetime

from app.schemas.orm_base_schema import ORMBaseSchema


class EnrollmentBase(BaseModel):
    is_active: Annotated[bool, Field(default=True)]


class CreateEnrollmentRequest(BaseModel):
    classroom_cod: Annotated[
        str, Field(min_length=3, max_length=10, description="Código da turma")
    ]

    student_id: Annotated[PydanticObjectId, Field(description="ID do estudante")]


class UpdateEnrollmentRequest(BaseModel):
    is_active: Annotated[bool | None, Field(default=None)]


class EnrollmentResponse(EnrollmentBase, ORMBaseSchema):
    id: PydanticObjectId
    enrolled_at: datetime
    classroom_cod: str
    student_id: PydanticObjectId

    @model_validator(mode="before")
    @classmethod
    def extract_links(cls, data: Any) -> Any:
        if isinstance(data, dict):
            res = data.copy()
            student = res.get("student")
            classroom = res.get("classroom")

            if student:
                if isinstance(student, dict):
                    res["student_id"] = student.get("id") or student.get("_id") or student.get("$id")
                else:
                    ref = getattr(student, "ref", None)
                    res["student_id"] = getattr(student, "id", getattr(ref, "id", None))

            if classroom:
                if isinstance(classroom, dict):
                    res["classroom_cod"] = classroom.get("cod")
                else:
                    res["classroom_cod"] = getattr(classroom, "cod", None)

            return res

        if hasattr(data, "model_dump"):
            res = data.model_dump()
        elif hasattr(data, "__dict__"):
            res = data.__dict__.copy()
        else:
            res = dict(data)

        if hasattr(data, "id") and data.id:
            res["id"] = data.id

        student = getattr(data, "student", None)
        if student:
            ref = getattr(student, "ref", None)
            res["student_id"] = getattr(student, "id", getattr(ref, "id", None))

        classroom = getattr(data, "classroom", None)
        if classroom:
            res["classroom_cod"] = getattr(classroom, "cod", None)

        return data
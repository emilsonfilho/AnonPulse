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
        if not isinstance(data, dict) and hasattr(data, "student") and hasattr(data.student, "classroom"):
            return {
                "id": data.id,
                "is_active": data.is_active,
                "enrolled_at": data.enrolled_at,
                "classroom_cod": data.student.classroom.cod if data.classroom else None,
                "student_id": data.student.id if data.student else None,
            }

        if hasattr(data, "student") and hasattr(data, "classroom"):
            return {
                "id": data.id,
                "is_active": data.is_active,
                "enrolled_at": data.enrolled_at,
                "classroom_cod": data.classroom.cod if data.classroom else None,
                "student_id": data.student.id if data.student else None,
            }
        return data
        return data
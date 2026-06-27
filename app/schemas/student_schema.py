from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field
from beanie import PydanticObjectId

from app.schemas.enrollment_schema import EnrollmentResponse
from app.schemas.orm_base_schema import ORMBaseSchema


class StudentBase(BaseModel):
    registration: Annotated[
        str,
        Field(
            min_length=64,
            max_length=64,
            description="Matrícula do aluno criptografado em SHA-256.",
        ),
    ]


class CreateStudentRequest(BaseModel):
    registration: Annotated[
        str, Field(min_length=5, max_length=10, description="Matrícula do aluno.")
    ]


class UpdateStudentRequest(CreateStudentRequest):
    pass


class StudentResponse(StudentBase, ORMBaseSchema):
    id: PydanticObjectId | None

    enrollments: list[EnrollmentResponse]

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

from typing import Annotated

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from app.schemas.orm_base_schema import ORMBaseSchema
from app.schemas.professor_schema import ProfessorSelectResponse
from app.schemas.subject_schema import SubjectResponse
from app.schemas.enrollment_schema import EnrollmentResponse

class ClassroomBase(BaseModel):
    cod: Annotated[
        str,
        Field(
            min_length=3,
            max_length=15,
            description="Código de turma",
            examples=["QXD0154", "QXD0155", "QXD0156"],
        ),
    ]

    subject_cod: Annotated[
        str, Field(min_length=7, max_length=15, description="Código de Cadeira")
    ]

    professor_id: Annotated[PydanticObjectId, Field(description="ID do professor")]

class CreateClassroomRequest(ClassroomBase):
    pass

class UpdateClassroomRequest(BaseModel):
    cod: Annotated[
        str | None,
        Field(default=None, min_length=3, max_length=10, description="Código de turma"),
    ]

class ClassroomResponse(ORMBaseSchema):
    id: PydanticObjectId
    cod: str
    professor: ProfessorSelectResponse | None = None
    subject: SubjectResponse | None = None
    enrollments: list[EnrollmentResponse] | None = None
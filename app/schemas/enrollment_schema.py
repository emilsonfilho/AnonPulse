from typing import Annotated

from beanie import PydanticObjectId
from pydantic import BaseModel, Field
from datetime import datetime

from app.schemas.orm_base_schema import ORMBaseSchema

class EnrollmentBase(BaseModel):
    isActive: Annotated[
        bool,
        Field(
            default=True
        )
    ]

class CreateEnrollmentRequest(BaseModel):
    classroom_cod: Annotated[
        str,
        Field(
            min_length=3,
            max_length=10,
            description="Código da turma"
        )
    ]

    student_id: Annotated[
        PydanticObjectId,
        Field(
            description="ID do estudante"
        )
     ]

class UpdateEnrollmentRequest(BaseModel):
    isActive: Annotated[
        bool | None,
        Field(
            default=None
        )
    ]

class EnrollmentResponse(EnrollmentBase, ORMBaseSchema):
    id: PydanticObjectId
    enrolled_at: datetime
    classroom_cod: str
    student_id: PydanticObjectId
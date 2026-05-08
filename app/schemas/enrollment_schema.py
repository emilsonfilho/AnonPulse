from typing import Annotated
from pydantic import BaseModel, Field
from datetime import datetime

class EnrollmentBase(BaseModel):
    isActive: Annotated[
        bool,
        Field(
            default=True
        )
    ]

class CreateEnrollmentRequest(EnrollmentBase):
    classroom_cod: Annotated[
        str,
        Field(
            min_length=3,
            max_length=3,
            description="Código da turma"
        )
    ]

    student_id: Annotated[
        int,
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

class EnrollmentResponse(EnrollmentBase):
    id: int
    enrolledAt: datetime
    classroom_cod: str
    student_id: int

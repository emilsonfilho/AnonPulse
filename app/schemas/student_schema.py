from typing import Annotated
from pydantic import BaseModel, Field

class StudentBase(BaseModel):
    registration: Annotated[
        str,
        Field(
            min_length=64,
            max_length=64,
            description="Matrícula do aluno criptografado em SHA-256."
        )
    ]

class CreateStudentRequest(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
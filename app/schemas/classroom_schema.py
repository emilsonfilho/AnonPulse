from typing import Annotated
from pydantic import BaseModel, Field


class ClassroomBase(BaseModel):
    cod: Annotated[
        str,
        Field(
            min_length=3,
            max_length=3,
            description="Código de turma",
            examples=["QXD0154", "QXD0155", "QXD0156"],
        ),
    ]


class CreateClassroomRequest(ClassroomBase):
    subject_cod: Annotated[
        str, Field(min_length=9, max_length=9, description="Código de Cadeira")
    ]

    professor_id: Annotated[int, Field(description="ID do professor")]


class UpdateClassroomRequest(BaseModel):
    cod: Annotated[
        str | None,
        Field(default=None, min_length=3, max_length=3, description="Código de turma"),
    ]


class ClassroomResponse(ClassroomBase):
    subject_cod: str
    professor_id: int

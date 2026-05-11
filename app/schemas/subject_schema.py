from typing import Annotated
from pydantic import BaseModel, Field
from .orm_base_schema import ORMBaseSchema

class SubjectBase(BaseModel):
    name: Annotated[
        str,
        Field(
            min_length=5,
            max_length=60,
            description="Nome da matéria."
        )
    ]

    cod: Annotated[
        str,
        Field(
            min_length=6,
            max_length=9,
            description="Código de Cadeira"
        )
    ]

class CreateSubjectRequest(SubjectBase):
    pass

class UpdateSubjectRequest(BaseModel):
    name: Annotated[
        str | None,
        Field(
            default=None,
            min_length=5,
            max_length=60,
            description="Nome da matéria."
        )
    ]

class SubjectResponse(SubjectBase, ORMBaseSchema):
    pass
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr

from app.schemas.orm_base_schema import ORMBaseSchema

class ProfessorBase(BaseModel):
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=100,
            description="Nome do professor."
        )
    ]
    email: EmailStr = Field(
        min_length=5,
        max_length=100,
        description="Email do professor."
    )

class CreateProfessorRequest(ProfessorBase):
    pass

class UpdateProfessorRequest(BaseModel):
    name: Annotated[
        str | None,
        Field(
            default=None,
            min_length=3,
            max_length=100,
            description="Nome do professor."
        )
    ]
    email: EmailStr | None = Field(
        default=None,
        min_length=5,
        max_length=100,
        description="Email do professor."
    )

class ProfessorResponse(ProfessorBase, ORMBaseSchema):
    id: int # acredito eu que sim

class ProfessorSelectResponse(ProfessorBase, ORMBaseSchema):
    pass
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr

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
            min_length=3,
            max_length=100,
            description="Nome do professor."
        )
    ]
    email: EmailStr | None = Field(
        min_length=5,
        max_length=100,
        description="Email do professor."
    )

class ProfessorResponse(ProfessorBase):
    id: int
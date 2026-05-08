from typing import Annotated
from pydantic import BaseModel, Field, EmailStr

class MonitorBase(BaseModel):
    name: Annotated[
        str,
        Field(
            min_length=15,
            max_length=50,
            description="Nome do monitor."
        )
    ]
    registration: Annotated[
        str,
        Field(
            min_length=5,
            max_length=8,
            description="Matrícula do aluno."
        )
    ]
    email: EmailStr = Field(
        min_length=5,
        max_length=100,
        description="E-mail do monitor."
    )

class CreateMonitorRequest(MonitorBase):
    pass

class UpdateMonitorRequest(BaseModel):
    name: Annotated[
        str | None,
        Field(
            default=None,
            min_length=15,
            max_length=50,
            description="Nome do monitor."
        )
    ]
    email: EmailStr | None = Field(
        default=None,
        min_length=5,
        max_length=100,
        description="E-mail do monitor."
    )

class MonitorResponse(MonitorBase):
    pass
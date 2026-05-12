from typing import Annotated
from pydantic import BaseModel, Field, field_validator


def validate_empty_text(value:str) -> str:
    if value is None:
        return value
    elif value.strip() == "":
        raise ValueError("O texto não deve ser vazio")
    else:
        return value

class FeedbackBase(BaseModel):
    text: Annotated[
        str,
        Field(
            min_length=2,
            max_length=5000,
            description="Campo para texto do feedback"
        )
    ]

    rating: Annotated[
        int,
        Field(
            ge= 0,
            le= 5,
            description="Nota de avaliação do monitor"
        )
    ]
  

    @field_validator("text")
    @classmethod
    def validate_fields(cls, v):
        return validate_empty_text(v)
    

class CreateFeedbackRequest(FeedbackBase):
    # Temos que adicionar a matrícula do aluno para que ele dê hash

    assignment_id: Annotated[
        int,
        Field(
            description="ID da tarefa"
        )
    ]

    enrollment_id: Annotated[
        int,
        Field(
            description="ID da matrícula"
        )
    ]

    type_id: Annotated[
        int,
        Field(
            description="ID do tipo de feedback"
        )
    ]



class UpdateFeedbackRequest(BaseModel):
    rating: Annotated[
        int | None, 
        Field(
            default=None,
            ge=0,
            le=5,
            description="Nota de avaliação do monitor"
        )
    ] 

    text: Annotated[
        str | None, 
        Field(
            default=None,
            min_length=2,
            max_length=5000,
            description="Campo para texto do feedback"
        )   
    ]

    @field_validator("text")
    @classmethod
    def validate_fields(cls, v):
        return validate_empty_text(v)
    


class FeedbackResponse(FeedbackBase):
    id: int
    createdAt: str
    assignment_id: int
    enrollment_id: int
    type_id: int
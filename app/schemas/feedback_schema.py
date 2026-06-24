from datetime import datetime
from typing import Annotated

from beanie import PydanticObjectId
from pydantic import BaseModel, Field, field_validator

from app.core.enums import MessageType
from app.schemas.orm_base_schema import ORMBaseSchema
from app.schemas.monitor_assignment_schema import MonitorAssignmentResponse


def validate_empty_text(value: str) -> str:
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
            min_length=2, max_length=5000, description="Campo para texto do feedback"
        ),
    ]

    rating: Annotated[
        int, Field(ge=0, le=5, description="Nota de avaliação do monitor")
    ]

    @field_validator("text")
    @classmethod
    def validate_fields(cls, v):
        return validate_empty_text(v)


class CreateFeedbackRequest(FeedbackBase):
    # Temos que adicionar a matrícula do aluno para que ele dê hash

    assignment: Annotated[PydanticObjectId, Field(description="ID da tarefa")]

    registration: Annotated[str, Field(description="ID da matrícula")]

    type: Annotated[MessageType, Field(description="Tipo do feedback")]


class UpdateFeedbackRequest(BaseModel):
    rating: Annotated[
        int | None,
        Field(default=None, ge=0, le=5, description="Nota de avaliação do monitor"),
    ]

    text: Annotated[
        str | None,
        Field(
            default=None,
            min_length=2,
            max_length=5000,
            description="Campo para texto do feedback",
        ),
    ]

    type: Annotated[MessageType | None, Field(description="Tipo do feedback")]

    @field_validator("text")
    @classmethod
    def validate_fields(cls, v):
        return validate_empty_text(v)


class FeedbackResponse(FeedbackBase, ORMBaseSchema):
    id: PydanticObjectId
    created_at: datetime
    registration: str
    type: MessageType

    assignment: MonitorAssignmentResponse | None = None


class FeedbackSubjectReportResponse(BaseModel):
    subject_name: str
    feedback_count: int

from typing import Annotated

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from app.schemas.orm_base_schema import ORMBaseSchema


class MonitorAssignmentBase(BaseModel):
    weekly_hours: Annotated[
        int,
        Field(
            ge=2,
            le=6,
            description="Número de horas semanais que o monitor irá trabalhar.",
        ),
    ]


class CreateMonitorAssignmentRequest(MonitorAssignmentBase):
    monitor_registration: Annotated[
        str,
        Field(
            min_length=5, max_length=8, description="Número de matrícula do monitor."
        ),
    ]

    classroom_cod: Annotated[
        str, Field(min_length=3, max_length=15, description="Código de turma")
    ]


class UpdateMonitorAssignmentRequest(BaseModel):
    weekly_hours: Annotated[
        int | None,
        Field(
            default=None,
            description="Número de horas semanais que o monitor irá trabalhar.",
        ),
    ]


class AssignmentMonitorNested(ORMBaseSchema):
    registration: str
    name: str


class AssignmentClassroomNested(ORMBaseSchema):
    cod: str


class MonitorAssignmentResponse(MonitorAssignmentBase, ORMBaseSchema):
    id: PydanticObjectId
    monitor: AssignmentMonitorNested
    classroom: AssignmentClassroomNested

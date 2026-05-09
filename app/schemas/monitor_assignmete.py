from typing import Annotated
from pydantic import BaseModel, Field

class MonitorAssignmentBase(BaseModel):
    weekly_hours: Annotated[
        int,
        Field(
            ge= 2,
            le= 6,
            description="Número de horas semanais que o monitor irá trabalhar."
        )
    ]

class CreateMonitorAssignmentRequest(MonitorAssignmentBase):
    monitor_registration_number: Annotated[
        str,
        Field(
            min_length= 5,
            max_length= 8,
            description="Número de matrícula do monitor."
        )
    ]

    classroom_cod: Annotated[
        str,
        Field(
            min_length= 3,
            max_length=3,
            description="Código de turma"
        )
    ]

class UpdateMonitorAssignmentRequest(BaseModel):
    weekly_hours: Annotated[
        int | None,
        Field(
            default=None,
            description="Número de horas semanais que o monitor irá trabalhar."
        )
    ]

class MonitorAssignmentResponse(MonitorAssignmentBase):
    id: int
    monitor_registration_number: str
    classroom_cod: str
    
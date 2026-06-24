from beanie import Document, Indexed, Link
from pydantic import Field
from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from app.models.monitor_assignment import MonitorAssignment


class Monitor(Document):
    registration: Annotated[str, Indexed(unique=True)]
    name: str
    email: str

    assignments: list[Link["MonitorAssignment"]] = Field(default_factory=list)

    class Settings:
        name = "monitors"

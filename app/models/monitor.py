from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.monitor_assignment import MonitorAssignment

class Monitor(SQLModel, table=True):
    __tablename__ = "monitors"

    registration: str = Field(primary_key=True)
    name: str
    email: str

    assignments: list["MonitorAssignment"] = Relationship(back_populates="monitor")
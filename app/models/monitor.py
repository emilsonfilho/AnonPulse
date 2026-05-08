from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.monitor_assignment import MonitorAssignment

class Monitor(SQLModel, table=True):
    __tablename__ = "monitors"

    id: int | None = Field(default= None, primary_key=True)
    registration: str = Field(unique=True)
    name: str
    email: str

    assignments: list["MonitorAssignment"] = Relationship(back_populates="monitor")
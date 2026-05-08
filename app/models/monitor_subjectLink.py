from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field

class MonitorSubjectLink(SQLModel, table=True):
    __tablename__ = "monitor_subject_link"

    monitor_id: int = Field(foreign_key="monitores.id", primary_key=True)
    subject_id: int = Field(foreign_key="subjects.id", primary_key=True)
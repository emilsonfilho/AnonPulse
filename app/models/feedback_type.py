from sqlmodel import SQLModel, Field, Relationship
from app.core.enums import MessageType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.feedback import Feedback

class FeedbackType(SQLModel, table=True):
    __tablename__ = "feedback_types"

    id: int | None = Field(default=None, primary_key=True)
    type: MessageType

    feedbacks: list["Feedback"] = Relationship(back_populates="type")
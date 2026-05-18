from typing import Annotated
from pydantic import BaseModel, Field

from app.core.enums import MessageType
from app.schemas.orm_base_schema import ORMBaseSchema
class FeedbackTypeBase(BaseModel):
   type: Annotated[
      MessageType,
      Field(
         description="Tipo de feedback"
      )
   ]

class CreateFeedbackTypeRequest(FeedbackTypeBase):
   pass

class UpdateFeedbackTypeRequest(BaseModel):
   type: Annotated[
     MessageType | None, 
     Field(
        default=None
      )
   ]
    
class FeedbackTypeResponse(FeedbackTypeBase, ORMBaseSchema):
   id: int
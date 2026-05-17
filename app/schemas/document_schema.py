from pydantic import BaseModel
from datetime import datetime

class DocumentBase(BaseModel):
    original_filename: str
    content_type: str
    extension: str
    size_bytes: int
    assignment_id: int
    
class CreateDocumentRequest(DocumentBase):
    pass

class UpdateDocumentRequest(BaseModel):
    original_filename: str | None = None
    content_type: str | None = None
    extension: str | None = None
    size_bytes: int | None = None
    assignment_id: int | None = None

class DocumentResponse(DocumentBase):
    id: int
    created_at: datetime
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

class DocumentResponse(DocumentBase):
    id: int
    created_at: datetime
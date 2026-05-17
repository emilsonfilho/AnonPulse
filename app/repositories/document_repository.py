from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.document_schema import CreateDocumentRequest
from app.models.document import Document

class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, data: CreateDocumentRequest) -> Document:
        new_document = Document(**data.model_dump())

        self.session.add(new_document)
        await self.session.commit()
        await self.session.refresh(new_document)

        return new_document
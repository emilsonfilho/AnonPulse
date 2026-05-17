from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from app.models.document import Document
from app.repositories.base_repository import BaseRepository

class DocumentRepository(BaseRepository[Document]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Document, session=session)
    
    async def list_by_assignment(self, assignment_id: int, params: Params) -> Page[Document]:
        query = select(self.model).where(self.model.assignment_id == assignment_id)
        return await paginate(self.session, query, params)
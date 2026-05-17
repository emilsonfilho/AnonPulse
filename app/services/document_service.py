import os 
import shutil

from fastapi import UploadFile
from fastapi_pagination import Page, Params

from app.core.mapper import Mapper
from app.services.base_service import BaseService
from app.schemas.document_schema import (
    DocumentResponse,
    CreateDocumentRequest,
    UpdateDocumentRequest
)
from app.models.document import Document
from app.core.exceptions.custom_exceptions import DocumentNotFoundException, DocumentNotExistsException

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class DocumentService(
    BaseService[Document, CreateDocumentRequest, UpdateDocumentRequest, DocumentResponse]
):
    def __init__(self, repository):
        super().__init__(
            repository=repository,
            response_schema=DocumentResponse,
            not_found_exception=DocumentNotFoundException
        )
        self.repository = repository

    def _get_file_path(self, doc: Document) -> str:
        return f"{UPLOAD_DIR}/{doc.id}.{doc.extension}"
    
    def _get_extension(self, file: UploadFile) -> str:
        return file.filename.split(".")[-1] if "." in file.filename else ""
    
    async def _get_size(self, file: UploadFile) -> int:
        await file.seek(0, os.SEEK_END)
        new_size = file.file.tell()
        await file.seek(0)

        return new_size

    async def upload(self, assignment_id: int, file: UploadFile) -> DocumentResponse:
        extension = self._get_extension(file)

        size_bytes = await self._get_size(file)

        document_data = {
            "original_filename": file.filename,
            "content_type": file.content_type,
            "extension": extension,
            "size_bytes": size_bytes,
            "assignment_id": assignment_id
        }

        document = Document(**document_data)

        new_document = await self.repository.create(document)

        file_path = self._get_file_path(new_document)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return DocumentResponse.model_validate(new_document)

    async def download(self, id: int) -> tuple[str, str]:
        document = await self.get_or_raise(id)

        file_path = self._get_file_path(document)

        if not os.path.exists(file_path):
            raise DocumentNotExistsException()
        
        return file_path, document.original_filename
    
    async def update(self, id: int, file: UploadFile) -> DocumentResponse:
        prev_doc = await self.get_or_raise(id)

        prev_file_path = self._get_file_path(prev_doc)
        if os.path.exists(prev_file_path):
            os.remove(prev_file_path)

        new_extension = self._get_extension(file)
        new_size = await self._get_size(file)

        new_file_path = f"{UPLOAD_DIR}/{prev_doc.id}.{new_extension}"
        with open(new_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        updated_data = {
            "original_filename": file.filename,
            "content_type": file.content_type,
            "extension": new_extension,
            "size_bytes": new_size
        }

        updated = await self.repository.update(id, updated_data)

        return Mapper.to_response(updated, DocumentResponse)
    
    async def delete(self, id: int) -> None:
        document = await self.get_or_raise(id)

        await super().delete(id)

        file_path = self._get_file_path(document)
        if os.path.exists(file_path):
            os.remove(file_path)

    async def list_by_assignment(self, assignment_id: int, params: Params) -> Page[Document]:
        page_result = await self.repository.list_by_assignment(assignment_id, params)

        page_result.items = [
            Mapper.to_response(document, self.response_schema) for document in page_result
        ]

        return page_result
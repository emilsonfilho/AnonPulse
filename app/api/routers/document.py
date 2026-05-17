from fastapi import APIRouter, UploadFile, File, Depends
from fastapi_pagination import Page, Params
from app.services.document_service import DocumentService
from app.schemas.document_schema import (
    DocumentResponse,
    CreateDocumentRequest,
    UpdateDocumentRequest,
)
from app.core.exceptions.custom_exceptions import (
    DocumentNotFoundException,
    DocumentNotExistsException,
)
from app.api.dependencies.services import get_document_service

api_router = APIRouter(prefix="/documents", tags=["Documentos"])


@api_router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    assignment_id: int,
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
):
    return await service.upload(assignment_id, file)


@api_router.get("/{document_id}", response_model=UploadFile)
async def get_document(
    document_id: int, service: DocumentService = Depends(get_document_service)
):
    file_path, filename = await service.download(document_id)
    return File(file_path, media_type="application/octet-stream", filename=filename)


@api_router.get("/", response_model=Page[DocumentResponse])
async def list_documents(
    assignment_id: int,
    params: Params = Depends(),
    service: DocumentService = Depends(get_document_service),
):
    return await service.list_by_assignment(assignment_id=assignment_id, params=params)


@api_router.patch("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: int,
    update_data: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
):
    return await service.update(document_id, update_data)


@api_router.delete("/{document_id}")
async def delete_document(
    document_id: int, service: DocumentService = Depends(get_document_service)
):
    await service.delete(document_id)
    return {"detail": "Documento deletado com sucesso"}

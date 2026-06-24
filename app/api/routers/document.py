from fastapi import APIRouter, Depends, File, Response, UploadFile, status
from fastapi_pagination import Page, Params

from app.api.dependencies.services import get_document_service
from app.schemas.document_schema import (
    DocumentResponse,
)
from app.services.document_service import DocumentService

api_router = APIRouter(prefix="/documents", tags=["Documentos"])


@api_router.post(
    "/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED
)
async def upload_document(
    assignment_id: str,  # Modificado para str (MongoDB)
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
):
    """Envia um novo documento para o MinIO e salva os metadados."""
    return await service.upload(assignment_id, file)


@api_router.get("/{document_id}", response_model=DocumentResponse)
async def get_document_metadata(
    document_id: str, service: DocumentService = Depends(get_document_service)
):
    """Retorna apenas os metadados do documento (Exigência do TP3)."""
    return await service.get_or_raise(document_id)


@api_router.get("/{document_id}/download")
async def download_document(
    document_id: str, service: DocumentService = Depends(get_document_service)
):
    """Baixa o arquivo físico diretamente do MinIO."""
    file_data, original_name, content_type = await service.download(document_id)

    # Retorna os bytes do arquivo em memória com os cabeçalhos corretos para download
    return Response(
        content=file_data,
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="{original_name}"'},
    )


@api_router.get("/", response_model=Page[DocumentResponse])
async def list_documents(
    assignment_id: str,
    params: Params = Depends(),
    service: DocumentService = Depends(get_document_service),
):
    """Lista os metadados dos documentos paginados vinculados a uma assignment."""
    return await service.list_by_assignment(assignment_id=assignment_id, params=params)


@api_router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
):
    """Substitui o arquivo físico no MinIO e atualiza os metadados."""
    return await service.update(document_id, file)


@api_router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str, service: DocumentService = Depends(get_document_service)
):
    """Remove o documento do MongoDB e o arquivo físico do MinIO."""
    await service.delete(document_id)

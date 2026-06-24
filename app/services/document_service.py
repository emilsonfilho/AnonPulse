"""Serviço de gerenciamento de documentos.

Este módulo fornece funcionalidades para upload, download, atualização e exclusão
de documentos, com validação de tipo MIME e armazenamento em nuvem (MinIO).
"""

from fastapi import HTTPException, UploadFile
from fastapi_pagination import Page, Params

from app.core.exceptions.custom_exceptions import DocumentNotFoundException
from app.core.mapper import Mapper
from app.models.document_metadata import Document
from app.schemas.document_schema import (
    CreateDocumentRequest,
    DocumentResponse,
    UpdateDocumentRequest,
)
from app.services.base_service import BaseService
from app.services.storage_service import StorageService

ALLOWED_MIME_TYPES = [
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/gif",
]


class DocumentService(
    BaseService[
        Document, CreateDocumentRequest, UpdateDocumentRequest, DocumentResponse
    ]
):
    """Serviço para gerenciar operações de documentos.

    Fornece métodos para upload, download, atualização e exclusão de documentos,
    com validação de tipo de arquivo e armazenamento no MinIO.
    """

    def __init__(self, repository, storage_service: StorageService):
        """Inicializa o serviço de documentos.

        Args:
            repository: Repositório de documentos para operações de banco de dados.
            storage_service: Serviço responsável pela persistência física no MinIO.
        """
        super().__init__(
            repository=repository,
            response_schema=DocumentResponse,
            not_found_exception=DocumentNotFoundException,
        )
        self.repository = repository
        self.storage_service = storage_service

    def _get_filename(self, doc: Document) -> str:
        """Obtém o nome físico do arquivo que será salvo no bucket.

        Args:
            doc: Objeto do documento.

        Returns:
            Nome do arquivo no formato '{id}.{extensao}'.
        """
        return f"{doc.id}.{doc.extension}"

    def _get_extension(self, file: UploadFile) -> str:
        """Extrai a extensão do arquivo.

        Args:
            file: Arquivo enviado.

        Returns:
            Extensão do arquivo ou string vazia se não houver.
        """
        return file.filename.split(".")[-1] if "." in file.filename else ""

    async def _get_size(self, file: UploadFile) -> int:
        """Obtém o tamanho do arquivo em bytes.

        Args:
            file: Arquivo enviado.

        Returns:
            Tamanho do arquivo em bytes.
        """
        content = await file.read()
        size = len(content)
        await file.seek(0)
        return size

    async def upload(self, assignment_id: str, file: UploadFile) -> DocumentResponse:
        """Faz upload de um novo documento.

        Salva os metadados no MongoDB primeiro para gerar o ID e, em seguida,
        envia o arquivo físico para o MinIO.

        Args:
            assignment_id: ID da tarefa associada.
            file: Arquivo a ser enviado.

        Returns:
            Resposta do documento criado.

        Raises:
            HTTPException: Se o tipo MIME não for permitido.
        """
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Formato inválido. São permitidos apenas ficheiros PDF e imagens.",
            )

        extension = self._get_extension(file)
        size_bytes = await self._get_size(file)

        document_data = {
            "original_filename": file.filename,
            "content_type": file.content_type,
            "extension": extension,
            "size_bytes": size_bytes,
            "assignment_id": assignment_id,
        }

        # 1. Salva os metadados no MongoDB
        document = Document(**document_data)
        new_document = await self.repository.create(document)

        # 2. Faz o upload físico no MinIO
        filename = self._get_filename(new_document)
        await self.storage_service.upload_file(file, filename)

        return DocumentResponse.model_validate(new_document)

    async def download(self, id: str) -> tuple[bytes, str, str]:
        """Recupera os bytes do documento diretamente do MinIO.

        Args:
            id: O ID do documento no banco de dados.

        Returns:
            Uma tupla contendo (bytes_do_arquivo, nome_original, content_type).
        """
        document = await self.get_or_raise(id)
        filename = self._get_filename(document)

        file_data, content_type = await self.storage_service.download_file(filename)

        return file_data, document.original_filename, content_type

    async def update(self, id: str, file: UploadFile) -> DocumentResponse:
        """Substitui o arquivo físico e atualiza os metadados.

        Args:
            id: ID do documento a ser atualizado.
            file: Novo arquivo.
        """
        prev_doc = await self.get_or_raise(id)
        old_filename = self._get_filename(prev_doc)

        # 1. Deleta o arquivo antigo do MinIO
        try:
            await self.storage_service.delete_file(old_filename)
        except Exception:
            pass  # Ignora se o arquivo antigo já não existir fisicamente no bucket

        # 2. Prepara novos dados
        new_extension = self._get_extension(file)
        new_size = await self._get_size(file)

        updated_data = {
            "original_filename": file.filename,
            "content_type": file.content_type,
            "extension": new_extension,
            "size_bytes": new_size,
        }

        # 3. Atualiza os metadados no MongoDB
        updated = await self.repository.update(id, updated_data)

        # 4. Envia o novo arquivo para o MinIO
        new_filename = self._get_filename(updated)
        await self.storage_service.upload_file(file, new_filename)

        return Mapper.to_response(updated, DocumentResponse)

    async def delete(self, id: str) -> None:
        """Remove o documento da base de dados e exclui o arquivo do MinIO."""
        document = await self.get_or_raise(id)
        filename = self._get_filename(document)

        # Remove do MongoDB
        await super().delete(id)

        # Remove do MinIO
        await self.storage_service.delete_file(filename)

    async def list_by_assignment(
        self, assignment_id: str, params: Params
    ) -> Page[Document]:
        page_result = await self.repository.list_by_assignment(assignment_id, params)

        page_result.items = [
            Mapper.to_response(document, self.response_schema)
            for document in page_result.items
        ]

        return page_result

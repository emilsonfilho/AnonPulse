from beanie import PydanticObjectId
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.beanie import apaginate

from app.models.document_metadata import DocumentMetadata
from app.repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository[DocumentMetadata]):
    """
    Repositório para gerenciar as operações de banco de dados da entidade Document.

    Esta classe herda de BaseRepository e fornece métodos de consulta específicos
    para o gerenciamento de metadados de arquivos (Document), permitindo a listagem
    filtrada por vínculos com outras entidades e suporte a paginação assíncrona.
    """

    def __init__(self) -> None:
        """
        Inicializa o repositório de documentos.

        Args:
            session (AsyncSession): Sessão assíncrona do banco de dados
                gerenciada pelo SQLModel/SQLAlchemy.
        """
        super().__init__(model=DocumentMetadata)

    async def list_by_assignment(
        self, assignment_id: int, params: Params, fetch_links: bool = False
    ) -> Page[DocumentMetadata]:
        """
        Lista de forma paginada todos os documentos associados a uma atribuição.

        Este método atende aos requisitos do TP2 ao permitir buscar os metadados
        dos arquivos salvos localmente que pertencem a uma determinada relação
        de monitoria (MonitorAssignment).

        Args:
            assignment_id (int): O identificador único da atribuição de monitoria.
            params (Params): Parâmetros de paginação fornecidos pelo fastapi-pagination
                (como página atual e tamanho da página).
            fetch_links: Se True, carrega os documentos relacionados (links).

        Returns:
            Page[Document]: Objeto paginado contendo a lista de metadados dos documentos
                encontrados e as informações de controle da paginação.
        """
        if isinstance(assignment_id, str):
            assignment_id = PydanticObjectId(assignment_id)

        query = self.model.find(
            {"assignment.$id": assignment_id}, fetch_links=fetch_links
        )

        return await apaginate(query, params)

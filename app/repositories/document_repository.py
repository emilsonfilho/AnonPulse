from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.document_metadata import Document
from app.repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    """
    Repositório para gerenciar as operações de banco de dados da entidade Document.

    Esta classe herda de BaseRepository e fornece métodos de consulta específicos
    para o gerenciamento de metadados de arquivos (Document), permitindo a listagem
    filtrada por vínculos com outras entidades e suporte a paginação assíncrona.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Inicializa o repositório de documentos.

        Args:
            session (AsyncSession): Sessão assíncrona do banco de dados 
                gerenciada pelo SQLModel/SQLAlchemy.
        """
        super().__init__(model=Document, session=session)
    
    async def list_by_assignment(
        self, 
        assignment_id: int, 
        params: Params
    ) -> Page[Document]:
        """
        Lista de forma paginada todos os documentos associados a uma atribuição.

        Este método atende aos requisitos do TP2 ao permitir buscar os metadados
        dos arquivos salvos localmente que pertencem a uma determinada relação 
        de monitoria (MonitorAssignment).

        Args:
            assignment_id (int): O identificador único da atribuição de monitoria.
            params (Params): Parâmetros de paginação fornecidos pelo fastapi-pagination
                (como página atual e tamanho da página).

        Returns:
            Page[Document]: Objeto paginado contendo a lista de metadados dos documentos
                encontrados e as informações de controle da paginação.
        """
        query = select(self.model).where(self.model.assignment_id == assignment_id)
        return await paginate(self.session, query, params)
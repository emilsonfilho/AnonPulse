from typing import Any

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import select

from app.models.classroom import Classroom
from app.repositories.base_repository import BaseRepository


class ClassroomRepository(BaseRepository[Classroom]):
    """
    Repositório para gerenciar as operações de banco de dados da entidade Classroom.

    Esta classe herda de BaseRepository e fornece métodos de consulta específicos
    para a entidade de turmas (Classroom), permitindo listagens filtradas por
    relacionamentos com suporte a paginação e carregamento ansioso (eager loading).
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Inicializa o repositório de turmas.

        Args:
            session (AsyncSession): Sessão assíncrona do banco de dados 
                gerenciada pelo SQLAlchemy.
        """
        super().__init__(model=Classroom, session=session)
    
    async def list_by_professor(
        self, 
        professor_id: int, 
        params: Params, 
        options: list[Any] | None = None
    ) -> Page[Classroom]:
        """
        Lista de forma paginada todas as turmas associadas a um determinado professor.

        Args:
            professor_id (int): O identificador único do professor.
            params (Params): Parâmetros de paginação fornecidos pelo fastapi-pagination 
                (página atual e limite de itens).
            options (list[Any] | None, opcional): Lista de estratégias de eager loading 
                do SQLAlchemy (como selectinload ou joinedload) para evitar o 
                problema de consultas N+1. Padrão é None.

        Returns:
            Page[Classroom]: Objeto paginado contendo a lista de turmas encontradas 
                e os metadados de paginação.
        """
        query = select(self.model).where(self.model.professor_id == professor_id)

        if options:
            query = query.options(*options)

        return await paginate(self.session, query, params)
    
    async def list_by_subject(
        self, 
        subject_cod: str, 
        params: Params, 
        options: list[Any] | None = None
    ) -> Page[Classroom]:
        """
        Lista de forma paginada todas as turmas vinculadas a uma determinada disciplina.

        Args:
            subject_cod (str): O código de identificação da disciplina (ex: "QXD123").
            params (Params): Parâmetros de paginação fornecidos pelo fastapi-pagination.
            options (list[Any] | None, opcional): Lista de estratégias de eager loading 
                do SQLAlchemy (como selectinload ou joinedload) para o carregamento 
                eficiente de relacionamentos. Padrão é None.

        Returns:
            Page[Classroom]: Objeto paginado contendo a lista de turmas encontradas 
                e os metadados de paginação.
        """
        query = select(self.model).where(self.model.subject_cod == subject_cod)
        
        if options:
            query = query.options(*options)

        return await paginate(self.session, query, params)
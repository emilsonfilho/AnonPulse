"""Serviço de disciplina.

Este módulo fornece a implementação do serviço de disciplina,
responsável pela lógica de negócio relacionada às disciplinas.
"""
from typing import cast

from app.core.exceptions.custom_exceptions import (
    SubjectAlreadyExistsException,
    SubjectNotFoundException,
)
from app.core.mapper import Mapper
from app.models import Subject
from app.repositories.subject_repository import SubjectRepository
from app.schemas.subject_schema import (
    CreateSubjectRequest,
    SubjectResponse,
    UpdateSubjectRequest,
)
from app.services.base_service import BaseService


class SubjectService(
    BaseService[Subject, CreateSubjectRequest, UpdateSubjectRequest, SubjectResponse]
):
    """Serviço para gerenciar operações de disciplinas.

    Herda de BaseService e fornece funcionalidades específicas para
    manipulação de dados de disciplinas, incluindo criação, leitura,
    atualização e exclusão.
    """

    def __init__(self, repository: SubjectRepository) -> None:
        """Inicializa o serviço de disciplina.

        Args:
            repository: Instância do repositório de disciplinas.
        """
        super().__init__(
            repository=repository,
            response_schema=SubjectResponse,
            not_found_exception=SubjectNotFoundException,
            already_exists_exception=SubjectAlreadyExistsException,
        )

    async def create(self, request: CreateSubjectRequest) -> SubjectResponse:
        """Cria uma nova disciplina.

        Args:
            request: Requisição com os dados da disciplina a ser criada.

        Returns:
            SubjectResponse: Resposta contendo os dados da disciplina criada.
        """
        if await self.repository.find_by(cod=request.cod):
            raise SubjectAlreadyExistsException(request.cod)

        subject = Subject(
            cod=request.cod,
            name=request.name,
        )

        new_obj = await subject.insert()

        await new_obj.fetch_all_links()

        return cast(
            SubjectResponse, Mapper.to_response(new_obj, self.response_schema)
        )

    async def update(
            self,
            identifier: str,
            request: UpdateSubjectRequest,
            fetch_links: bool | None = None,
    ) -> SubjectResponse:
        subject = await self.repository.find_by(cod=identifier)

        if not subject:
            raise SubjectNotFoundException()

        await subject.update({ "$set": { "name": request.name } })
        await subject.fetch_all_links()
        return cast(SubjectResponse, Mapper.to_response(subject, self.response_schema))

    async def get_by_cod(self, cod: str) -> SubjectResponse:
       return await self.get_by(cod=cod)

    async def delete(self, cod: str) -> None:
        subject = await self.repository.find_by(cod=cod)
        if not subject:
            raise SubjectNotFoundException()

        await subject.delete()
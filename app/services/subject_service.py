"""Serviço de disciplina.

Este módulo fornece a implementação do serviço de disciplina,
responsável pela lógica de negócio relacionada às disciplinas.
"""

from app.core.exceptions.custom_exceptions import (
    SubjectAlreadyExistsException,
    SubjectNotFoundException,
)
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
        return await super().create(request, identifier_value=request.cod)

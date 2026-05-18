"""Serviço de inscrição (enrollment).

Este módulo contém a lógica de negócio para gerenciar inscrições,
incluindo criação, recuperação e exclusão lógica de registros.
"""

from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError

from app.core.exceptions.custom_exceptions import (
    EnrollmentAlreadyExistsException,
    EnrollmentNotFoundException,
)
from app.core.mapper import Mapper
from app.models.enrollment import Enrollment
from app.repositories.enrollment_repository import EnrollmentRepository
from app.schemas.enrollment_schema import (
    CreateEnrollmentRequest,
    EnrollmentResponse,
    UpdateEnrollmentRequest,
)
from app.services.base_service import BaseService


class EnrollmentService(
    BaseService[
        Enrollment, CreateEnrollmentRequest, UpdateEnrollmentRequest, EnrollmentResponse
    ]
):
    """Serviço para gerenciar operações de inscrição.

    Fornece funcionalidades para criar, recuperar e deletar inscrições,
    herdando funcionalidades base de manipulação de dados.
    """

    def __init__(self, repository: EnrollmentRepository) -> None:
        """Inicializa o serviço de inscrição.

        Args:
            repository: Repositório para acesso aos dados de inscrição.
        """
        super().__init__(
            repository=repository,
            response_schema=EnrollmentResponse,
            not_found_exception=EnrollmentNotFoundException,
            already_exists_exception=EnrollmentAlreadyExistsException,
        )

    async def create(self, request: CreateEnrollmentRequest) -> EnrollmentResponse:
        """Cria uma nova inscrição.

        Args:
            request: Dados da inscrição a ser criada.

        Returns:
            EnrollmentResponse: Dados da inscrição criada.

        Raises:
            EnrollmentAlreadyExistsException: Se a inscrição já existe.
        """
        enrollment = Enrollment(
            **request.model_dump(),
            is_active=True,
            enrolled_at=datetime.now(timezone.utc),
        )
        
        try:
            new_enrollment = await self.repository.create(enrollment)
        except IntegrityError:
            raise EnrollmentAlreadyExistsException()

        return Mapper.to_response(new_enrollment, EnrollmentResponse)

    async def delete(self, id: int) -> None:
        """Deleta uma inscrição (exclusão lógica).

        Define o status is_active como False em vez de remover o registro.

        Args:
            id: Identificador da inscrição a ser deletada.

        Raises:
            EnrollmentNotFoundException: Se a inscrição não é encontrada.
        """
        await self.get_or_raise(id)

        await self.repository.update(id, {"is_active": False})

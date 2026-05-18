"""
Serviço de gerenciamento de atribuições de monitores.

Módulo responsável pela lógica de negócio relacionada à criação, atualização,
deleção e recuperação de atribuições de monitores.
"""

from app.core.exceptions.custom_exceptions import (
    MonitorAssignmentHasFeedbackException,
    MonitorAssignmentNotFoundException,
)
from app.core.mapper import Mapper
from sqlalchemy.orm import joinedload
from app.models.monitor_assignment import MonitorAssignment
from app.repositories.monitor_assignment_repository import MonitorAssignmentRepository
from app.schemas.monitor_assignment_schema import (
    CreateMonitorAssignmentRequest,
    MonitorAssignmentResponse,
    UpdateMonitorAssignmentRequest,
)
from app.services.base_service import BaseService


class MonitorAssignmentService(
    BaseService[
        MonitorAssignment,
        CreateMonitorAssignmentRequest,
        UpdateMonitorAssignmentRequest,
        MonitorAssignmentResponse,
    ]
):
    """
    Serviço para gerenciar atribuições de monitores.

    Fornece funcionalidades para criar, atualizar, recuperar e deletar
    atribuições de monitores, com validações de regras de negócio.
    """

    def __init__(self, repository: MonitorAssignmentRepository) -> None:
        """
        Inicializa o serviço de atribuição de monitores.

        Args:
            repository: Repositório para acesso aos dados de atribuições.
        """
        super().__init__(
            repository=repository,
            response_schema=MonitorAssignmentResponse,
            not_found_exception=MonitorAssignmentNotFoundException
        )

    async def create(
        self, request: CreateMonitorAssignmentRequest
    ) -> MonitorAssignmentResponse:
        """
        Cria uma nova atribuição de monitor.

        Args:
            request: Dados da solicitação para criar uma atribuição.

        Returns:
            MonitorAssignmentResponse: Resposta contendo a atribuição criada.
        """
        assignment = MonitorAssignment(**request.model_dump())
        new_assignment = await self.repository.create(assignment)

        return Mapper.to_response(new_assignment, self.response_schema)

    async def delete(self, id: int) -> None:
        """
        Deleta uma atribuição de monitor.

        Args:
            id: Identificador da atribuição a ser deletada.

        Raises:
            MonitorAssignmentNotFoundException: Se a atribuição não existir.
            MonitorAssignmentHasFeedbackException: Se a atribuição possuir
                feedbacks associados.
        """
        # Carrega explicitamente os feedbacks para evitar lazy-load assíncrono
        assignment = await self.get_or_raise(
            id, options=[joinedload(MonitorAssignment.feedbacks)] # <--- Mude aqui
        )

        if assignment.feedbacks:
            raise MonitorAssignmentHasFeedbackException(id)

        await self.repository.delete(id)

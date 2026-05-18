"""Serviço para gerenciamento de monitores.

Este módulo fornece a classe MonitorService que implementa operações
CRUD para monitores, estendendo a funcionalidade do BaseService.
"""

from app.core.exceptions.custom_exceptions import (
    MonitorAlreadyExistsException,
    MonitorNotFoundException,
)
from app.models.monitor import Monitor
from app.repositories.monitor_repository import MonitorRepository
from app.schemas.monitor_schema import (
    CreateMonitorRequest,
    MonitorResponse,
    UpdateMonitorRequest,
)
from app.services.base_service import BaseService


class MonitorService(
    BaseService[Monitor, CreateMonitorRequest, UpdateMonitorRequest, MonitorResponse]
):
    """Serviço para gerenciar operações de monitores.

    Esta classe estende BaseService e fornece métodos para criar,
    atualizar, recuperar e deletar monitores.
    """

    def __init__(self, repository: MonitorRepository) -> None:
        """Inicializa o serviço de monitor.

        Args:
            repository: Repositório de monitor para acesso aos dados.
        """
        super().__init__(
            repository=repository,
            response_schema=MonitorResponse,
            not_found_exception=MonitorNotFoundException,
            already_exists_exception=MonitorAlreadyExistsException,
        )

    async def create(self, request: CreateMonitorRequest) -> MonitorResponse:
        """Cria um novo monitor.

        Args:
            request: Dados de requisição para criação do monitor.

        Returns:
            MonitorResponse: Dados do monitor criado.
        """
        return await super().create(request, identifier_value=request.registration)

from http import HTTPStatus

from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Page, Params

from app.api.dependencies.services import get_monitor_service
from app.schemas.monitor_schema import (
    CreateMonitorRequest,
    MonitorResponse,
    UpdateMonitorRequest,
)
from app.services.monitor_service import MonitorService

api_router = APIRouter(prefix="/v1/monitores", tags=["Monitores"])


@api_router.post(
    path="/",
    response_model=MonitorResponse,
    name="Criar Monitor",
    description="Cria um novo monitor.",
    response_description="Monitor criado com sucesso.",
    status_code=HTTPStatus.CREATED,
)
async def create_monitor(
    monitor_request: CreateMonitorRequest,
    service: MonitorService = Depends(get_monitor_service),
) -> MonitorResponse:
    """Cria um novo monitor.

    A rota recebe os dados validados do corpo da requisição e delega a criação
    do monitor para a camada de serviço. O serviço é responsável por
    persistir o novo monitor e retornar os dados do monitor criado.

    Args:
        monitor_request: Dados necessários para criar um novo monitor.
        monitor_service: Dependência injetada com as regras de negócio de
            monitores.

    Returns:
        MonitorResponse: Dados do monitor criado.
    """
    return await service.create(monitor_request)


@api_router.get(
    path="/",
    response_model=Page[MonitorResponse],
    name="Listar Monitores",
    description="Retorna uma lista paginada de monitores.",
    response_description="Lista de monitores paginada.",
)
async def list_monitors(
    monitor_service: MonitorService = Depends(get_monitor_service),
    params: Params = Depends(),
) -> Page[MonitorResponse]:
    """Lista os monitores cadastrados.

    Esta rota consulta a camada de serviço para obter a lista de monitores
    persistidos e devolve o resultado paginado.

    Args:
        monitor_service: Dependência injetada com as regras de negócio de
            monitores.
        params: Parâmetros de paginação extraídos da query string."""
    return await monitor_service.list_all(params)


@api_router.patch(
    path="/{monitor_id}",
    response_model=MonitorResponse,
    name="Atualizar Monitor",
    description="Atualiza os dados de um monitor existente.",
    response_description="Monitor atualizado com sucesso.",
)
async def update_monitor(
    monitor_request: UpdateMonitorRequest,
    monitor_service: MonitorService = Depends(get_monitor_service),
    monitor_id: str = Path(..., description="ID do monitor a ser atualizado"),
) -> MonitorResponse:
    """Atualiza os dados de um monitor existente.

    A rota recebe o ID do monitor a ser atualizado e os dados validados do
    corpo da requisição. Ela delega a atualização do monitor para a camada
    de serviço, que é responsável por persistir as alterações e retornar os
    dados do monitor atualizado.

    Args:
        monitor_id: ID do monitor a ser atualizado.
        monitor_request: Dados para atualizar o monitor.
        monitor_service: Dependência injetada com as regras de negócio de
            monitores.

    Returns:
        MonitorResponse: Dados do monitor atualizado.
    """
    monitor = await monitor_service.update(monitor_id, monitor_request)
    return monitor


@api_router.get(
    path="/{monitor_id}",
    response_model=MonitorResponse,
    name="Buscar Monitor por ID",
    description="Retorna os dados de um monitor específico pelo seu ID.",
    response_description="Dados do monitor encontrada.",
)
async def get_monitor_by_id(
    monitor_service: MonitorService = Depends(get_monitor_service),
    monitor_id: str = Path(..., description="ID do monitor a ser consultado"),
) -> MonitorResponse:
    """Busca os dados de um monitor específico pelo seu ID.

    A rota recebe o ID do monitor a ser buscado e delega a consulta para a
    camada de serviço. O serviço é responsável por recuperar os dados do
    monitor e retorná-los.

    Args:
        monitor_id: ID do monitor a ser buscado.
        monitor_service: Dependência injetada com as regras de negócio de
            monitores.
    Returns:
        MonitorResponse: Dados do monitor encontrada.
    """
    monitor = await monitor_service.get_by_id(monitor_id)
    return monitor


@api_router.delete(
    path="/{monitor_id}",
    status_code=HTTPStatus.NO_CONTENT,
    name="Excluir Monitor",
    description="Exclui um monitor existente.",
    response_description="Monitor excluído com sucesso.",
)
async def delete_monitor(
    monitor_service: MonitorService = Depends(get_monitor_service),
    monitor_id: str = Path(..., description="ID do monitor a ser excluído"),
) -> None:
    """Exclui um monitor existente.

    A rota recebe a matrícula do monitor a ser excluído e delega a exclusão para a
    camada de serviço, que é responsável por remover o monitor do sistema.

    Args:
        monitor_id: ID do monitor a ser excluído.
        monitor_service: Dependência injetada com as regras de negócio de
            monitores.
    Returns:
        None
    """
    await monitor_service.delete(monitor_id)

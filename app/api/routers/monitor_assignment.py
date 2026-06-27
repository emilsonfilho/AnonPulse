from http import HTTPStatus

from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Page, Params

from app.schemas.monitor_assignment_schema import (
    CreateMonitorAssignmentRequest,
    MonitorAssignmentResponse,
    UpdateMonitorAssignmentRequest,
)
from app.services.monitor_assignment_service import MonitorAssignmentService
from app.api.dependencies.services import get_monitor_assignment_service

api_router = APIRouter(prefix="/v1/monitorias", tags=["Monitorias"])


@api_router.post(
    path="/",
    response_model=MonitorAssignmentResponse,
    name="Criar Monitoria",
    description="Cria uma nova monitoria.",
    response_description="Monitoria criada com sucesso.",
    status_code=HTTPStatus.CREATED,
)
async def create_monitor_assignment(
    monitor_assignment_request: CreateMonitorAssignmentRequest,
    monitor_assignment_service: MonitorAssignmentService = Depends(
        get_monitor_assignment_service
    ),
) -> MonitorAssignmentResponse:
    """Cria uma nova monitoria.

    A rota recebe os dados validados do corpo da requisição e delega a criação
    da monitoria para a camada de serviço. O serviço é responsável por
    persistir a nova monitoria e retornar os dados da monitoria criada.

    Args:
        monitor_assignment_request: Dados necessários para criar uma nova monitoria.
        monitor_assignment_service: Dependência injetada com as regras de negócio de
            cursos.

    Returns:
        MonitorAssignmentResponse: Dados da monitoria criada.
    """
    monitor_assignment = await monitor_assignment_service.create(
        monitor_assignment_request
    )
    return monitor_assignment


@api_router.get(
    path="/",
    response_model=Page[MonitorAssignmentResponse],
    name="Listar Monitorias",
    description="Retorna uma lista paginada de monitorias.",
    response_description="Lista de monitorias paginada.",
)
async def list_monitor_assignments(
    monitor_assignment_service: MonitorAssignmentService = Depends(
        get_monitor_assignment_service
    ),
    params: Params = Depends(),
) -> Page[MonitorAssignmentResponse]:
    """Lista as monitorias cadastradas.

    Esta rota consulta a camada de serviço para obter a lista de monitorias
    persistidas e devolve o resultado paginado.

    Args:
        params: Parâmetros de paginação.
        monitor_assignment_service: Dependência injetada com as regras de negócio de
            cursos.

    Returns:
        Page[MonitorAssignmentResponse]: Página contendo a lista de monitorias.
    """
    return await monitor_assignment_service.list_all(params)


@api_router.get(
    path="/{monitor_assignment_id}",
    response_model=MonitorAssignmentResponse,
    name="Buscar Monitoria por ID",
    description="Retorna uma monitoria específica pelo seu ID.",
    response_description="Dados da monitoria encontrada.",
)
async def get_monitor_assignment_by_id(
    monitor_assignment_service: MonitorAssignmentService = Depends(
        get_monitor_assignment_service
    ),
    monitor_assignment_id: str = Path(
        ..., description="ID da monitoria a ser consultada."
    ),
) -> MonitorAssignmentResponse:
    """Busca uma monitoria específica a partir do identificador.

    A rota recebe o identificador numérico da monitoria a ser consultada e
    delega a busca para a camada de serviço, que é responsável por retornar os
    dados da monitoria encontrada.

    Args:
        monitor_assignment_id: Identificador numérico da monitoria a ser consultada.
        monitor_assignment_service: Dependência injetada com as regras de negócio de
            cursos.

    Returns:
        MonitorAssignmentResponse: Dados da monitoria encontrada.
    """
    monitor_assignment = await monitor_assignment_service.get_by_id(
        monitor_assignment_id
    )
    return monitor_assignment


@api_router.patch(
    path="/{monitor_assignment_id}",
    response_model=MonitorAssignmentResponse,
    name="Atualizar Monitoria",
    description="Atualiza os dados de uma monitoria existente.",
    response_description="Monitoria atualizada com sucesso.",
)
async def update_monitor_assignment(
    monitor_assignment_request: UpdateMonitorAssignmentRequest,
    monitor_assignment_service: MonitorAssignmentService = Depends(
        get_monitor_assignment_service
    ),
    monitor_assignment_id: str = Path(
        ..., description="ID da monitoria a ser atualizada."
    ),
) -> MonitorAssignmentResponse:
    """Atualiza os dados de uma monitoria existente.

    A rota recebe o identificador da monitoria a ser atualizada e os dados
    validados do corpo da requisição. Ela delega a atualização para a camada de
    serviço, que é responsável por persistir as alterações e retornar os dados
    da monitoria atualizada.

    Args:
        monitor_assignment_id: Identificador numérico da monitoria a ser atualizada.
        monitor_assignment_request: Dados para atualizar a monitoria.
        monitor_assignment_service: Dependência injetada com as regras de negócio de
            cursos.

    Returns:
        MonitorAssignmentResponse: Dados da monitoria atualizada.
    """
    updated_monitor_assignment = await monitor_assignment_service.update(
        monitor_assignment_id, monitor_assignment_request
    )
    return updated_monitor_assignment


@api_router.delete(
    path="/{monitor_assignment_id}",
    name="Excluir Monitoria",
    description="Exclui uma monitoria existente.",
    response_description="Monitoria excluída com sucesso.",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_monitor_assignment(
    monitor_assignment_service: MonitorAssignmentService = Depends(
        get_monitor_assignment_service
    ),
    monitor_assignment_id: str = Path(
        ..., description="ID da monitoria a ser excluída."
    ),
) -> None:
    """Exclui uma monitoria existente.

    A rota recebe o identificador da monitoria a ser excluída e delega a
    exclusão para a camada de serviço, que é responsável por remover o
    professor do sistema.

    Args:
        monitor_assignment_id: Identificador numérico da monitoria a ser excluída.
        monitor_assignment_service: Dependência injetada com as regras de negócio de
            cursos.

    Returns:
        None: A resposta não contém conteúdo.
    """
    await monitor_assignment_service.delete(monitor_assignment_id)
    return None

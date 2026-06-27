from http import HTTPStatus

from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Params

from app.schemas.classroom_schema import (
    ClassroomResponse,
    CreateClassroomRequest,
    UpdateClassroomRequest,
)
from app.services.classroom_service import ClassroomService
from app.api.dependencies.services import get_classroom_service
from app.schemas.custom_page import Page

api_router = APIRouter(prefix="/v1/turmas", tags=["Turmas"])


@api_router.post(
    path="/",
    response_model=ClassroomResponse,
    name="Criar Turma",
    description="Cria uma nova turma.",
    response_description="Turma criada com sucesso.",
    status_code=HTTPStatus.CREATED,
)
async def create_classroom(
    classroom_request: CreateClassroomRequest,
    classroom_service: ClassroomService = Depends(get_classroom_service),
) -> ClassroomResponse:
    """Cria uma nova turma.

    A rota recebe os dados validados do corpo da requisição e delega a criação
    da turma para a camada de serviço. O serviço é responsável por
    persistir a nova turma e retornar os dados da turma criada.

    Args:
        classroom_request: Dados necessários para criar uma nova turma.
        classroom_service: Dependência injetada com as regras de negócio de
            turmas.

    Returns:
        ClassroomResponse: Dados da turma criada.
    """
    classroom = await classroom_service.create(classroom_request)
    return classroom


@api_router.get(
    path="/{classroom_code}",
    response_model=ClassroomResponse,
    name="Buscar Turma por Código",
    description="Busca os dados de uma turma específica pelo seu código.",
    response_description="Dados da turma encontrada.",
)
async def get_classroom_by_code(
    classroom_service: ClassroomService = Depends(get_classroom_service),
    classroom_code: str = Path(..., description="Código da turma a ser consultada"),
) -> ClassroomResponse:
    """Busca os dados de uma turma específica pelo seu código.

    A rota recebe o código da turma a ser consultada e delega a busca para a
    camada de serviço, que é responsável por recuperar os dados da turma do
    sistema.

    Args:
        classroom_code: Código da turma a ser consultada.
        classroom_service: Dependência injetada com as regras de negócio de
            turmas.
    Returns:
        ClassroomResponse: Dados da turma encontrada.
    """
    classroom = await classroom_service.get_by_cod(classroom_code)
    return classroom


@api_router.get(
    path="/",
    response_model=Page[ClassroomResponse],
    name="Listar Turmas",
    description="Retorna uma lista paginada de turmas.",
    response_description="Lista de turmas paginada.",
)
async def list_classrooms(
    classroom_service: ClassroomService = Depends(get_classroom_service),
    params: Params = Depends(),
) -> Page[ClassroomResponse]:
    """Lista as turmas cadastradas.

    Esta rota consulta a camada de serviço para obter a lista de turmas
    persistidos e devolve o resultado paginado.

    Args:
        params: Parâmetros de paginação.
        classroom_service: Dependência injetada com as regras de negócio de
            turmas.

    Returns:
        Page[ClassroomResponse]: Página contendo a lista de turmas.
    """
    classrooms = await classroom_service.list_all(params)
    return classrooms


@api_router.patch(
    path="/{classroom_code}",
    response_model=ClassroomResponse,
    name="Atualizar Turma",
    description="Atualiza os dados de uma turma existente.",
    response_description="Turma atualizada com sucesso.",
)
async def update_classroom(
    classroom_request: UpdateClassroomRequest,
    classroom_service: ClassroomService = Depends(get_classroom_service),
    classroom_code: str = Path(..., description="Código da turma a ser atualizada"),
) -> ClassroomResponse:
    """Atualiza os dados de uma turma existente.

    A rota recebe o código da turma a ser atualizada e os dados validados do
    corpo da requisição. Ela delega a atualização para a camada de serviço, que
    é responsável por persistir as alterações e retornar os dados da turma
    atualizada.

    Args:
        classroom_code: Código da turma a ser atualizada.
        classroom_request: Dados para atualizar a turma.
        classroom_service: Dependência injetada com as regras de negócio de
            turmas.

    Returns:
        ClassroomResponse: Dados da turma atualizada.
    """
    classroom = await classroom_service.update(classroom_code, classroom_request)
    return classroom


@api_router.delete(
    path="/{classroom_code}",
    status_code=HTTPStatus.NO_CONTENT,
    name="Excluir Turma",
    description="Exclui uma turma existente.",
    response_description="Turma excluída com sucesso.",
)
async def delete_classroom(
    classroom_service: ClassroomService = Depends(get_classroom_service),
    classroom_code: str = Path(..., description="Código da turma a ser excluída"),
) -> None:
    """Exclui uma turma existente.

    A rota recebe o código da turma a ser excluída e delega a exclusão para a
    camada de serviço, que é responsável por remover a turma do sistema.

    Args:
        classroom_code: Código da turma a ser excluída.
        classroom_service: Dependência injetada com as regras de negócio de
            turmas.
        Returns:
        None
    """
    await classroom_service.delete(classroom_code)

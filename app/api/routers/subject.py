from http import HTTPStatus

from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Page, Params

from app.api.dependencies.services import get_subject_service
from app.schemas.subject_schema import (
    CreateSubjectRequest,
    SubjectResponse,
    UpdateSubjectRequest,
)
from app.services.subject_service import SubjectService

api_router = APIRouter(prefix="/v1/disciplinas", tags=["Disciplinas"])


@api_router.post(
    path="/",
    response_model=SubjectResponse,
    name="Criar Disciplina",
    description="Cria uma nova disciplina.",
    response_description="Disciplina criada com sucesso.",
    status_code=HTTPStatus.CREATED,
)
async def create_subject(
    subject_request: CreateSubjectRequest,
    service: SubjectService = Depends(get_subject_service),
) -> SubjectResponse:
    """Cria uma nova disciplina.

    A rota recebe os dados validados do corpo da requisição e delega a criação
    da disciplina para a camada de serviço. O serviço é responsável por
    persistir a nova disciplina e retornar os dados da disciplina criada.

    Args:
        subject_request: Dados necessários para criar uma nova disciplina.
        subject_service: Dependência injetada com as regras de negócio de
            disciplinas.

    Returns:
        SubjectResponse: Dados da disciplina criada.
    """
    return await service.create(subject_request)


@api_router.get(
    path="/",
    response_model=Page[SubjectResponse],
    name="Listar Disciplinas",
    description="Retorna uma lista paginada de disciplinas.",
    response_description="Lista de disciplinas paginada.",
)
async def list_subjects(
    subject_service: SubjectService = Depends(get_subject_service),
    params: Params = Depends(),
) -> Page[SubjectResponse]:
    """Lista as disciplinas cadastradas.

    Esta rota consulta a camada de serviço para obter a lista de disciplinas
    persistidos e devolve o resultado paginado.

    Args:
        subject_service: Dependência injetada com as regras de negócio de
            disciplinas.
        params: Parâmetros de paginação extraídos da query string."""
    return await subject_service.list_all(params)


@api_router.patch(
    path="/{subject_code}",
    response_model=SubjectResponse,
    name="Atualizar Disciplina",
    description="Atualiza os dados de uma disciplina existente.",
    response_description="Disciplina atualizada com sucesso.",
)
async def update_subject(
    subject_request: UpdateSubjectRequest,
    subject_service: SubjectService = Depends(get_subject_service),
    subject_code: str = Path(..., description="Código da disciplina a ser atualizada"),
) -> SubjectResponse:
    """Atualiza os dados de uma disciplina existente.

    A rota recebe o código da disciplina a ser atualizada e os dados validados do
    corpo da requisição. Ela delega a atualização da disciplina para a camada
    de serviço, que é responsável por persistir as alterações e retornar os
    dados da disciplina atualizada.

    Args:
        subject_code: Código da disciplina a ser atualizada.
        subject_request: Dados para atualizar a disciplina.
        subject_service: Dependência injetada com as regras de negócio de
            disciplinas.

    Returns:
        SubjectResponse: Dados da disciplina atualizada.
    """
    subject = await subject_service.update(subject_code, subject_request)
    return subject


@api_router.get(
    path="/{subject_code}",
    response_model=SubjectResponse,
    name="Buscar Disciplina por Código",
    description="Retorna os dados de uma disciplina específica pelo seu código.",
    response_description="Dados da disciplina encontrada.",
)
async def get_subject_by_code(
    subject_service: SubjectService = Depends(get_subject_service),
    subject_code: str = Path(..., description="Código da disciplina a ser consultada"),
) -> SubjectResponse:
    """Busca os dados de uma disciplina específica pelo seu código.

    A rota recebe o código da disciplina a ser buscada e delega a consulta para a
    camada de serviço. O serviço é responsável por recuperar os dados da
    disciplina e retorná-los.

    Args:
        subject_code: Código da disciplina a ser buscada.
        subject_service: Dependência injetada com as regras de negócio de
            disciplinas.
    Returns:
        SubjectResponse: Dados da disciplina encontrada.
    """
    subject = await subject_service.get_by_id(subject_code)
    return subject


@api_router.delete(
    path="/{subject_code}",
    status_code=HTTPStatus.NO_CONTENT,
    name="Excluir Disciplina",
    description="Exclui uma disciplina existente.",
    response_description="Disciplina excluída com sucesso.",
)
async def delete_subject(
    subject_service: SubjectService = Depends(get_subject_service),
    subject_code: str = Path(..., description="Código da disciplina a ser excluída"),
) -> None:
    """Exclui uma disciplina existente.

    A rota recebe o código da disciplina a ser excluída e delega a exclusão para a
    camada de serviço, que é responsável por remover a disciplina do sistema.

    Args:
        subject_code: Código da disciplina a ser excluída.
        subject_service: Dependência injetada com as regras de negócio de
            disciplinas.
    Returns:
        None
    """
    await subject_service.delete(subject_code)

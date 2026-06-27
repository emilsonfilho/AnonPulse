from http import HTTPStatus

from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Page, Params

from app.api.dependencies.services import get_student_service
from app.schemas.student_schema import (
    CreateStudentRequest,
    StudentResponse,
    UpdateStudentRequest,
)
from app.services.student_service import StudentService

api_router = APIRouter(prefix="/v1/estudantes", tags=["Estudantes"])


@api_router.post(
    path="/",
    response_model=StudentResponse,
    name="Criar Estudante",
    description="Cria um novo estudante.",
    response_description="Estudante criado com sucesso.",
    status_code=HTTPStatus.CREATED,
)
async def create_student(
    student_request: CreateStudentRequest,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """Cria um novo estudante.

    A rota recebe os dados validados do corpo da requisição e delega a criação
    do estudante para a camada de serviço. O serviço é responsável por
    persistir o novo estudante e retornar os dados do estudante criado.

    Args:
        student_request: Dados necessários para criar um novo estudante.
        student_service: Dependência injetada com as regras de negócio de
            estudantes.

    Returns:
        StudentResponse: Dados do estudante criado.
    """
    return await service.create(student_request)


@api_router.get(
    path="/",
    response_model=Page[StudentResponse],
    name="Listar Estudantes",
    description="Retorna uma lista paginada de estudantes.",
    response_description="Lista de estudantes paginada.",
)
async def list_students(
    student_service: StudentService = Depends(get_student_service),
    params: Params = Depends(),
) -> Page[StudentResponse]:
    """Lista os estudantes cadastrados.

    Esta rota consulta a camada de serviço para obter a lista de estudantes
    persistidos e devolve o resultado paginado.

    Args:
        student_service: Dependência injetada com as regras de negócio de
            estudantes.
        params: Parâmetros de paginação extraídos da query string."""
    return await student_service.list_all(params)


@api_router.patch(
    path="/{student_id}",
    response_model=StudentResponse,
    name="Atualizar Estudante",
    description="Atualiza os dados de um estudante existente.",
    response_description="Estudante atualizado com sucesso.",
)
async def update_student(
    student_request: UpdateStudentRequest,
    student_service: StudentService = Depends(get_student_service),
    student_id: str = Path(..., description="ID do estudante a ser atualizado"),
) -> StudentResponse:
    """Atualiza os dados de um estudante existente.

    A rota recebe o ID do estudante a ser atualizado e os dados validados do
    corpo da requisição. Ela delega a atualização do estudante para a camada
    de serviço, que é responsável por persistir as alterações e retornar os
    dados do estudante atualizado.

    Args:
        student_id: ID do estudante a ser atualizado.
        student_request: Dados para atualizar o estudante.
        student_service: Dependência injetada com as regras de negócio de
            estudantes.

    Returns:
        StudentResponse: Dados do estudante atualizado.
    """
    student = await student_service.update(student_id, student_request)
    return student


@api_router.get(
    path="/{student_id}",
    response_model=StudentResponse,
    name="Buscar Estudante por ID",
    description="Retorna os dados de um estudante específico pelo seu ID.",
    response_description="Dados do estudante encontrada.",
)
async def get_student_by_id(
    student_service: StudentService = Depends(get_student_service),
    student_id: str = Path(..., description="ID do estudante a ser consultado"),
) -> StudentResponse:
    """Busca os dados de um estudante específico pelo seu ID.

    A rota recebe o ID do estudante a ser buscado e delega a consulta para a
    camada de serviço. O serviço é responsável por recuperar os dados do
    estudante e retorná-los.

    Args:
        student_id: ID do estudante a ser buscado.
        student_service: Dependência injetada com as regras de negócio de
            estudantes.
    Returns:
        StudentResponse: Dados do estudante encontrada.
    """
    student = await student_service.get_by_id(student_id)
    return student


@api_router.delete(
    path="/{student_id}",
    status_code=HTTPStatus.NO_CONTENT,
    name="Excluir Estudante",
    description="Exclui um estudante existente.",
    response_description="Estudante excluído com sucesso.",
)
async def delete_student(
    student_service: StudentService = Depends(get_student_service),
    student_id: str = Path(..., description="ID do estudante a ser excluído"),
) -> None:
    """Exclui um estudante existente.

    A rota recebe o ID do estudante a ser excluído e delega a exclusão para a
    camada de serviço, que é responsável por remover o estudante do sistema.

    Args:
        student_id: ID do estudante a ser excluído.
        student_service: Dependência injetada com as regras de negócio de
            estudantes.
    Returns:
        None
    """
    await student_service.delete(student_id)

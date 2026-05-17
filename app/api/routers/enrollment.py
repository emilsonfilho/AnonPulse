from http import HTTPStatus

from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Page, Params

from app.schemas.enrollment_schema import (
    CreateEnrollmentRequest,
    EnrollmentResponse,
    UpdateEnrollmentRequest,
)
from app.services.enrollment_service import EnrollmentService
from app.api.dependencies.services import get_enrollment_service

api_router = APIRouter(prefix="/v1/matriculas", tags=["Matrículas"])


@api_router.post(
    path="/",
    response_model=EnrollmentResponse,
    name="Criar Matrícula",
    description="Cria uma nova matrícula.",
    response_description="Matrícula criada com sucesso.",
    status_code=HTTPStatus.CREATED,
)
async def create_enrollment(
    enrollment_request: CreateEnrollmentRequest,
    enrollment_service: EnrollmentService = Depends(get_enrollment_service),
) -> EnrollmentResponse:
    """Cria uma nova matrícula.

    A rota recebe os dados validados do corpo da requisição e delega a criação
    da matrícula para a camada de serviço. O serviço é responsável por
    persistir a nova matrícula e retornar os dados da matrícula criada.

    Args:
        enrollment_request: Dados necessários para criar uma nova matrícula.
        enrollment_service: Dependência injetada com as regras de negócio de
            cursos.

    Returns:
        EnrollmentResponse: Dados da matrícula criada.
    """
    enrollment = await enrollment_service.create(enrollment_request)
    return enrollment


@api_router.get(
    path="/",
    response_model=Page[EnrollmentResponse],
    name="Listar Matrículas",
    description="Retorna uma lista paginada de matrículas.",
    response_description="Lista de matrículas paginada.",
)
async def list_enrollments(
    enrollment_service: EnrollmentService = Depends(get_enrollment_service),
    params: Params = Depends(),
) -> Page[EnrollmentResponse]:
    """Lista as matrículas cadastradas.

    Esta rota consulta a camada de serviço para obter a lista de matrículas
    persistidas e devolve o resultado paginado.

    Args:
        params: Parâmetros de paginação.
        enrollment_service: Dependência injetada com as regras de negócio de
            cursos.

    Returns:
        Page[EnrollmentResponse]: Página contendo a lista de matrículas.
    """
    return await enrollment_service.list_all(params)


@api_router.get(
    path="/{enrollment_id}",
    response_model=EnrollmentResponse,
    name="Buscar Matrícula por ID",
    description="Retorna uma matrícula específica pelo seu ID.",
    response_description="Dados da matrícula encontrada.",
)
async def get_enrollment_by_id(
    enrollment_service: EnrollmentService = Depends(get_enrollment_service),
    enrollment_id: int = Path(
        ..., description="Identificador numérico da matrícula a ser consultada."
    ),
) -> EnrollmentResponse:
    """Busca uma matrícula específica a partir do identificador.

    A rota recebe o identificador numérico da matrícula a ser consultada e
    delega a busca para a camada de serviço, que é responsável por retornar os
    dados da matrícula encontrada.

    Args:
        enrollment_id: Identificador numérico da matrícula a ser consultada.
        enrollment_service: Dependência injetada com as regras de negócio de
            cursos.

    Returns:
        EnrollmentResponse: Dados da matrícula encontrada.
    """
    enrollment = await enrollment_service.get_by_id(enrollment_id)
    return enrollment


@api_router.patch(
    path="/{enrollment_id}",
    response_model=EnrollmentResponse,
    name="Atualizar Matrícula",
    description="Atualiza os dados de uma matrícula existente.",
    response_description="Matrícula atualizada com sucesso.",
)
async def update_enrollment(
    enrollment_request: UpdateEnrollmentRequest,
    enrollment_service: EnrollmentService = Depends(get_enrollment_service),
    enrollment_id: int = Path(
        ..., description="Identificador numérico da matrícula a ser atualizada."
    ),
) -> EnrollmentResponse:
    """Atualiza os dados de uma matrícula existente.

    A rota recebe o identificador da matrícula a ser atualizada e os dados
    validados do corpo da requisição. Ela delega a atualização para a camada de
    serviço, que é responsável por persistir as alterações e retornar os dados
    da matrícula atualizada.

    Args:
        enrollment_id: Identificador numérico da matrícula a ser atualizada.
        enrollment_request: Dados para atualizar a matrícula.
        enrollment_service: Dependência injetada com as regras de negócio de
            cursos.

    Returns:
        EnrollmentResponse: Dados da matrícula atualizada.
    """
    updated_enrollment = await enrollment_service.update(
        enrollment_id, enrollment_request
    )
    return updated_enrollment


@api_router.delete(
    path="/{enrollment_id}",
    name="Excluir Matrícula",
    description="Exclui uma matrícula existente.",
    response_description="Matrícula excluída com sucesso.",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_enrollment(
    enrollment_service: EnrollmentService = Depends(get_enrollment_service),
    enrollment_id: int = Path(
        ..., description="Identificador numérico da matrícula a ser excluída."
    ),
) -> None:
    """Exclui uma matrícula existente.

    A rota recebe o identificador da matrícula a ser excluída e delega a
    exclusão para a camada de serviço, que é responsável por remover o
    professor do sistema.

    Args:
        enrollment_id: Identificador numérico da matrícula a ser excluída.
        enrollment_service: Dependência injetada com as regras de negócio de
            cursos.

    Returns:
        None: A resposta não contém conteúdo.
    """
    await enrollment_service.delete(enrollment_id)
    return None

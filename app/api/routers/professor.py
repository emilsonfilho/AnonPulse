from http import HTTPStatus

from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Params

from app.schemas.professor_schema import (
    CreateProfessorRequest,
    ProfessorResponse,
    UpdateProfessorRequest,
)
from app.services.professor_service import ProfessorService
from app.api.dependencies.services import get_professor_service
from app.schemas.custom_page import Page

api_router = APIRouter(prefix="/v1/professores", tags=["Professores"])


@api_router.post(
    path="/",
    response_model=ProfessorResponse,
    name="Criar Professor",
    description="Cria um novo professor.",
    response_description="Professor criado com sucesso.",
    status_code=HTTPStatus.CREATED,
)
async def create_professor(
    professor_request: CreateProfessorRequest,
    professor_service: ProfessorService = Depends(get_professor_service),
) -> ProfessorResponse:
    """Cria um novo professor.

    A rota recebe os dados validados do corpo da requisição e delega a criação
    do professor para a camada de serviço. O serviço é responsável por
    persistir o novo professor e retornar os dados do professor criado.

    Args:
        professor_request: Dados necessários para criar um novo professor.
        professor_service: Dependência injetada com as regras de negócio de
            cursos.

    Returns:
        ProfessorResponse: Dados do professor criado.
    """
    professor = await professor_service.create(professor_request)
    return professor


@api_router.get(
    path="/",
    response_model=Page[ProfessorResponse],
    name="Listar Professores",
    description="Retorna uma lista paginada de professores.",
    response_description="Lista de professores paginada.",
)
async def list_professores(
    professor_service: ProfessorService = Depends(get_professor_service),
    params: Params = Depends(),
) -> Page[ProfessorResponse]:
    """Lista os professores cadastrados.

    Esta rota consulta a camada de serviço para obter a lista de professores
    persistidos e devolve o resultado paginado.

    Args:
        params: Parâmetros de paginação.
        professor_service: Dependência injetada com as regras de negócio de
            cursos.

    Returns:
        Page[ProfessorResponse]: Página contendo a lista de professores.
    """
    return await professor_service.list_all(params)


@api_router.get(
    path="/{professor_id}",
    response_model=ProfessorResponse,
    name="Buscar Professor por ID",
    description="Retorna um professor específico pelo seu ID.",
    response_description="Dados do professor encontrado.",
)
async def get_professor_by_id(
    professor_service: ProfessorService = Depends(get_professor_service),
    professor_id: str = Path(
        ..., description="Identificador do professor a ser consultado."
    ),
) -> ProfessorResponse:
    """Busca um professor específico a partir do identificador.

    A rota recebe o identificador do professor a ser consultado e
    delega a busca para a camada de serviço, que é responsável por retornar os
    dados do professor encontrado.

    Args:
        professor_id: Identificador do professor a ser consultado.
        professor_service: Dependência injetada com as regras de negócio de
            cursos.

    Returns:
        ProfessorResponse: Dados do professor encontrado.
    """
    professor = await professor_service.get_by_id(professor_id)
    return professor


@api_router.patch(
    path="/{professor_id}",
    response_model=ProfessorResponse,
    name="Atualizar Professor",
    description="Atualiza os dados de um professor existente.",
    response_description="Professor atualizado com sucesso.",
)
async def update_professor(
    professor_request: UpdateProfessorRequest,
    professor_service: ProfessorService = Depends(get_professor_service),
    professor_id: str = Path(
        ..., description="Identificador numérico do professor a ser atualizado."
    ),
) -> ProfessorResponse:
    """Atualiza os dados de um professor existente.

    A rota recebe o identificador do professor a ser atualizado e os dados
    validados do corpo da requisição. Ela delega a atualização para a camada de
    serviço, que é responsável por persistir as alterações e retornar os dados
    do professor atualizado.

    Args:
        professor_id: Identificador numérico do professor a ser atualizado.
        professor_request: Dados para atualizar o professor.
        professor_service: Dependência injetada com as regras de negócio de
            cursos.

    Returns:
        ProfessorResponse: Dados do professor atualizado.
    """
    updated_professor = await professor_service.update(professor_id, professor_request)
    return updated_professor


@api_router.delete(
    path="/{professor_id}",
    name="Excluir Professor",
    description="Exclui um professor existente.",
    response_description="Professor excluído com sucesso.",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_professor(
    professor_service: ProfessorService = Depends(get_professor_service),
    professor_id: str = Path(
        ..., description="Identificador numérico do professor a ser excluído."
    ),
) -> None:
    """Exclui um professor existente.

    A rota recebe o identificador do professor a ser excluído e delega a
    exclusão para a camada de serviço, que é responsável por remover o
    professor do sistema.

    Args:
        professor_id: Identificador numérico do professor a ser excluído.
        professor_service: Dependência injetada com as regras de negócio de
            cursos.

    Returns:
        None: A resposta não contém conteúdo.
    """
    await professor_service.delete(professor_id)
    return None

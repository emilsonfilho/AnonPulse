from datetime import date
from http import HTTPStatus

from fastapi import APIRouter, Depends, Path, Query
from fastapi_pagination import Params

from app.schemas.feedback_schema import (
    CreateFeedbackRequest,
    FeedbackResponse,
    FeedbackSubjectReportResponse,
    UpdateFeedbackRequest,
)
from app.services.feedback_service import FeedbackService
from app.api.dependencies.services import get_feedback_service
from app.schemas.custom_page import Page

api_router = APIRouter(prefix="/v1/feedbacks", tags=["Feedbacks"])


@api_router.get(
    path="/count",
    response_model=dict[str, int],
    name="Contar Feedbacks",
    description="Retorna a contagem total de feedbacks registrados.",
    response_description="Número total de feedbacks.",
)

async def count_feedbacks(
    feedback_service: FeedbackService = Depends(get_feedback_service),
) -> dict[str, int]:
    """Conta o total de feedbacks registrados no sistema.

    Esta rota consulta a camada de serviço para obter a quantidade total de
    feedbacks persistidos e devolve o resultado em um dicionário simples.

    Args:
        feedback_service: Dependência injetada com as regras de negócio de
            feedback.

    Returns:
        dict[str, int]: Dicionário contendo a chave ``total_feedbacks`` com o
        número total de registros.
    """
    total_feedbacks = await feedback_service.count_feedbacks()

    return {"total_feedbacks": total_feedbacks}


@api_router.post(
    path="/",
    response_model=FeedbackResponse,
    name="Criar Feedback",
    description="Cria um novo feedback para um monitor específico.",
    response_description="Feedback criado com sucesso.",
    status_code=HTTPStatus.CREATED,
)
async def create_feedback(
    feedback_request: CreateFeedbackRequest,
    feedback_service: FeedbackService = Depends(get_feedback_service),
) -> FeedbackResponse:
    """Cria um novo feedback.

    A rota recebe os dados validados do corpo da requisição e delega a criação
    para a camada de serviço.

    Args:
        feedback_request: Payload com os dados necessários para criação do
            feedback.
        feedback_service: Dependência injetada com as regras de negócio de
            feedback.

    Returns:
        FeedbackResponse: Objeto com os dados do feedback criado.
    """

    return await feedback_service.create(feedback_request)


@api_router.get(
    path="/search",
    response_model=Page[FeedbackResponse],
    name="Buscar Feedbacks por Texto",
    description="Busca feedbacks por texto parcial no campo de mensagem.",
    response_description="Resultados de feedbacks correspondentes ao termo de busca.",
)
async def search_feedbacks(
    q: str = Query(..., min_length=1, description="Termo parcial para buscar no texto do feedback"),
    params: Params = Depends(),
    feedback_service: FeedbackService = Depends(get_feedback_service),
) -> Page[FeedbackResponse]:
    """Pesquisa feedbacks pelo texto fornecido e retorna resultados paginados."""
    return await feedback_service.search(q, params)


@api_router.get(
    path="/filter",
    response_model=Page[FeedbackResponse],
    name="Filtrar Feedbacks por Data",
    description="Filtra feedbacks por intervalo de data ou por ano de criação.",
    response_description="Resultados de feedbacks filtrados por data ou ano.",
)
async def filter_feedbacks(
    params: Params = Depends(),
    start_date: date | None = Query(
        None,
        description="Data inicial do intervalo no formato YYYY-MM-DD",
    ),
    end_date: date | None = Query(
        None,
        description="Data final do intervalo no formato YYYY-MM-DD",
    ),
    year: int | None = Query(
        None,
        description="Ano de criação para filtrar feedbacks",
        ge=1900,
    ),
    feedback_service: FeedbackService = Depends(get_feedback_service),
) -> Page[FeedbackResponse]:
    """Filtra feedbacks por data inicial, final ou por ano."""
    return await feedback_service.list_by_date(
        params=params,
        start_date=start_date,
        end_date=end_date,
        year=year,
    )


@api_router.get(
    path="/reports/subjects",
    response_model=Page[FeedbackSubjectReportResponse],
    name="Relatório de Feedbacks por Disciplina",
    description="Gera um relatório paginado de quantidade de feedbacks por disciplina.",
    response_description="Quantidade de feedbacks agrupada por disciplina.",
)
async def report_feedbacks_by_subject(
    params: Params = Depends(),
    feedback_service: FeedbackService = Depends(get_feedback_service),
) -> Page[FeedbackSubjectReportResponse]:
    """Relatório multi-entidade de feedbacks agrupados por disciplina."""
    return await feedback_service.report_by_subject(params)


@api_router.get(
    path="/{feedback_id}",
    response_model=FeedbackResponse,
    name="Buscar Feedback por ID",
    description="Retorna um feedback específico pelo seu ID.",
)
async def get_feedback_by_id(
    feedback_id: int = Path(..., description="ID numérico do feedback"),
    feedback_service: FeedbackService = Depends(get_feedback_service),
) -> FeedbackResponse:
    """Busca um feedback específico a partir do identificador.

    Args:
        feedback_id: Identificador numérico do feedback a ser consultado.
        feedback_service: Dependência injetada com as regras de negócio de
            feedback.

    Returns:
        FeedbackResponse: Dados completos do feedback encontrado.
    """
    return await feedback_service.get_by_id(feedback_id)


@api_router.get(
    path="/",
    response_model=Page[FeedbackResponse],
    name="Listar Feedbacks",
    description="Lista os feedbacks registrados com suporte a paginação.",
    response_description="Lista paginada de feedbacks.",
)
async def list_feedbacks(
    params: Params = Depends(),
    q: str | None = None,
    feedback_service: FeedbackService = Depends(get_feedback_service),
):
    """Lista feedbacks com suporte a paginação.

    A paginação é controlada pelos parâmetros ``page`` e ``size``. O cálculo
    de deslocamento (offset) é feito localmente e os itens são obtidos via
    camada de serviço.

    Args:
        page: Número da página (inicia em 1).
        size: Quantidade de itens por página (entre 1 e 100).
        feedback_service: Dependência injetada com as regras de negócio de
            feedback.

    Returns:
        Page[FeedbackResponse]: Estrutura paginada contendo os feedbacks da
        página solicitada.
    """

    if q:
        return await feedback_service.search(q, params)

    return await feedback_service.list_all(params)


@api_router.patch(
    path="/{feedback_id}",
    response_model=FeedbackResponse,
    name="Atualizar Feedback",
    description="Atualiza um feedback existente com base no ID fornecido.",
    response_description="Feedback atualizado com sucesso.",
)
async def update_feedback(
    feedback_request: UpdateFeedbackRequest,
    feedback_id: int = Path(..., description="ID do feedback a ser atualizado"),
    feedback_service: FeedbackService = Depends(get_feedback_service),
) -> FeedbackResponse:
    """Atualiza um feedback existente.

    A rota recebe o identificador do feedback e os campos de atualização.
    Após a operação, realiza uma nova consulta para retornar o estado atual do
    recurso.

    Args:
        feedback_request: Payload com os dados permitidos para atualização.
        feedback_id: Identificador do feedback que será atualizado.
        feedback_service: Dependência injetada com as regras de negócio de
            feedback.

    Returns:
        FeedbackResponse: Dados atualizados do feedback.
    """

    feedback = await feedback_service.update(feedback_id, feedback_request)
    return feedback


@api_router.delete(
    path="/{feedback_id}",
    name="Deletar Feedback",
    description="Deleta um feedback existente com base no ID fornecido.",
    response_description="Feedback deletado com sucesso.",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_feedback(
    feedback_id: int = Path(..., description="ID do feedback a ser deletado"),
    feedback_service: FeedbackService = Depends(get_feedback_service),
) -> None:
    """Remove um feedback existente.

    Args:
        feedback_id: Identificador do feedback que será removido.
        feedback_service: Dependência injetada com as regras de negócio de
            feedback.

    Returns:
        None: Resposta sem corpo (HTTP 204) quando a remoção é concluída.
    """

    await feedback_service.delete(feedback_id)

    return None

@api_router.get("/student/{registration}", response_model=Page[FeedbackResponse])
async def list_student_feedbacks(
    registration: str,
    params: Params = Depends(),
    service: FeedbackService = Depends(get_feedback_service)
):
    """Rota Complexa: Lista todos os feedbacks efetuados por um estudante de forma anônima e detalhada."""
    return await service.list_by_student(raw_registration=registration, params=params)

@api_router.get("/monitor/{registration}", response_model=Page[FeedbackResponse])
async def list_monitor_feedbacks(
    registration: str,
    params: Params = Depends(),
    service: FeedbackService = Depends(get_feedback_service)
):
    """Rota Complexa: Lista todos os feedbacks recebidos por um monitor de forma anônima e detalhada."""
    return await service.list_by_monitor(monitor_registration=registration, params=params)
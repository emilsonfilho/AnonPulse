from http import HTTPStatus

from fastapi import APIRouter, Depends, Path
from fastapi.responses import StreamingResponse
from fastapi_pagination import Page, paginate, Params

from app.schemas.feedback_schema import (
    CreateFeedbackRequest,
    FeedbackResponse,
    UpdateFeedbackRequest,
)
from app.services.exportacao_service import gerar_bytes_csv, gerar_zip_streaming
from app.services.feedback_service import FeedbackService

api_router = APIRouter(prefix="/v1/feedbacks", tags=["Feedbacks"])


@api_router.get(
    path="/count",
    response_model=dict[str, int],
    name="Contar Feedbacks",
    description="Retorna a contagem total de feedbacks registrados.",
    response_description="Número total de feedbacks.",
)
async def count_feedbacks(
    feedback_service: FeedbackService = Depends(FeedbackService),
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
    total_feedbacks = feedback_service.count_feedbacks()

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
    feedback_service: FeedbackService = Depends(FeedbackService),
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

    return feedback_service.criar_feedback(feedback_request)


@api_router.get(
    path="/{feedback_id}",
    response_model=FeedbackResponse,
    name="Buscar Feedback por ID",
    description="Retorna um feedback específico pelo seu ID.",
)
async def get_feedback_by_id(
    feedback_id: int = Path(..., description="ID numérico do feedback"),
    feedback_service: FeedbackService = Depends(FeedbackService),
) -> FeedbackResponse:
    """Busca um feedback específico a partir do identificador.

    Args:
        feedback_id: Identificador numérico do feedback a ser consultado.
        feedback_service: Dependência injetada com as regras de negócio de
            feedback.

    Returns:
        FeedbackResponse: Dados completos do feedback encontrado.
    """
    return feedback_service.obter_feedback_por_id(feedback_id)


@api_router.get(
    path="/",
    response_model=Page[FeedbackResponse],
    name="Listar Feedbacks",
    description="Lista os feedbacks registrados com suporte a paginação.",
    response_description="Lista paginada de feedbacks.",
)
async def list_feedbacks(
    params: Params = Depends(),
    feedback_service: FeedbackService = Depends(FeedbackService),
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

    # TODO: Futuramente, terá que adicionar Query params aqui para filtrar por data, nota, etc.

    skip = (params.page - 1) * params.size

    items = feedback_service.obter_feedbacks(skip=skip, limit=params.size)

    return paginate(items)


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
    feedback_service: FeedbackService = Depends(FeedbackService),
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

    feedback_service.atualizar_feedback(feedback_id, feedback_request)

    return feedback_service.obter_feedback_por_id(feedback_id)


@api_router.delete(
    path="/{feedback_id}",
    name="Deletar Feedback",
    description="Deleta um feedback existente com base no ID fornecido.",
    response_description="Feedback deletado com sucesso.",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_feedback(
    feedback_id: int = Path(..., description="ID do feedback a ser deletado"),
    feedback_service: FeedbackService = Depends(FeedbackService),
) -> None:
    """Remove um feedback existente.

    Args:
        feedback_id: Identificador do feedback que será removido.
        feedback_service: Dependência injetada com as regras de negócio de
            feedback.

    Returns:
        None: Resposta sem corpo (HTTP 204) quando a remoção é concluída.
    """

    feedback_service.deletar_feedback(feedback_id=feedback_id)

    return None


@api_router.get(
    path="/exportar/csv",
    name="Exportar Feedbacks para CSV",
    description="Exporta os feedbacks registrados para um arquivo CSV.",
    response_description="Arquivo CSV contendo os feedbacks exportados.",
    response_class=StreamingResponse,
)
def export_feedbacks_csv() -> StreamingResponse:
    """Exporta feedbacks para um arquivo CSV em streaming.

    Returns:
        StreamingResponse: Fluxo de bytes no formato CSV com cabeçalho para
        download do arquivo ``feedbacks.csv``.
    """

    return StreamingResponse(
        gerar_bytes_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=feedbacks.csv"},
    )


@api_router.get(
    path="/exportar/zip",
    name="Exportar Feedbacks para ZIP",
    description="Exporta os feedbacks registrados para um arquivo ZIP contendo o CSV.",
    response_description="Arquivo ZIP contendo o CSV dos feedbacks exportados.",
    response_class=StreamingResponse,
)
def export_feedbacks_zip() -> StreamingResponse:
    """Exporta feedbacks para um arquivo ZIP contendo o CSV.

    Returns:
        StreamingResponse: Fluxo de bytes no formato ZIP com cabeçalho para
        download do arquivo ``feedbacks.zip``.
    """

    return StreamingResponse(
        gerar_zip_streaming(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=feedbacks.zip"},
    )

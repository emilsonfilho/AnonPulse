from fastapi import APIRouter, Query, Path
from fastapi.responses import FileResponse, StreamingResponse
from app.api.schemas.feedback_schema import (
    FeedbackResponse,
    CreateFeedbackRequest,
    UpdateFeedbackRequest,
)
from app.api.schemas.pagination_schema import PaginatedResponse
from http import HTTPStatus
from app.services.exportacao_service import gerar_bytes_csv, gerar_zip_streaming
from app.services.feedback_service import FeedbackService

api_router = APIRouter(prefix="/v1/feedbacks", tags=["Feedbacks"])
feedback_service = FeedbackService()


@api_router.get(
    path="/count",
    response_model=dict[str, int],
    name="Contar Feedbacks",
    description="Retorna a contagem total de feedbacks registrados.",
    response_description="Número total de feedbacks.",
)
async def count_feedbacks() -> dict[str, int]:
    """
    Endpoint para contar o número total de feedbacks registrados. Retorna um inteiro representando a contagem.
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
async def create_feedback(feedback_request: CreateFeedbackRequest) -> FeedbackResponse:
    """
    Endpoint para criar um novo feedback. Recebe os dados do feedback e retorna o feedback criado.
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
) -> FeedbackResponse:
    """Endpoint para buscar um feedback específico."""
    return feedback_service.obter_feedback_por_id(feedback_id)


@api_router.get(
    path="/",
    response_model=PaginatedResponse[FeedbackResponse],
    name="Listar Feedbacks",
    description="Lista os feedbacks registrados com suporte a paginação.",
    response_description="Lista paginada de feedbacks.",
)
async def list_feedbacks(
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
):
    """
    Endpoint para listar os feedbacks registrados com suporte a paginação. Retorna uma lista de feedbacks para a página solicitada.
    """
    skip = (page - 1) * size

    items = feedback_service.obter_feedbacks(skip=skip, limit=size)

    return PaginatedResponse(
        items=items,
        total=feedback_service.count_feedbacks(),  # TODO: O Membro 1 conectará a camada de persistência aqui futuramente para contar o total de feedbacks.
        limit=size,
        skip=skip,
    )


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
) -> FeedbackResponse:
    """Endpoint para atualizar um feedback existente. Recebe o ID do feedback a ser atualizado e os dados para atualização, retornando o feedback atualizado."""

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
) -> None:
    """Endpoint para deletar um feedback existente. Recebe o ID do feedback a ser deletado e remove o feedback correspondente."""

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
    """Endpoint para exportar os feedbacks registrados para um arquivo CSV. Retorna o arquivo CSV gerado."""

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
    """Endpoint para exportar os feedbacks registrados para um arquivo ZIP contendo o CSV. Retorna o arquivo ZIP gerado."""

    return StreamingResponse(
        gerar_zip_streaming(),
        media_type="text/zip",
        headers={"Content-Disposition": "attachment; filename=feedbacks.zip"},
    )

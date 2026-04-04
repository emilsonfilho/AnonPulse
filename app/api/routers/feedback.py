from fastapi import APIRouter, Query, Path
from app.models.feedback import Feedback
from app.api.schemas.feedback_schema import (
    FeedbackResponse,
    CreateFeedbackRequest,
    UpdateFeedbackRequest,
)
from app.api.schemas.pagination_schema import PaginatedResponse
from app.api.core.enums import HashAlgorithm, MessageType
from app.services.hash_service import HashService
from http import HTTPStatus

api_router = APIRouter(prefix="/v1/feedbacks", tags=["Feedbacks"])


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
    # TODO: O Membro 1 conectará a camada de persistência aqui futuramente. (Necesário o service de feedback para isso)
    # Exemplo: total_feedbacks = delta_repository.count_feedbacks()

    return {"total_feedbacks": 0}


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

    data = feedback_request.model_dump()

    identificador_aluno = data.pop("identificador_aluno")

    hash_gerado = HashService.generate_hash(identificador_aluno, HashAlgorithm.SHA256)

    data["hash_aluno"] = hash_gerado

    new_feedback = Feedback.model_validate(data)

    # TODO: O Membro 1 conectará a camada de persistência aqui futuramente.
    # Exemplo: delta_repository.insert(new_feedback)

    return FeedbackResponse.model_validate(new_feedback.model_dump())


@api_router.get(
    path="/{feedback_id}",
    response_model=FeedbackResponse,
    name="Buscar Feedback por ID",
    description="Retorna um feedback específico pelo seu ID.",
)
async def get_feedback(
    feedback_id: int = Path(..., description="ID numérico do feedback"),
) -> FeedbackResponse:
    """Endpoint para buscar um feedback específico."""
    # TODO: Membro 1 conectará -> delta_repository.get(feedback_id)
    # Exemplo temporário para não quebrar a API:
    pass


@api_router.get(
    path="/",
    response_model=PaginatedResponse[FeedbackResponse],
    name="Listar Feedbacks",
    description="Lista os feedbacks registrados com suporte a paginação.",
    response_description="Lista paginada de feedbacks.",
)
async def list_feedbacks(
    message_type: MessageType | None = Query(None, alias="type", description="Filtrar por tipo de mensagem"),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
):
    """
    Endpoint para listar os feedbacks registrados com suporte a paginação. Retorna uma lista de feedbacks para a página solicitada.
    """
    skip = (page - 1) * size

    return PaginatedResponse(
        items=[],  # TODO: O Membro 1 conectará a camada de persistência aqui futuramente para buscar os feedbacks com base no skip e size.
        total=0,  # TODO: O Membro 1 conectará a camada de persistência aqui futuramente para contar o total de feedbacks.
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
    data = feedback_request.model_dump(exclude_unset=True)
    # TODO: O Membro 1 conectará a camada de persistência aqui futuramente para buscar o feedback existente, aplicar as atualizações e salvar as alterações.
    pass


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

    # TODO: O Membro 1 conectará a camada de persistência aqui futuramente para deletar o feedback com base no ID fornecido.
    return None

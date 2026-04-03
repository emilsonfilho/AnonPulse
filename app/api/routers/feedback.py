from fastapi import APIRouter
from app.models.feedback import Feedback
from app.api.schemas.feedback_schema import FeedbackResponse, CreateFeedbackRequest
from app.api.core.enums import HashAlgorithm, MessageType
from app.services.hash_service import HashService
from http import HTTPStatus

api_router = APIRouter(prefix="/v1/feedbacks", tags=["Feedbacks"])


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

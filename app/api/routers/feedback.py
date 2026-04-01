from fastapi import APIRouter
from models.feedback import Feedback
from api.schemas.feedback_schema import FeedbackResponse, CreateFeedbackRequest
from api.core.enums import MessageType
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

    new_feedback = Feedback.model_validate(feedback_request.model_dump())

    return FeedbackResponse.model_validate(
        new_feedback.model_dump(exclude={"hash_aluno"})
    )

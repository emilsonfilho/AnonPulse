from datetime import date

from app.core.exceptions.custom_exceptions import FeedbackNotFoundException
from app.core.mapper import Mapper
from app.services.base_service import BaseService
from app.repositories.feedback_repository import FeedbackRepository
from app.schemas.feedback_schema import FeedbackResponse, CreateFeedbackRequest, UpdateFeedbackRequest
from app.models.feedback import Feedback

class FeedbackService(BaseService[Feedback, CreateFeedbackRequest, UpdateFeedbackRequest, FeedbackResponse]):
    def __init__(self, repository: FeedbackRepository) -> None:
        super().__init__(
            repository=repository,
            response_schema=FeedbackResponse,
            not_found_exception=FeedbackNotFoundException,
        )

    async def create(self, request: CreateFeedbackRequest) -> FeedbackResponse:
        feedback = Feedback(
            **request.model_dump(),
            created_at=date.today()
        )

        new_feedback = await self.repository.create(feedback)

        return Mapper.to_response(new_feedback, FeedbackResponse)
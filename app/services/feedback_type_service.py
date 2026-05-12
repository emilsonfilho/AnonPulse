from app.core.mapper import Mapper
from app.repositories.feedback_type_repository import FeedbackTypeRepository
from app.schemas.feedback_type_schema import FeedbackTypeResponse

class FeedbackTypeService:
    def __init__(self, repository: FeedbackTypeRepository) -> None:
        self.repository = repository

    async def list_all(self) -> list[FeedbackTypeResponse]:
        types = await self.repository.list_all()

        return [Mapper.to_response(type, FeedbackTypeResponse) for type in types]
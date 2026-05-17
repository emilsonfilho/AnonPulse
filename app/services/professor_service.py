from app.core.exceptions.custom_exceptions import ProfessorNotFoundException
from app.models.professor import Professor
from app.repositories.professor_repository import ProfessorRepository
from app.schemas.professor_schema import (
    CreateProfessorRequest,
    ProfessorResponse,
    UpdateProfessorRequest,
)
from app.services.base_service import BaseService


class ProfessorService(
    BaseService[
        Professor, CreateProfessorRequest, UpdateProfessorRequest, ProfessorResponse
    ]
):
    def __init__(self, repository: ProfessorRepository) -> None:
        super().__init__(
            repository=repository,
            response_schema=ProfessorResponse,
            not_found_exception=ProfessorNotFoundException,
        )

    async def create(self, request: CreateProfessorRequest) -> ProfessorResponse:
        return await super().create(request)

from app.core.exceptions.custom_exceptions import ProfessorAlreadyExistsException, ProfessorNotFoundException
from app.repositories.professor_repository import ProfessorRepository
from app.services.base_service import BaseService
from app.schemas.professor_schema import ProfessorResponse, CreateProfessorRequest, UpdateProfessorRequest
from app.models.professor import Professor

class ProfessorService(BaseService[Professor, CreateProfessorRequest, UpdateProfessorRequest, ProfessorResponse]):
    def __init__(self, repository: ProfessorRepository) -> None:
        super().__init(
            repository=repository,
            response_schema=ProfessorResponse,
            not_found_exception=ProfessorNotFoundException,
        )

    async def create(self, request: CreateProfessorRequest) -> ProfessorResponse:
        return await super().create(request)
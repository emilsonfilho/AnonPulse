from app.schemas.subject_schema import CreateSubjectRequest, UpdateSubjectRequest, SubjectResponse
from app.models import Subject
from app.core.exceptions.custom_exceptions import SubjectAlreadyExistsException, SubjectNotFoundException
from app.repositories.subject_repository import SubjectRepository
from app.services.base_service import BaseService

class SubjectService(BaseService[Subject, CreateSubjectRequest, UpdateSubjectRequest, SubjectResponse]):
    def __init__(self, repository: SubjectRepository) -> None:
        super().__init__(
            repository=repository,
            response_schema=SubjectResponse,
            not_found_exception=SubjectNotFoundException,
            already_exists_exception=SubjectAlreadyExistsException
        )

    async def create(self, request: CreateSubjectRequest) -> SubjectResponse:
        return await super().create(request, identifier_value=request.cod)
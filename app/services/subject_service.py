from fastapi_pagination import Params, Page

from app.schemas.subject_schema import CreateSubjectRequest, UpdateSubjectRequest, SubjectResponse
from app.models import Subject
from app.core.exceptions.custom_exceptions import SubjectAlreadyExistsExcepion, SubjectNotFoundException
from app.repositories.subject_repository import SubjectRepository

class SubjectService:
    def __init__(self, repository: SubjectRepository) -> None:
        self.repository = repository
    
    async def list_subjects(self, params: Params) -> Page[SubjectResponse]:
        page = await self.repository.list_all(params)

        page.items = [
            SubjectResponse.model_validate(subject) for subject in page
        ] 

        return page

    async def get_subject_by_code(self, code: str) -> SubjectResponse:
        subject = await self.repository.get_by_code(code)

        if not subject:
            raise SubjectNotFoundException()


    async def create(self, data: CreateSubjectRequest) -> SubjectResponse:
        subject_exists = await self.repository.get_by_code(data.cod)

        if (subject_exists):
            raise SubjectAlreadyExistsExcepion(
                f"Já existe uma disciplina com o código {data.cod}."
            )

        subject = Subject(**data.model_dump())
        new_subject = await self.repository.create(subject)

        return SubjectResponse.model_validate(new_subject)
    
    async def update_subject(self, code: str, request: UpdateSubjectRequest) -> SubjectResponse:
        subject_exists = await self.repository.get_by_code(code)

        if not subject_exists:
            raise SubjectNotFoundException()

        updated_subject = await self.repository.update(
            code,
            request.model_dump(exclude_unset=True)
        )

        return SubjectResponse.model_validate(updated_subject)
    
    async def delete_suject(self, code: str) -> None:
        subject_exists = await self.repository.get_by_code(code)

        if not subject_exists:
            raise SubjectNotFoundException()
        
        self.repository.delete(code)
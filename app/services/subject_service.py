from fastapi_pagination import Params, Page

from app.schemas.subject_schema import CreateSubjectRequest, UpdateSubjectRequest, SubjectResponse
from app.models import Subject
from app.core.exceptions.custom_exceptions import SubjectAlreadyExistsExcepion, SubjectNotFoundException
from app.core.mapper import Mapper
from app.repositories.subject_repository import SubjectRepository
from app.services.base_service import BaseService

class SubjectService(BaseService):
    def __init__(self, repository: SubjectRepository) -> None:
        self.repository = repository

    async def _get_subject_or_raise(self, code: str) -> Subject:
        return self.get_or_raise(
            lambda: self.repository.get_by_code(code),
            SubjectNotFoundException
        )
    
    async def list_subjects(self, params: Params) -> Page[SubjectResponse]:
        page = await self.repository.list_all(params)

        page.items = [
            Mapper.to_response(subject, SubjectResponse) for subject in page
        ] 

        return page

    async def get_subject_by_code(self, code: str) -> SubjectResponse:
        subject = await self._get_subject_or_raise(code)
        return Mapper.to_response(subject, SubjectResponse)


    async def create_subject(self, data: CreateSubjectRequest) -> SubjectResponse:
        subject_exists = await self.repository.get_by_code(data.cod)

        if (subject_exists):
            raise SubjectAlreadyExistsExcepion(
                f"Já existe uma disciplina com o código {data.cod}."
            )

        subject = Subject(**data.model_dump())
        new_subject = await self.repository.create(subject)

        return Mapper.to_response(new_subject, SubjectResponse)
    
    async def update_subject(self, code: str, request: UpdateSubjectRequest) -> SubjectResponse:
        self._get_subject_or_raise(code)

        updated_subject = await self.repository.update(
            code,
            request.model_dump(exclude_unset=True)
        )

        return Mapper.to_response(updated_subject, SubjectResponse)
    
    async def delete_suject(self, code: str) -> None:
        self._get_subject_or_raise(code) 
        self.repository.delete(code)
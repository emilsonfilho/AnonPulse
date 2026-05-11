from fastapi_pagination import Params, Page

from app.core.exceptions.custom_exceptions import ProfessorAlreadyExistsExcepion, ProfessorNotFoundException
from app.core.mapper import Mapper
from app.repositories.professor_repository import ProfessorRepository
from app.services.base_service import BaseService
from app.schemas.professor_schema import ProfessorResponse, CreateProfessorRequest, UpdateProfessorRequest
from app.models.professor import Professor

class ProfessorService(BaseService):
    def __init__(self, repository: ProfessorRepository) -> None:
        self.repository = repository

    async def _get_professor_or_raise(self, id: int) -> Professor:
        return self.get_or_raise(
            lambda: self.repository.get_by_id(id),
            ProfessorNotFoundException
        )

    async def list_professors(self, params: Params) -> Page[ProfessorResponse]:
        page = await self.repository.list_all(params)

        page.items = [
            Mapper.to_response(professor, ProfessorResponse) for professor in page
        ]

        return page

    async def create(self, data: CreateProfessorRequest) -> ProfessorResponse:
        professor = await self.repository.get_by_id(data.id)

        if professor:
            raise ProfessorAlreadyExistsExcepion()
        
        professor = Professor(**data.model_dump())
        new_professor = await self.repository.create(professor)
        
        return Mapper.to_response(new_professor, ProfessorResponse)
    
    async def get_professor_by_id(self, id: int) -> ProfessorResponse:
        professor = await self._get_professor_or_raise(id)
        return Mapper.to_response(professor, ProfessorResponse)

    async def update_professor(self, id: int, request: UpdateProfessorRequest) -> ProfessorResponse:
        await self._get_professor_or_raise(id)

        updated_professor = await self.repository.update(
            id,
            request.model_dump(exclude_unset=True)
        )

        return Mapper.to_response(updated_professor, ProfessorResponse)
    
    async def delete_professor(self, id: int) -> None:
        await self._get_professor_or_raise(id)
        await self.repository.delete(id)
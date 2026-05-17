from app.core.exceptions.custom_exceptions import (
    ClassroomAlreadyExistsException,
    ClassroomHasEnrollmentsException,
    ClassroomNotFoundException,
)
from app.models.classroom import Classroom
from app.repositories.classroom_repository import ClassroomRepository
from app.schemas.classroom_schema import (
    ClassroomResponse,
    CreateClassroomRequest,
    UpdateClassroomRequest,
)
from app.services.base_service import BaseService


class ClassroomService(
    BaseService[
        Classroom, CreateClassroomRequest, UpdateClassroomRequest, ClassroomResponse
    ]
):
    def __init__(self, repository: ClassroomRepository) -> None:
        super().__init__(
            repository=repository,
            response_schema=ClassroomResponse,
            not_found_exception=ClassroomNotFoundException,
            already_exists_exception=ClassroomAlreadyExistsException,
        )

    async def create(self, request: CreateClassroomRequest) -> ClassroomResponse:
        return await super().create(request, identifier_value=request.cod)

    async def delete(self, cod: str) -> None:
        classroom = await self.get_or_raise(cod)

        if classroom.enrollments:
            raise ClassroomHasEnrollmentsException(classroom.cod)

        await self.repository.delete(cod)

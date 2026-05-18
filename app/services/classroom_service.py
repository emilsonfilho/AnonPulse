"""Serviço de salas de aula.

Este módulo fornece a classe ClassroomService, responsável pela lógica de
negócio relacionada a turmas (classrooms).
"""

from app.core.exceptions.custom_exceptions import (
    ClassroomAlreadyExistsException,
    ClassroomHasEnrollmentsException,
    ClassroomNotFoundException,
)
from app.core.mapper import Mapper
from app.models.classroom import Classroom
from app.repositories.classroom_repository import ClassroomRepository
from app.schemas.classroom_schema import (
    ClassroomResponse,
    CreateClassroomRequest,
    UpdateClassroomRequest,
)
from app.services.base_service import BaseService
from fastapi_pagination import Params
from sqlalchemy.orm import joinedload, selectinload


class ClassroomService(
    BaseService[
        Classroom, CreateClassroomRequest, UpdateClassroomRequest, ClassroomResponse
    ]
):
    """Serviço para operações sobre Classroom.

    Herdando de BaseService, este serviço adiciona validações e métodos
    específicos como listagens por professor e por disciplina.
    """
    def __init__(self, repository: ClassroomRepository) -> None:
        """Inicializa o serviço com o repositório e opções de carregamento.

        Args:
            repository: Instância de ClassroomRepository usada para
                operações de persistência.
        """
        super().__init__(
            repository=repository,
            response_schema=ClassroomResponse,
            not_found_exception=ClassroomNotFoundException,
            already_exists_exception=ClassroomAlreadyExistsException,
            default_load_options=[
                joinedload(Classroom.subject),
                joinedload(Classroom.professor),
                selectinload(Classroom.enrollments)
            ]
        )

    async def create(self, request: CreateClassroomRequest) -> ClassroomResponse:
        """Cria uma nova classroom.

        O identificador usado para checagem de existência é o atributo
        `cod` do request.
        """

        return await super().create(request, identifier_value=request.cod)

    async def delete(self, cod: str) -> None:
        """Remove uma classroom pelo código.

        Antes de deletar, valida se existem matrículas associadas e levanta
        ClassroomHasEnrollmentsException quando houver.
        """

        classroom = await self.get_or_raise(cod)

        if classroom.enrollments:
            raise ClassroomHasEnrollmentsException(classroom.cod)

        await self.repository.delete(cod)

    async def list_by_professor(self, professor_id: int, params: Params, options: list | None = None):
        """Lista turmas filtradas por professor.

        Args:
            professor_id: Identificador do professor.
            params: Parâmetros de paginação (fastapi_pagination.Params).
            options: Opcionalmente, opções de carregamento do SQLAlchemy.

        Retorna uma página com os itens já convertidos para o schema de
        resposta.
        """

        _options = options or self.default_load_options

        page = await self.repository.list_by_professor(professor_id, params, options=_options)

        page.items = [Mapper.to_response(obj, self.response_schema) for obj in page.items]

        return page

    async def list_by_subject(self, subject_cod: str, params: Params, options: list | None = None):
        """Lista turmas filtradas por disciplina (subject).

        Args:
            subject_cod: Código da disciplina.
            params: Parâmetros de paginação.
            options: Opcionalmente, opções de carregamento do SQLAlchemy.

        Retorna uma página com os itens convertidos para o schema de
        resposta.
        """

        _options = options or self.default_load_options

        page = await self.repository.list_by_subject(subject_cod, params, options=_options)

        page.items = [Mapper.to_response(obj, self.response_schema) for obj in page.items]
        return page
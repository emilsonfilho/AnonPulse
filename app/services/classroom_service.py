"""Serviço de salas de aula.

Este módulo fornece a classe ClassroomService, responsável pela lógica de
negócio relacionada a turmas (classrooms).
"""

from typing import cast

from beanie import PydanticObjectId, Link

from app.core.exceptions.custom_exceptions import (
    ClassroomAlreadyExistsException,
    ClassroomHasEnrollmentsException,
    ClassroomNotFoundException,
)
from app.core.mapper import Mapper
from app.models import Classroom, Subject, Professor
from app.repositories.classroom_repository import ClassroomRepository
from app.schemas.classroom_schema import (
    ClassroomResponse,
    CreateClassroomRequest,
    UpdateClassroomRequest,
)
from app.services.base_service import BaseService, UpdateSchemaType, ResponseSchemaType
from fastapi_pagination import Params


class ClassroomService(
    BaseService[
        Classroom, CreateClassroomRequest, UpdateClassroomRequest, ClassroomResponse
    ]
):
    repository: ClassroomRepository

    """Serviço para operações sobre Classroom.

    Herdando de BaseService, este serviço adiciona validações e métodos
    específicos como listagens por professor e por disciplina.
    """

    def __init__(self, repository: ClassroomRepository) -> None:
        """Inicializa o serviço com o repositório e opções de carregamento."""
        super().__init__(
            repository=repository,
            response_schema=ClassroomResponse,
            not_found_exception=ClassroomNotFoundException,
            already_exists_exception=ClassroomAlreadyExistsException,
            default_fetch_links=True,
        )

    async def get_by_cod(self, cod: str) -> ClassroomResponse:
        """
        Busca uma sala de aula específica através do seu código identificador.

        Args:
            cod (str): O código único de identificação da sala de aula a ser buscada.

        Returns:
            ClassroomResponse: Uma instância validada do esquema de resposta
                contendo os dados da sala de aula localizada.

        Raises:
            Exception: A exceção de não encontrado (herdada do método `get_by`) caso
                nenhuma sala de aula corresponda ao código informado.
        """
        return await self.get_by(cod=cod)

    async def create(self, request: CreateClassroomRequest) -> ClassroomResponse:
        """Cria uma turma.

        O identificador usado para checagem de existência é o atributo
        `cod` do request.
        """
        subject = await Subject.find_one(Subject.cod == request.subject_cod)
        professor = await Professor.find_one(Professor.id == request.professor_id)

        if not subject or not professor:
            raise ClassroomNotFoundException()

        return await self._execute_creation(
            unique_filter={"cod": request.cod},
            cod=request.cod,
            subject=subject,
            professor=professor,
        )

    async def update(
        self,
        identifier: PydanticObjectId | str,
        request: UpdateSchemaType,
        fetch_links: bool | None = None,
    ) -> ResponseSchemaType:
        """
        Atualiza o código de uma sala de aula existente e a mapeia para o esquema de resposta.

        Args:
            identifier (PydanticObjectId | str): O código (cod) atual da sala de aula
                que será atualizada.
            request (UpdateSchemaType): O objeto Pydantic contendo os dados de
                atualização (espera-se que contenha o novo atributo `cod`).
            fetch_links (bool | None, opcional): Parâmetro presente na assinatura,
                mas não utilizado para condicionamento nesta implementação, uma vez
                que `fetch_all_links()` é acionado incondicionalmente. Padrão é None.

        Returns:
            ResponseSchemaType: Uma instância validada do esquema de resposta
                representando a sala de aula atualizada.

        Raises:
            ClassroomNotFoundException: Caso a sala de aula não seja localizada no
                banco de dados através do código (identifier) informado.
        """
        classroom = await self.repository.find_by(cod=identifier)

        if not classroom:
            raise ClassroomNotFoundException()

        await classroom.update({ "$set": { "cod": request.cod } })
        await classroom.fetch_all_links()
        return cast(ResponseSchemaType, Mapper.to_response(classroom, self.response_schema))

    async def delete(self, cod: str) -> None:
        """Remove uma classroom pelo código.

        Antes de deletar, valida se existem matrículas associadas e levanta
        ClassroomHasEnrollmentsException quando houver.
        """
        classroom = await self.repository.find_by(cod=cod)

        if not classroom:
            raise ClassroomNotFoundException()

        await classroom.fetch_all_links()

        if classroom.enrollments and len(classroom.enrollments) > 0:
            raise ClassroomHasEnrollmentsException(classroom.cod)

        await self.repository.delete(classroom.id)

    async def list_by_professor(self, professor_id: PydanticObjectId, params: Params):
        """Lista turmas filtradas por professor.

        Args:
            professor_id: Identificador do professor.
            params: Parâmetros de paginação (fastapi_pagination.Params).

        Retorna uma página com os itens já convertidos para o schema de
        resposta.
        """
        page = await self.repository.list_by_professor(
            professor_id, params, fetch_links=self.default_fetch_links
        )

        for obj in page.items:
            await obj.fetch_all_links()

        page.items = [
            Mapper.to_response(obj, self.response_schema) for obj in page.items
        ]

        return page

    async def list_by_subject(self, subject_cod: str, params: Params):
        """Lista turmas filtradas por disciplina (subject).

        Args:
            subject_cod: Código da disciplina.
            params: Parâmetros de paginação.

        Retorna uma página com os itens convertidos para o schema de
        resposta.
        """

        page = await self.repository.list_by_subject(
            subject_cod, params, fetch_links=self.default_fetch_links
        )

        for obj in page.items:
            await obj.fetch_all_links()

        page.items = [
            Mapper.to_response(obj, self.response_schema) for obj in page.items
        ]
        return page

"""Serviço de estudante.

Este módulo fornece a implementação de StudentService, responsável
por operações relacionadas ao modelo Student.
"""
from typing import cast, Any

from app.core.exceptions.custom_exceptions import (
    StudentAlreadyExistsException,
    StudentNotFoundException,
)
from app.core.mapper import Mapper
from app.models.student import Student
from app.repositories.student_repository import StudentRepository
from app.schemas.student_schema import (
    CreateStudentRequest,
    StudentResponse,
    UpdateStudentRequest,
)
from app.services.base_service import BaseService
from app.services.hash_service import HashService
from app.core.enums import HashAlgorithm


class StudentService(
    BaseService[Student, CreateStudentRequest, UpdateStudentRequest, StudentResponse]
):
    """Serviço para operações relacionadas a estudantes.

    Args:
        repository: Repositório responsável pela persistência de Student.
    """

    def __init__(self, repository: StudentRepository) -> None:
        """Inicializa o serviço de estudante.

        Parameters
        ----------
        repository : StudentRepository
            Instância do repositório de estudantes.
        """
        super().__init__(
            repository=repository,
            response_schema=StudentResponse,
            not_found_exception=StudentNotFoundException,
            already_exists_exception=StudentAlreadyExistsException,
        )

    async def create(self, request: CreateStudentRequest) -> StudentResponse:
        """Cria um estudante aplicando hash na matrícula.

        A matrícula (registration) é hasheada com SHA256 antes de
        delegar a criação ao BaseService.

        Parameters
        ----------
        request : CreateStudentRequest
            Dados do estudante a ser criado.

        Returns
        -------
        StudentResponse
            Representação do estudante criado.
        """
        request.registration = HashService.generate_hash(
            request.registration, HashAlgorithm.SHA256
        )

        return await self._execute_creation(
            unique_filter={"registration": request.registration},
            registration=request.registration,
        )

    async def update(
            self,
            identifier: str,
            request: UpdateStudentRequest,
            fetch_links: bool | None = None,
    ) -> StudentResponse:
        """
        Atualiza os dados de um estudante, aplicando hash na matrícula, e o mapeia para o esquema de resposta.

        Args:
            identifier (str): O identificador único do estudante a ser atualizado.
            request (UpdateStudentRequest): O objeto Pydantic contendo os dados de
                atualização, especificamente a nova matrícula que será criptografada.
            fetch_links (bool | None, opcional): Parâmetro presente na assinatura, mas
                não utilizado para condicionamento nesta implementação, visto que
                `fetch_all_links()` é executado incondicionalmente. Padrão é None.

        Returns:
            StudentResponse: Uma instância validada do esquema de resposta
                representando o estudante atualizado.

        Raises:
            StudentNotFoundException: Caso o estudante não seja localizado no
                banco de dados através do identificador informado.
        """
        request.registration = HashService.generate_hash(
            request.registration, HashAlgorithm.SHA256
        )

        student = await self.repository.get(identifier)

        if not student:
            raise StudentNotFoundException()

        await student.update({ "$set": { "registration": request.registration } })

        await student.fetch_all_links()

        return cast(
            StudentResponse,
            Mapper.to_response(student, self.response_schema)
        )

    async def delete(self, identifier: Any) -> None:
        """
        Exclui um estudante e remove em cascata todas as suas matrículas associadas.

        Args:
            identifier (Any): O identificador único do estudante a ser excluído.

        Returns:
            None

        Raises:
            Exception: A exceção gerada por `get_or_raise` (geralmente indicando que
                o recurso não foi encontrado) caso o estudante não exista no banco
                antes da tentativa de exclusão.
        """
        from app.models.enrollment import Enrollment

        student = await self.get_or_raise(identifier)

        await Enrollment.find({ "student.$id": student.id }).delete()
        await self.repository.delete(student.id)
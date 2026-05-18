"""Serviço de estudante.

Este módulo fornece a implementação de StudentService, responsável
por operações relacionadas ao modelo Student.
"""

from app.core.exceptions.custom_exceptions import (
    StudentAlreadyExistsException,
    StudentNotFoundException,
)
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

        return await super().create(request, identifier_value=request.registration)

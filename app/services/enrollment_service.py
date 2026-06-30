"""Serviço de inscrição (enrollment).

Este módulo contém a lógica de negócio para gerenciar inscrições,
incluindo criação, recuperação e exclusão lógica de registros.
"""

from datetime import datetime, timezone
from typing import cast

from beanie import PydanticObjectId, Link
from pymongo.errors import DuplicateKeyError

from app.core.exceptions.custom_exceptions import (
    EnrollmentAlreadyExistsException,
    EnrollmentNotFoundException,
    ClassroomNotFoundException,
    StudentNotFoundException,
)
from app.models import Student, Classroom
from app.models.enrollment import Enrollment
from app.repositories.enrollment_repository import EnrollmentRepository
from app.schemas.enrollment_schema import (
    CreateEnrollmentRequest,
    EnrollmentResponse,
    UpdateEnrollmentRequest,
)
from app.services.base_service import BaseService


class EnrollmentService(
    BaseService[
        Enrollment, CreateEnrollmentRequest, UpdateEnrollmentRequest, EnrollmentResponse
    ]
):
    """Serviço para gerenciar operações de inscrição.

    Fornece funcionalidades para criar, recuperar e deletar inscrições,
    herdando funcionalidades-base de manipulação de dados.
    """

    def __init__(self, repository: EnrollmentRepository) -> None:
        """Inicializa o serviço de inscrição."""
        super().__init__(
            repository=repository,
            response_schema=EnrollmentResponse,
            not_found_exception=EnrollmentNotFoundException,
            already_exists_exception=EnrollmentAlreadyExistsException,
        )

    async def create(self, request: CreateEnrollmentRequest) -> EnrollmentResponse:
        """Cria uma inscrição.

        Args:
            request: Dados da inscrição a ser criada.

        Returns:
            EnrollmentResponse: Dados da inscrição criada.

        Raises:
            EnrollmentAlreadyExistsException: Se a inscrição já existe.
        """
        student = await Student.get(request.student_id)

        if not student:
            raise StudentNotFoundException()

        classroom = await Classroom.find_one(Classroom.cod == request.classroom_cod)
        if not classroom:
            raise ClassroomNotFoundException()

        enrollment = Enrollment(
            student=cast(Link[Student], cast(object, student)),
            classroom=cast(Link[Classroom], cast(object, classroom)),
            is_active=True,
            enrolled_at=datetime.now(timezone.utc),
        )

        try:
            new_enrollment = await self.repository.create(enrollment)
        except DuplicateKeyError:
            raise EnrollmentAlreadyExistsException()

        assert student.id is not None
        assert new_enrollment.id is not None

        student.enrollments.append(cast(Link["Enrollment"], cast(object, new_enrollment)))
        classroom.enrollments.append(cast(Link["Enrollment"], cast(object, new_enrollment)))

        await student.save()
        await classroom.save()

        return EnrollmentResponse(
            id=new_enrollment.id,
            is_active=new_enrollment.is_active,
            enrolled_at=new_enrollment.enrolled_at,
            classroom_cod=classroom.cod,
            student_id=student.id,
        )

    async def delete(self, identifier: PydanticObjectId) -> None:
        """Deleta uma inscrição (exclusão lógica).

        Define o status is_active como False em vez de remover o registro.

        Args:
            identifier: Identificador da inscrição a ser deletada.

        Raises:
            EnrollmentNotFoundException: Se a inscrição não é encontrada.
        """
        await self.get_or_raise(identifier)

        await self.repository.update(identifier, {"is_active": False})

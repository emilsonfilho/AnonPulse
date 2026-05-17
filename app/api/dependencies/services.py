"""Dependências para injeção de serviços da aplicação."""

from fastapi import Depends

from app.services.classroom_service import ClassroomService
from app.services.professor_service import ProfessorService
from app.services.subject_service import SubjectService

from app.api.dependencies.repositories import (
    get_classroom_repository,
    get_professor_repository,
    get_subject_repository,
)

from app.repositories.classroom_repository import ClassroomRepository
from app.repositories.professor_repository import ProfessorRepository
from app.repositories.subject_repository import SubjectRepository
from app.repositories.feedback_repository import FeedbackRepository
from app.services.feedback_service import FeedbackService
from app.api.dependencies.repositories import get_feedback_repository


def get_classroom_service(
    repository: ClassroomRepository = Depends(get_classroom_repository),
) -> ClassroomService:
    """Retorna uma instância do serviço de salas de aula."""
    return ClassroomService(repository)


def get_professor_service(
    repository: ProfessorRepository = Depends(get_professor_repository),
) -> ProfessorService:
    """Retorna uma instância do serviço de professores."""
    return ProfessorService(repository)


def get_subject_service(
    repository: SubjectRepository = Depends(get_subject_repository),
) -> SubjectService:
    """Retorna uma instância do serviço de disciplinas."""
    return SubjectService(repository)


def get_feedback_service(
    repository: FeedbackRepository = Depends(get_feedback_repository),
) -> FeedbackService:
    """Retorna uma instância do serviço de feedback."""
    return FeedbackService(repository)

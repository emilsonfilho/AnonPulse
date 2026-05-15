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
    return ClassroomService(repository)


def get_professor_service(
    repository: ProfessorRepository = Depends(get_professor_repository),
) -> ProfessorService:
    return ProfessorService(repository)


def get_subject_service(
    repository: SubjectRepository = Depends(get_subject_repository),
) -> SubjectService:
    return SubjectService(repository)


def get_feedback_service(
    repository: FeedbackRepository = Depends(get_feedback_repository),
) -> FeedbackService:
    return FeedbackService()

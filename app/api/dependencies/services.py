"""Dependências para injeção de serviços da aplicação."""

from fastapi import Depends

from app.api.dependencies.repositories import (
    get_classroom_repository,
    get_document_repository,
    get_enrollment_repository,
    get_feedback_repository,
    get_monitor_assignment_repository,
    get_monitor_repository,
    get_professor_repository,
    get_student_repository,
    get_subject_repository,
)

from app.repositories.classroom_repository import ClassroomRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.monitor_assignment_repository import MonitorAssignmentRepository
from app.repositories.monitor_repository import MonitorRepository
from app.repositories.professor_repository import ProfessorRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.subject_repository import SubjectRepository
from app.services.classroom_service import ClassroomService
from app.services.document_service import DocumentService
from app.services.enrollment_service import EnrollmentService
from app.services.feedback_service import FeedbackService
from app.services.monitor_assignment_service import MonitorAssignmentService
from app.services.monitor_service import MonitorService
from app.services.professor_service import ProfessorService
from app.services.student_service import StudentService
from app.services.subject_service import SubjectService
from app.services.storage_service import StorageService


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


def get_student_service(
    repository: StudentRepository = Depends(get_student_repository),
) -> StudentService:
    """Retorna uma instância do serviço de estudantes."""
    return StudentService(repository)


def get_monitor_service(
    repository: MonitorRepository = Depends(get_monitor_repository),
) -> MonitorService:
    """Retorna uma instância do serviço de monitores."""
    return MonitorService(repository)


def get_monitor_assignment_service(
    repository: MonitorAssignmentRepository = Depends(
        get_monitor_assignment_repository
    ),
) -> MonitorAssignmentService:
    """Retorna uma instância do serviço de monitorias."""
    return MonitorAssignmentService(repository)


def get_enrollment_service(
    repository: EnrollmentRepository = Depends(get_enrollment_repository),
) -> EnrollmentService:
    """Retorna uma instância do serviço de matrículas."""
    return EnrollmentService(repository)


def get_storage_service() -> StorageService:
    """Retorna uma instância do serviço de armazenamento."""
    return StorageService()


def get_document_service(
    repository: DocumentRepository = Depends(get_document_repository),
) -> DocumentService:
    """Retorna uma instância do serviço de documentos."""
    return DocumentService(repository=repository, storage_service=get_storage_service())

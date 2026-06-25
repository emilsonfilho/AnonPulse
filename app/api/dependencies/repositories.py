"""Módulo de dependências para repositórios da aplicação.

Este módulo fornece funções de dependência FastAPI para injetar
instâncias de repositórios nas rotas da API.
"""

from app.repositories.classroom_repository import ClassroomRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.professor_repository import ProfessorRepository
from app.repositories.subject_repository import SubjectRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.monitor_repository import MonitorRepository
from app.repositories.monitor_assignment_repository import MonitorAssignmentRepository
from app.repositories.document_repository import DocumentRepository


def get_subject_repository():
    """Obtém uma instância do repositório de disciplinas.

    Returns:
        Instância do repositório de disciplinas.
    """
    return SubjectRepository()


def get_student_repository():
    """Obtém uma instância do repositório de estudantes.

    Returns:
        Instância do repositório de estudantes.
    """
    return StudentRepository()


def get_professor_repository():
    """Obtém uma instância do repositório de professores.

    Returns:
        Instância do repositório de professores.
    """
    return ProfessorRepository()


def get_classroom_repository():
    """Obtém uma instância do repositório de salas de aula.

    Returns:
        Instância do repositório de salas de aula.
    """
    return ClassroomRepository()


def get_feedback_repository():
    """Obtém uma instância do repositório de feedback.

    Returns:
        Instância do repositório de feedback.
    """
    return FeedbackRepository()


def get_monitor_repository():
    """Obtém uma instância do repositório de monitores.

    Returns:
        Instância do repositório de monitores.
    """
    return MonitorRepository()


def get_monitor_assignment_repository():
    """Obtém uma instância do repositório de atribuições de monitores.

    Returns:
        Instância do repositório de atribuições de monitores.
    """
    return MonitorAssignmentRepository()


def get_enrollment_repository():
    """Obtém uma instância do repositório de matrículas.

    Returns:
        Instância do repositório de matrículas.
    """
    return EnrollmentRepository()


def get_document_repository():
    """Obtém uma instância do repositório de documentos.

    Returns:
        Instância do repositório de documentos.
    """
    return DocumentRepository()

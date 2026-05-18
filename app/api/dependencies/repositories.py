"""Módulo de dependências para repositórios da aplicação.

Este módulo fornece funções de dependência FastAPI para injetar
instâncias de repositórios nas rotas da API.
"""

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.dependencies.session import get_session
from app.repositories.classroom_repository import ClassroomRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.professor_repository import ProfessorRepository
from app.repositories.subject_repository import SubjectRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.monitor_repository import MonitorRepository
from app.repositories.monitor_assignment_repository import MonitorAssignmentRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.feedback_type_repository import FeedbackTypeRepository


def get_subject_repository(session: AsyncSession = Depends(get_session)):
    """Obtém uma instância do repositório de disciplinas.

    Args:
        session: Sessão assíncrona do banco de dados.

    Returns:
        Instância do repositório de disciplinas.
    """
    return SubjectRepository(session)


def get_student_repository(session: AsyncSession = Depends(get_session)):
    """Obtém uma instância do repositório de estudantes.

    Args:
        session: Sessão assíncrona do banco de dados.

    Returns:
        Instância do repositório de estudantes.
    """
    return StudentRepository(session)


def get_professor_repository(session: AsyncSession = Depends(get_session)):
    """Obtém uma instância do repositório de professores.

    Args:
        session: Sessão assíncrona do banco de dados.

    Returns:
        Instância do repositório de professores.
    """
    return ProfessorRepository(session)


def get_classroom_repository(session: AsyncSession = Depends(get_session)):
    """Obtém uma instância do repositório de salas de aula.

    Args:
        session: Sessão assíncrona do banco de dados.

    Returns:
        Instância do repositório de salas de aula.
    """
    return ClassroomRepository(session)


def get_feedback_repository(session: AsyncSession = Depends(get_session)):
    """Obtém uma instância do repositório de feedback.

    Args:
        session: Sessão assíncrona do banco de dados.

    Returns:
        Instância do repositório de feedback.
    """
    return FeedbackRepository(session)


def get_monitor_repository(session: AsyncSession = Depends(get_session)):
    """Obtém uma instância do repositório de monitores.

    Args:
        session: Sessão assíncrona do banco de dados.

    Returns:
        Instância do repositório de monitores.
    """
    return MonitorRepository(session)


def get_monitor_assignment_repository(
    session: AsyncSession = Depends(get_session)
):
    """Obtém uma instância do repositório de atribuições de monitores.

    Args:
        session: Sessão assíncrona do banco de dados.

    Returns:
        Instância do repositório de atribuições de monitores.
    """
    return MonitorAssignmentRepository(session)


def get_enrollment_repository(session: AsyncSession = Depends(get_session)):
    """Obtém uma instância do repositório de matrículas.

    Args:
        session: Sessão assíncrona do banco de dados.

    Returns:
        Instância do repositório de matrículas.
    """
    return EnrollmentRepository(session)


def get_document_repository(session: AsyncSession = Depends(get_session)):
    """Obtém uma instância do repositório de documentos.

    Args:
        session: Sessão assíncrona do banco de dados.

    Returns:
        Instância do repositório de documentos.
    """
    return DocumentRepository(session)


def get_feedback_type_repository(session: AsyncSession = Depends(get_session)):
    """Obtém uma instância do repositório de tipos de feedback.

    Args:
        session: Sessão assíncrona do banco de dados.

    Returns:
        Instância do repositório de tipos de feedback.
    """
    return FeedbackTypeRepository(session)

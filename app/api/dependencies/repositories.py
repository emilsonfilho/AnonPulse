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


def get_subject_repository(session: AsyncSession = Depends(get_session)):
    return SubjectRepository(session)


def get_student_repository(session: AsyncSession = Depends(get_session)):
    return StudentRepository(session)


def get_professor_repository(session: AsyncSession = Depends(get_session)):
    return ProfessorRepository(session)


def get_classroom_repository(session: AsyncSession = Depends(get_session)):
    return ClassroomRepository(session)


def get_feedback_repository(session: AsyncSession = Depends(get_session)):
    return FeedbackRepository(session)


def get_monitor_repository(session: AsyncSession = Depends(get_session)):
    return MonitorRepository(session)


def get_monitor_assignment_repository(session: AsyncSession = Depends(get_session)):
    return MonitorAssignmentRepository(session)


def get_enrollment_repository(session: AsyncSession = Depends(get_session)):
    return EnrollmentRepository(session)


def get_document_repository(session: AsyncSession = Depends(get_session)):
    return DocumentRepository(session)

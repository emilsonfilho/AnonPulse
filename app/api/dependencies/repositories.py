from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.session import get_session
from app.repositories.classroom_repository import ClassroomRepository
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.professor_repository import ProfessorRepository
from app.repositories.subject_repository import SubjectRepository


def get_subject_repository(session: AsyncSession = Depends(get_session)):
    return SubjectRepository(session)


def get_professor_repository(session: AsyncSession = Depends(get_session)):
    return ProfessorRepository(session)


def get_classroom_repository(session: AsyncSession = Depends(get_session)):
    return ClassroomRepository(session)


def get_feedback_repository(session: AsyncSession = Depends(get_session)):
    return FeedbackRepository(session)

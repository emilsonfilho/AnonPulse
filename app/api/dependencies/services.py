from fastapi import Depends

from app.api.dependencies.repositories import get_subject_repository
from app.repositories.subject_repository import SubjectRepository
from app.services.subject_service import SubjectService

def get_subject_service(
        repository: SubjectRepository = Depends(get_subject_repository)
):
    return SubjectService(repository)
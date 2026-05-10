from app.schemas.subject_schema import CreateSubjectRequest, SubjectResponse
from app.models import Subject
from app.core.exceptions.custom_exceptions import SubjectAlreadyExistsExcepion

class SubjectService:
    def __init__(self, repository) -> None:
        self.repository = repository

    async def create_subject(self, data: CreateSubjectRequest):
        subject_exists = await self.repository.get_by_code(data.cod)

        if (subject_exists):
            raise SubjectAlreadyExistsExcepion(
                f"Já existe uma disciplina com o código {data.cod}."
            )

        subject = Subject(**data.model_dump())
        new_subject = await self.repository.create(subject)

        return SubjectResponse.model_validate(new_subject)
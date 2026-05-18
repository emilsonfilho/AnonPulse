from app.core.exceptions.custom_exceptions import ProfessorNotFoundException
from app.models.professor import Professor
from app.repositories.professor_repository import ProfessorRepository
from app.schemas.professor_schema import (
    CreateProfessorRequest,
    ProfessorResponse,
    UpdateProfessorRequest,
)
from app.services.base_service import BaseService


class ProfessorService(
    BaseService[
        Professor, CreateProfessorRequest, UpdateProfessorRequest, ProfessorResponse
    ]
):
    """Serviço responsável pelas operações relacionadas a professores."""

    def __init__(self, repository: ProfessorRepository) -> None:
        """Inicializa o serviço com o repositório de professores.

        Args:
            repository: Repositório utilizado para persistência e consulta.
        """
        super().__init__(
            repository=repository,
            response_schema=ProfessorResponse,
            not_found_exception=ProfessorNotFoundException,
        )

    async def create(self, request: CreateProfessorRequest) -> ProfessorResponse:
        """Cria um novo professor.

        Args:
            request: Dados necessários para a criação do professor.

        Returns:
            ProfessorResponse: Dados do professor criado.
        """
        return await super().create(request)

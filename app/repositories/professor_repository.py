from app.models.professor import Professor
from app.repositories.base_repository import BaseRepository


class ProfessorRepository(BaseRepository):
    """Repositorio para a entidade Professor."""

    def __init__(self) -> None:
        """Inicializa o repositório com a sessão do banco de dados."""
        super().__init__(model=Professor)

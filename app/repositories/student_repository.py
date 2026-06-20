from app.repositories.base_repository import BaseRepository
from app.models.student import Student

class StudentRepository(BaseRepository):
    """Repositorio para a entidade Student."""
    def __init__(self) -> None:
        """Inicializa o repositório com a sessão do banco de dados."""
        super().__init__(model=Student)
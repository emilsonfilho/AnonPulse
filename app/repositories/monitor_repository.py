from app.repositories.base_repository import BaseRepository
from app.models.monitor import Monitor

class MonitorRepository(BaseRepository):
    """Repositorio para acesso e manipulação de dados relacionados a Monitores."""
    def __init__(self) -> None:
        """Inicializa o MonitorRepository com a sessão de banco de dados."""
        super().__init__(model=Monitor)
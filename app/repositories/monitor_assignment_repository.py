from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base_repository import BaseRepository
from app.models.monitor_assignment import MonitorAssignment

class MonitorAssignmentRepository(BaseRepository):
    """Repositório para acesso e manipulação de dados de MonitorAssignment."""
    def __init__(self, session: AsyncSession) -> None:
        """Inicializa o repositório com a sessão de banco de dados."""
        super().__init__(model=MonitorAssignment, session=session)
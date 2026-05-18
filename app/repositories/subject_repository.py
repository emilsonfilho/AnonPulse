from sqlalchemy.ext.asyncio import AsyncSession

from app.models.subject import Subject
from app.repositories.base_repository import BaseRepository
class SubjectRepository(BaseRepository):
    """Repositorio para a entidade Subject."""
    def __init__(self, session: AsyncSession):
        """Inicializa o repositório com a sessão do banco de dados."""
        super().__init__(model=Subject, session=session)
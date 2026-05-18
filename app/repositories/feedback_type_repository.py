"""Repositório para gerenciar operações de tipo de feedback."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.feedback_type import FeedbackType
from app.repositories.base_repository import BaseRepository

class FeedbackTypeRepository(BaseRepository[FeedbackType]):
    """Repositório para acesso e manipulação de dados de tipos de feedback.
    
    A paginação não é necessária nesta entidade, pois ela possui um número
    definido de valores possíveis.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Inicializa o repositório com uma sessão assíncrona.
        
        Args:
            session: Sessão assíncrona do SQLAlchemy para operações com banco.
        """
        super().__init__(model=FeedbackType, session=session)

    
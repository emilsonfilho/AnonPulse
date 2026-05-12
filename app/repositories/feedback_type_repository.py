from sqlalchemy.ext.asyncio import AsyncSession

from app.models.feedback_type import FeedbackType

class FeedbackTypeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # Aqui, não é necessário paginação porque temos certeza de que essa entidade possui um número definido de valores possíveis
    async def list_all(self) -> list[FeedbackType]:
        # To-Do
        pass
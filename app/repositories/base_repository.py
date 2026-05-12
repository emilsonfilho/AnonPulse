from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

from typing import TypeVar, Generic, Type, Any

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get(self, identifier: Any) -> ModelType | None:
        return await self.session.get(self.model, identifier)
    
    async def list_all(self, params: Params) -> Page[ModelType]:
        # To-Do
        pass
        
    async def create(self, obj: ModelType) -> ModelType:
        # To-Do
        pass
        
    async def update(self, identifier: Any, obj_in: dict) -> ModelType:
        # se não houver um cara para atualizar, devolva o erro

        # To-Do
        pass
        
    async def delete(self, identifier: Any) -> None:
        # To-Do
        pass
        
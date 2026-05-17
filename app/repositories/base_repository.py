from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func
from fastapi_pagination.ext.sqlalchemy import paginate
from app.core.exceptions.custom_exceptions import ResourceNotFoundException as Res

from typing import TypeVar, Generic, Type, Any

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get(self, identifier: Any, options: list[Any] | None = None) -> ModelType | None:
        primary_key = list(self.model.__table__.primary_key.columns)[0]

        query = select(self.model).where(primary_key == identifier)

        if options:
            query = query.options(*options)

        result = await self.session.execute(query)

        return result.scalars().first()

    async def list_all(self, params: Params, options: list[Any] | None = None) -> Page[ModelType]:
        query = select(self.model)

        if options:
            query = query.options(*options)

        return await paginate(self.session, query, params)

    async def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, identifier: Any, obj_in: dict) -> ModelType:
        obj = await self.get(identifier)
        if not obj:
            raise Res(f"Sem resultados para {identifier} informado.")

        for key, value in obj_in.items():
            setattr(obj, key, value)

        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, identifier: Any) -> None:
        obj = await self.get(identifier)
        if not obj:
            raise Res(f"Sem resultados para {identifier} informado.")

        await self.session.delete(obj)
        await self.session.commit()

    async def count(self) -> int:
        stmt = select(func.count()).select_from(self.model)
        result = await self.session.execute(stmt)

        return result.scalar_one()
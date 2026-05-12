from fastapi_pagination import Page, Params
from typing import TypeVar, Callable, Awaitable, Generic, Type, Any

from app.core.mapper import Mapper
from app.repositories.base_repository import BaseRepository

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
ResponseSchemaType = TypeVar("ResponseSchemaType")

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
    def __init__(
            self, 
            repository: BaseRepository,
            response_schema: Type[ResponseSchemaType],
            not_found_exception: Type[Exception],
            already_exists_exception: Type[Exception]
    ) -> None:
        self.repository = repository
        self.response_schema = self.response_schema
        self.not_found_exception = not_found_exception
        self.already_exists_exception = already_exists_exception

    async def get_or_raise(self, identifier: Any) -> ModelType:
        obj = await self.repository.get(identifier)

        if not obj:
            raise self.not_found_exception()
        
        return obj
    
    async def list_all(self, params: Params) -> Page[ResponseSchemaType]:
        page = await self.repository.list_all(params)

        page.items = [
            Mapper.to_response(obj, self.response_schema) for obj in page
        ]

        return page
    
    async def get_by_id(self, identifier: Any) -> ResponseSchemaType:
        obj = await self.get_or_raise(identifier)
        return Mapper.to_response(obj, self.response_schema)
    
    async def create(self, request: CreateSchemaType, identifier_value: Any) -> ResponseSchemaType:
        obj_exists = await self.repository.get(identifier_value)

        if obj_exists:
            raise self.already_exists_exception()
        
        obj = self.repository.model(**request.model_dump())
        new_obj = await self.repository.create(obj)

        return Mapper.to_response(new_obj, self.response_schema)
    
    async def update(self, identifier: Any, request: UpdateSchemaType) -> ResponseSchemaType:
        await self.get_or_raise(identifier)

        updated_obj = await self.repository.update(
            identifier,
            request.model_dump(exclude_unset=True)
        )

        return Mapper.to_response(updated_obj, self.response_schema)
    
    async def delete(self, identifier: Any) -> None:
        await self.get_or_raise(identifier)
        await self.repository.delete(identifier)
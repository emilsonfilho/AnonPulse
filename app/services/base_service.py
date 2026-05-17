from fastapi_pagination import Page, Params
from sqlalchemy import inspect
from typing import Any, Generic, Type, TypeVar


from app.core.mapper import Mapper
from app.repositories.base_repository import BaseRepository


ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
ResponseSchemaType = TypeVar("ResponseSchemaType")


class BaseService(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]
):
    def __init__(
        self,
        repository: BaseRepository,
        response_schema: Type[ResponseSchemaType],
        not_found_exception: Type[Exception],
        already_exists_exception: Type[Exception] | None = None,
        default_load_options: list[Any] | None = None,
    ) -> None:
        self.repository = repository
        self.response_schema = response_schema
        self.not_found_exception = not_found_exception
        self.already_exists_exception = already_exists_exception
        self.default_load_options = default_load_options

    async def get_or_raise(self, identifier: Any, options: list[Any] | None = None) -> ModelType:
        _options = options or self.default_load_options

        obj = await self.repository.get(identifier, options=_options)

        if not obj:
            raise self.not_found_exception()

        return obj

    async def list_all(self, params: Params, options: list[Any] | None = None) -> Page[ResponseSchemaType]:
        _options = options or self.default_load_options

        page = await self.repository.list_all(params, options=_options)

        page.items = [
            Mapper.to_response(obj, self.response_schema) for obj in page.items
        ]

        return page

    async def get_by_id(self, identifier: Any, options: list[Any] | None = None) -> ResponseSchemaType:
        obj = await self.get_or_raise(identifier, options=options)
        return Mapper.to_response(obj, self.response_schema)

    async def create(
        self, request: CreateSchemaType, identifier_value: Any | None = None
    ) -> ResponseSchemaType:
        if identifier_value is not None:
            obj_exists = await self.repository.get(identifier_value)

            if obj_exists:
                raise self.already_exists_exception(identifier_value)

        obj = self.repository.model(**request.model_dump())
        new_obj = await self.repository.create(obj)

        identifier = inspect(new_obj).identity[0]

        new_obj = await self.get_or_raise(
            identifier,
            options=self.default_load_options
        )

        return Mapper.to_response(new_obj, self.response_schema)

    async def update(
        self, identifier: Any, request: UpdateSchemaType, options: list[Any] | None = None
    ) -> ResponseSchemaType:
        updated_obj = await self.repository.update(
            identifier, request.model_dump(exclude_unset=True),
        )

        _new_identifier = inspect(updated_obj).identity[0]

        _options = options or self.default_load_options

        updated_obj_with_rels = await self.get_or_raise(_new_identifier, options=_options)

        return Mapper.to_response(updated_obj_with_rels, self.response_schema)

    async def delete(self, identifier: Any) -> None:
        await self.get_or_raise(identifier)
        await self.repository.delete(identifier)

    async def count(self) -> int:
        return await self.repository.count()
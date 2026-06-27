"""Módulo de serviço base com operações CRUD genéricas.

Este módulo fornece a classe BaseService que implementa operações
básicas de criação, leitura, atualização e exclusão (CRUD) de forma
genérica para qualquer modelo de dados.
"""

from beanie import Document, PydanticObjectId
from fastapi_pagination import Page, Params
from fastapi_pagination.api import create_page
from pydantic import BaseModel
from typing import Any, Generic, Type, TypeVar

from app.core.mapper import Mapper
from app.repositories.base_repository import BaseRepository

ModelType = TypeVar("ModelType", bound=Document)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)


class BaseService(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]
):
    """Serviço base genérico para operações CRUD."""

    def __init__(
        self,
        repository: BaseRepository[ModelType],
        response_schema: Type[ResponseSchemaType],
        not_found_exception: Type[Exception],
        already_exists_exception: Type[Exception] | None = None,
        default_fetch_links: bool = True,
    ) -> None:
        self.repository = repository
        self.response_schema = response_schema
        self.not_found_exception = not_found_exception
        self.already_exists_exception = already_exists_exception
        self.default_fetch_links = default_fetch_links

    async def get_or_raise(
        self,
        identifier: PydanticObjectId,
        fetch_links: bool | None = None,
    ) -> ModelType:
        _fetch_links = (
            fetch_links if fetch_links is not None else self.default_fetch_links
        )

        obj = await self.repository.get(identifier, fetch_links=_fetch_links)

        if not obj:
            raise self.not_found_exception()

        return obj

    async def list_all(
        self,
        params: Params,
        fetch_links: bool | None = None,
    ) -> Page[ResponseSchemaType]:
        _fetch_links = (
            fetch_links if fetch_links is not None else self.default_fetch_links
        )

        query = self.repository.model.find_all(fetch_links=_fetch_links)

        total = await query.count()

        limit = params.size
        skip = (params.page - 1) * params.size if hasattr(params, "page") else 0

        raw_items = await query.skip(skip).limit(limit).to_list()

        if _fetch_links:
            for item in raw_items:
                await item.fetch_all_links()

        mapped_items = [
            Mapper.to_response(obj, self.response_schema) for obj in raw_items
        ]

        return create_page(mapped_items, total, params)

    async def get_by_id(
        self,
        identifier: PydanticObjectId,
        fetch_links: bool | None = None,
    ) -> ResponseSchemaType:
        obj = await self.get_or_raise(identifier, fetch_links=fetch_links)
        return Mapper.to_response(obj, self.response_schema)

    async def get_by(self, **filters) -> ResponseSchemaType:
        obj = await self.repository.find_by(**filters)

        if not obj:
            raise self.not_found_exception()

        return Mapper.to_response(obj, self.response_schema)

    async def create(
        self,
        request: CreateSchemaType,
        identifier_value: PydanticObjectId | None = None,
    ) -> ResponseSchemaType:
        if identifier_value is not None and self.already_exists_exception:
            obj_exists = await self.repository.get(identifier_value)
            if obj_exists:
                raise self.already_exists_exception(identifier_value)

        obj_dict = request.model_dump(exclude_unset=True)
        new_obj = await self.repository.create(obj_dict)

        if new_obj.id is None:
            raise RuntimeError("Objeto criado sem ID")

        new_obj = await self.get_or_raise(
            new_obj.id,
            fetch_links=self.default_fetch_links,
        )

        return Mapper.to_response(new_obj, self.response_schema)

    async def _execute_creation(
            self,
            unique_filter: dict,
            **model_data
    ) -> ResponseSchemaType:
        if await self.repository.find_by(**unique_filter):
            raise self.already_exists_exception(**unique_filter)

        entity = self.repository.model(**model_data)

        new_obj = await entity.insert()

        if hasattr(new_obj, "fetch_all_links"):
            await new_obj.fetch_all_links()

        return Mapper.to_response(new_obj, self.response_schema)

    async def update(
        self,
        identifier: PydanticObjectId | str,
        request: UpdateSchemaType,
        fetch_links: bool | None = None,
    ) -> ResponseSchemaType:
        updated_obj = await self.repository.update(
            identifier,
            request.model_dump(exclude_unset=True),
        )

        if not updated_obj:
            raise self.not_found_exception()

        if updated_obj.id is None:
            raise RuntimeError("Objeto atualizado sem ID")

        _fetch_links = (
            fetch_links if fetch_links is not None else self.default_fetch_links
        )

        updated_obj_with_rels = await self.get_or_raise(
            updated_obj.id, fetch_links=_fetch_links
        )

        return Mapper.to_response(updated_obj_with_rels, self.response_schema)

    async def delete(self, identifier: Any) -> None:
        await self.get_or_raise(identifier)
        await self.repository.delete(identifier)

    async def count(self) -> int:
        return await self.repository.count()

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
        """
        Busca um documento pelo seu identificador ou lança uma exceção se não for encontrado.

        Args:
            identifier (PydanticObjectId): O identificador único (Object ID) do
                documento a ser recuperado.
            fetch_links (bool | None, opcional): Flag para determinar se os documentos
                vinculados devem ser trazidos na consulta. Se `None`, assume o
                comportamento padrão da classe. Padrão é None.

        Returns:
            ModelType: A instância do documento correspondente ao identificador.

        Raises:
            Exception: A exceção gerada por `self.not_found_exception()` caso o
                documento não seja localizado no repositório.
        """
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
        """
        Lista todos os documentos do repositório com paginação e mapeamento.

        Args:
            params (Params): Os parâmetros de paginação (como página e tamanho)
                utilizados para limitar e deslocar os resultados da consulta.
            fetch_links (bool | None, opcional): Flag para determinar se os
                documentos vinculados devem ser resolvidos. Se `None`, utiliza o
                comportamento padrão da classe. Padrão é None.

        Returns:
            Page[ResponseSchemaType]: Um objeto de resposta paginada contendo
                os documentos convertidos para o esquema de saída, além do
                total de registros e detalhes da paginação.
        """
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
        """
        Busca um documento pelo seu identificador e o mapeia para o esquema de resposta.

        Args:
            identifier (PydanticObjectId): O identificador único (Object ID) do
                documento a ser buscado.
            fetch_links (bool | None, opcional): Flag para determinar se os
                documentos vinculados devem ser resolvidos durante a consulta. Se
                `None`, repassa a decisão para o método `get_or_raise`. Padrão é None.

        Returns:
            ResponseSchemaType: Uma instância validada do esquema de resposta
                contendo os dados do documento localizado.

        Raises:
            Exception: A mesma exceção lançada por `get_or_raise` (geralmente indicando
                que o recurso não foi encontrado) caso o documento não exista.
        """
        obj = await self.get_or_raise(identifier, fetch_links=fetch_links)
        return Mapper.to_response(obj, self.response_schema)

    async def get_by(self, **filters) -> ResponseSchemaType:
        """
        Busca um único documento com base em filtros e o mapeia para o esquema de resposta.

        Args:
            **filters: Critérios de filtragem flexíveis (argumentos nomeados)
                utilizados para a consulta no repositório.

        Returns:
            ResponseSchemaType: Uma instância validada do esquema de resposta
                contendo os dados do documento localizado.

        Raises:
            Exception: A exceção gerada por `self.not_found_exception()` caso
                nenhum registro corresponda aos filtros informados.
        """
        obj = await self.repository.find_by(**filters)

        if not obj:
            raise self.not_found_exception()

        return Mapper.to_response(obj, self.response_schema)

    async def create(
        self,
        request: CreateSchemaType,
        identifier_value: PydanticObjectId | None = None,
    ) -> ResponseSchemaType:
        """
        Cria um novo documento no banco de dados e o mapeia para o esquema de resposta.

        Args:
            request (CreateSchemaType): O objeto Pydantic contendo os dados validados
                necessários para a criação do novo registro.
            identifier_value (PydanticObjectId | None, opcional): Um identificador
                opcional utilizado para verificar se o documento já existe no banco
                de dados antes da criação. Padrão é None.

        Returns:
            ResponseSchemaType: Uma instância validada do esquema de resposta
                representando o documento recém-criado.

        Raises:
            Exception: A exceção configurada em `self.already_exists_exception` caso
                um documento com o `identifier_value` já exista no repositório.
            RuntimeError: Se o documento for salvo no repositório, mas não possuir
                um ID gerado.
            Exception: A exceção gerada por `get_or_raise` caso falhe ao tentar
                recarregar o documento após a criação.
        """
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
        """
        Executa a criação interna de um documento após verificar sua unicidade.

        Args:
            unique_filter (dict): Um dicionário contendo os critérios de busca
                utilizados para garantir que o documento não seja duplicado.
            **model_data: Argumentos nomeados contendo os dados a serem
                preenchidos na criação da nova instância do modelo.

        Returns:
            ResponseSchemaType: Uma instância validada do esquema de resposta
                representando o documento recém-criado.

        Raises:
            Exception: A exceção configurada em `self.already_exists_exception`
                caso a validação de unicidade falhe (o documento já exista).
        """
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
        """
        Atualiza um documento existente no banco de dados e o mapeia para o esquema de resposta.

        Args:
            identifier (PydanticObjectId | str): O identificador único do documento a
                ser atualizado.
            request (UpdateSchemaType): O objeto Pydantic contendo os dados parciais ou
                totais validados para a atualização do registro.
            fetch_links (bool | None, opcional): Flag para determinar se os documentos
                vinculados devem ser resolvidos ao recarregar o registro após a atualização.
                Se `None`, assume o comportamento padrão da classe. Padrão é None.

        Returns:
            ResponseSchemaType: Uma instância validada do esquema de resposta
                representando o documento atualizado.

        Raises:
            Exception: A exceção gerada por `self.not_found_exception()` caso o documento
                não seja encontrado para a atualização.
            RuntimeError: Se o documento for atualizado com sucesso, mas o objeto retornado
                não possuir um ID.
            Exception: A exceção gerada por `get_or_raise` caso falhe ao tentar recarregar
                o documento após a atualização.
        """
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
        """
        Exclui um documento do banco de dados com base no seu identificador.

        Args:
            identifier (Any): O identificador único do documento a ser excluído.

        Returns:
            None

        Raises:
            Exception: A exceção gerada por `get_or_raise` (geralmente indicando que
                o recurso não foi encontrado) caso o documento não exista no banco
                antes da tentativa de exclusão.
        """
        await self.get_or_raise(identifier)
        await self.repository.delete(identifier)

    async def count(self) -> int:
        """
        Retorna a contagem total de documentos armazenados no repositório.

        Returns:
            int: O número total de documentos encontrados no repositório.
        """
        return await self.repository.count()

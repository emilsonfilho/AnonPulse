"""Módulo de serviço base com operações CRUD genéricas.

Este módulo fornece a classe BaseService que implementa operações
básicas de criação, leitura, atualização e exclusão (CRUD) de forma
genérica para qualquer modelo de dados.
"""

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
    """Serviço base genérico para operações CRUD.

    Fornece operações padrão de leitura, criação, atualização e exclusão
    de objetos através de um repositório, com mapeamento automático para
    esquemas de resposta.

    Atributos genéricos:
        ModelType: Tipo do modelo de dados.
        CreateSchemaType: Esquema de validação para criação.
        UpdateSchemaType: Esquema de validação para atualização.
        ResponseSchemaType: Esquema para resposta da API.
    """

    def __init__(
        self,
        repository: BaseRepository,
        response_schema: Type[ResponseSchemaType],
        not_found_exception: Type[Exception],
        already_exists_exception: Type[Exception] | None = None,
        default_load_options: list[Any] | None = None,
    ) -> None:
        """Inicializa o serviço base.

        Args:
            repository: Repositório para acesso aos dados.
            response_schema: Esquema para serialização de respostas.
            not_found_exception: Exceção a lançar quando objeto não é encontrado.
            already_exists_exception: Exceção a lançar quando objeto já existe.
                Padrão é None.
            default_load_options: Opções de carregamento padrão do SQLAlchemy.
                Padrão é None.
        """
        self.repository = repository
        self.response_schema = response_schema
        self.not_found_exception = not_found_exception
        self.already_exists_exception = already_exists_exception
        self.default_load_options = default_load_options

    async def get_or_raise(
        self, identifier: Any, options: list[Any] | None = None
    ) -> ModelType:
        """Obtém um objeto pelo identificador ou lança exceção.

        Args:
            identifier: Identificador único do objeto.
            options: Opções de carregamento do SQLAlchemy. Padrão é None.

        Returns:
            O objeto encontrado.

        Raises:
            not_found_exception: Se o objeto não é encontrado.
        """
        _options = options or self.default_load_options

        obj = await self.repository.get(identifier, options=_options)

        if not obj:
            raise self.not_found_exception()

        return obj

    async def list_all(
        self, params: Params, options: list[Any] | None = None
    ) -> Page[ResponseSchemaType]:
        """Lista todos os objetos com paginação.

        Args:
            params: Parâmetros de paginação.
            options: Opções de carregamento do SQLAlchemy. Padrão é None.

        Returns:
            Página contendo objetos mapeados para o esquema de resposta.
        """
        _options = options or self.default_load_options

        page = await self.repository.list_all(params, options=_options)

        page.items = [
            Mapper.to_response(obj, self.response_schema) for obj in page.items
        ]

        return page

    async def get_by_id(
        self, identifier: Any, options: list[Any] | None = None
    ) -> ResponseSchemaType:
        """Obtém um objeto pelo identificador e o mapeia.

        Args:
            identifier: Identificador único do objeto.
            options: Opções de carregamento do SQLAlchemy. Padrão é None.

        Returns:
            Objeto mapeado para o esquema de resposta.

        Raises:
            not_found_exception: Se o objeto não é encontrado.
        """
        obj = await self.get_or_raise(identifier, options=options)
        return Mapper.to_response(obj, self.response_schema)

    async def create(
        self, request: CreateSchemaType, identifier_value: Any | None = None
    ) -> ResponseSchemaType:
        """Cria um novo objeto.

        Args:
            request: Dados do objeto a criar, validados pelo esquema.
            identifier_value: Valor do identificador para verificar duplicatas.
                Padrão é None.

        Returns:
            Objeto criado mapeado para o esquema de resposta.

        Raises:
            already_exists_exception: Se o objeto com o identificador já existe.
        """
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
        self, identifier: Any, request: UpdateSchemaType,
        options: list[Any] | None = None
    ) -> ResponseSchemaType:
        """Atualiza um objeto existente.

        Args:
            identifier: Identificador único do objeto a atualizar.
            request: Dados a atualizar, validados pelo esquema.
            options: Opções de carregamento do SQLAlchemy. Padrão é None.

        Returns:
            Objeto atualizado mapeado para o esquema de resposta.

        Raises:
            not_found_exception: Se o objeto não é encontrado.
        """
        updated_obj = await self.repository.update(
            identifier, request.model_dump(exclude_unset=True),
        )

        _new_identifier = inspect(updated_obj).identity[0]

        _options = options or self.default_load_options

        updated_obj_with_rels = await self.get_or_raise(
            _new_identifier, options=_options
        )

        return Mapper.to_response(updated_obj_with_rels, self.response_schema)

    async def delete(self, identifier: Any) -> None:
        """Deleta um objeto.

        Args:
            identifier: Identificador único do objeto a deletar.

        Raises:
            not_found_exception: Se o objeto não é encontrado.
        """
        await self.get_or_raise(identifier)
        await self.repository.delete(identifier)

    async def count(self) -> int:
        """Conta o número total de objetos.

        Returns:
            Quantidade total de objetos.
        """
        return await self.repository.count()
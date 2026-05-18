"""Módulo de repositório base para acesso a dados.

Este módulo fornece a classe BaseRepository que implementa operações
CRUD genéricas para qualquer modelo SQLModel.
"""

from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func
from fastapi_pagination.ext.sqlalchemy import paginate
from app.core.exceptions.custom_exceptions import ResourceNotFoundException as Res

from typing import TypeVar, Generic, Type, Any

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """Repositório base genérico para operações CRUD.

    Fornece métodos assíncronos para criar, ler, atualizar, deletar
    e listar registros de qualquer modelo SQLModel.

    Atributos:
        model: O tipo de modelo SQLModel a ser gerenciado.
        session: Sessão assíncrona do SQLAlchemy.
    """

    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        """Inicializa o repositório com um modelo e sessão.

        Args:
            model: A classe do modelo SQLModel.
            session: A sessão assíncrona do SQLAlchemy.
        """
        self.model = model
        self.session = session

    async def get(self, identifier: Any, options: list[Any] | None = None) -> ModelType | None:
        """Obtém um registro pela chave primária.

        Args:
            identifier: O valor da chave primária a buscar.
            options: Opções adicionais de carregamento SQLAlchemy (opcional).

        Returns:
            O objeto do modelo ou None se não encontrado.
        """
        primary_key = list(self.model.__table__.primary_key.columns)[0]

        query = select(self.model).where(primary_key == identifier)

        if options:
            query = query.options(*options)

        result = await self.session.execute(query)

        return result.unique().scalars().first()

    async def list_all(self, params: Params, options: list[Any] | None = None) -> Page[ModelType]:
        """Lista todos os registros com paginação.

        Args:
            params: Parâmetros de paginação (página, tamanho, etc).
            options: Opções adicionais de carregamento SQLAlchemy (opcional).

        Returns:
            Uma página contendo os registros do modelo.
        """
        query = select(self.model)

        if options:
            query = query.options(*options)

        return await paginate(self.session, query, params)

    async def create(self, obj: ModelType) -> ModelType:
        """Cria um novo registro.

        Args:
            obj: O objeto do modelo a ser criado.

        Returns:
            O objeto criado com os dados persistidos.
        """
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, identifier: Any, obj_in: dict) -> ModelType:
        """Atualiza um registro existente.

        Args:
            identifier: O valor da chave primária do registro.
            obj_in: Dicionário com os dados a atualizar.

        Returns:
            O objeto atualizado.

        Raises:
            ResourceNotFoundException: Se o registro não for encontrado.
        """
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
        """Deleta um registro.

        Args:
            identifier: O valor da chave primária do registro a deletar.

        Raises:
            ResourceNotFoundException: Se o registro não for encontrado.
        """
        obj = await self.get(identifier)
        if not obj:
            raise Res(f"Sem resultados para {identifier} informado.")

        await self.session.delete(obj)
        await self.session.commit()

    async def count(self) -> int:
        """Conta a quantidade total de registros.

        Returns:
            O número total de registros do modelo.
        """
        stmt = select(func.count()).select_from(self.model)
        result = await self.session.execute(stmt)

        return result.scalar_one()
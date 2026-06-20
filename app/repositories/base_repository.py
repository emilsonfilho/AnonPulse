"""Módulo de repositório base para acesso a dados.

Este módulo fornece a classe BaseRepository que implementa operações
CRUD genéricas para qualquer modelo SQLModel.
"""

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.beanie import apaginate

from app.core.exceptions.custom_exceptions import ResourceNotFoundException
from beanie import Document, PydanticObjectId
from pydantic import BaseModel

from typing import TypeVar, Generic, Any

ModelType = TypeVar(
    "ModelType",
    bound=Document
)

class BaseRepository(Generic[ModelType]):
    """
        Repositório base genérico para operações CRUD.

        Fornece métodos assíncronos para criar, ler, atualizar, deletar
        e listar registros de qualquer modelo Beanie (MongoDB Document).
    """

    def __init__(self, model: type[ModelType]) -> None:
        """
            Inicializa o repositório com um modelo Beanie.

            Args:
                model: A classe do Document que será gerenciado pelo repositório.
        """
        self.model = model

    async def get(
            self,
            identifier: PydanticObjectId | str,
            fetch_links: bool = False
    ) -> ModelType | None:
        """
            Obtém um documento pelo seu ID.

            Args:
                identifier: ID do documento (ObjectId ou string).
                fetch_links: Se True, carrega os documentos relacionados (links).

            Returns:
                O documento encontrado ou None se não existir.
        """
        if isinstance(identifier, str):
            identifier = PydanticObjectId(identifier)

        return await self.model.get(identifier, fetch_links=fetch_links)

    async def list_all(
            self,
            params: Params,
            fetch_links: bool = False
    ) -> Page[ModelType]:
        """
            Lista documentos com paginação.

            Args:
                params: Parâmetros de paginação (página, tamanho, limite).
                fetch_links: Se True, carrega os documentos relacionados (links).

            Returns:
                Uma página contendo os documentos do MongoDB.
        """

        return await apaginate(
            self.model.find_all(
                fetch_links=fetch_links
            ),
            params
        )

    @staticmethod
    async def create(obj: ModelType) -> ModelType:
        """Cria um novo registro.

        Args:
            obj: O objeto do modelo a ser criado.

        Returns:
            O objeto criado com os dados persistidos.
        """
        return await obj.insert()

    async def update(self, identifier: Any, obj_in: dict | BaseModel) -> ModelType:
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
            raise ResourceNotFoundException(f"Sem resultados para {identifier} informado.")

        if isinstance(obj_in, BaseModel):
            obj_in = obj_in.model_dump(exclude_unset=True)

        return await obj.set(obj_in)

    async def delete(self, identifier: Any) -> None:
        """Deleta um registro.

        Args:
            identifier: O valor da chave primária do registro a deletar.

        Raises:
            ResourceNotFoundException: Se o registro não for encontrado.
        """
        obj = await self.get(identifier)
        if not obj:
            raise ResourceNotFoundException(f"Sem resultados para {identifier} informado.")

        await obj.delete()

    async def count(self) -> int:
        """Conta a quantidade total de registros.

        Returns:
            O número total de registros do modelo.
        """

        return await self.model.count()
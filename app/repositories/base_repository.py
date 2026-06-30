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

from app.core.pagination.pagination import Pagination

ModelType = TypeVar("ModelType", bound=Document)


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

    async def find_by(self, **filters) -> ModelType | None:
        """
        Busca um único documento no banco de dados com base nos filtros fornecidos.

        Realiza uma consulta assíncrona utilizando os critérios de busca passados
        como argumentos nomeados (`**filters`). A busca é configurada para resolver
        e recuperar automaticamente os documentos relacionados (via `fetch_links=True`).

        Args:
            **filters: Critérios de filtragem flexíveis para a consulta.

        Returns:
            ModelType | None: A instância do documento encontrado com os seus
                relacionamentos resolvidos, ou `None` caso nenhum registro
                corresponda aos critérios.
        """
        return await self.model.find_one(filters, fetch_links=True)

    async def get(
        self, identifier: PydanticObjectId, fetch_links: bool = False
    ) -> ModelType | None:
        """
        Obtém um documento pelo seu ID.

        Args:
            identifier: ID do documento (ObjectId ).
            fetch_links: Se True, carrega os documentos relacionados (links).

        Returns:
            O documento encontrado ou None se não existir.
        """

        return await self.model.get(identifier, fetch_links=fetch_links)

    async def list_all(
        self, params: Params, fetch_links: bool = False
    ) -> Page[ModelType]:
        """
        Lista documentos com paginação.

        Args:
            params: Parâmetros de paginação (página, tamanho, limite).
            fetch_links: Se True, carrega os documentos relacionados (links).

        Returns:
            Uma página contendo os documentos do MongoDB.
        """

        return await apaginate(self.model.find_all(fetch_links=fetch_links), params)

    async def create(self, obj: ModelType) -> ModelType:
        """Cria um registro.

        Args:
            obj: O objeto do modelo a ser criado.

        Returns:
            O objeto criado com os dados persistidos.
        """
        if isinstance(obj, dict):
            obj = self.model(**obj)
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
            raise ResourceNotFoundException(
                f"Sem resultados para {identifier} informado."
            )

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
            raise ResourceNotFoundException(
                f"Sem resultados para {identifier} informado."
            )

        await obj.delete()

    async def count(self) -> int:
        """Conta a quantidade total de registros.

        Returns:
            O número total de registros do modelo.
        """

        return await self.model.count()

    async def _paginate_aggregation(
        self, aggregation: list, params: Params
    ) -> Page[Any]:
        """
        Executa um pipeline de agregação e formata os resultados com paginação.

        Args:
            - aggregation (list): O pipeline de agregação do MongoDB a ser executado.
            - params (Params): Os parâmetros de paginação (como número e tamanho da
                página) que serão utilizados para formatar a resposta final.

        Returns:
            Page[Any]: um objeto de resposta paginada contendo os itens retornados
                pela agregação, a contagem total de registros e os parâmetros
                de paginação aplicados.
        """
        results = await self.model.aggregate(aggregation).to_list()
        data = results[0]
        return Page.create(
            items=data["items"],
            total=data["total"][0]["count"] if data["total"] else 0,
            params=params,
        )

    @staticmethod
    def _facet_stage(params: Params, sort: dict | None = None) -> dict:
        """
        Cria o estágio de agregação `$facet` para paginação e ordenação no MongoDB.

        Args:
            - params (Params): Os parâmetros de paginação contendo informações como
                a página atual e o limite de itens por página.
            - sort (dict | None, opcional): Um dicionário de ordenação no formato do
                MongoDB (ex: {"campo": 1}). Padrão é None.

        Returns:
            dict: O dicionário formatado representando o estágio `$facet` pronto
                para ser anexado a um pipeline de agregação.
        """
        p = Pagination.from_params(params)

        items = []

        if sort:
            items.append({"$sort": sort})

        items.extend([{"$skip": p.skip}, {"$limit": p.limit}])

        return {"$facet": {"items": items, "total": [{"$count": "count"}]}}

    @staticmethod
    async def _find_by_linked(
        model: type[Document],
        lookup_expr: Any,
        source_model: type[Document],
        link_field: str,
        exception: Exception,
        params: Params,
        fetch_links: bool = False,
    ) -> Page[Any]:
        """
        Busca documentos vinculados a um registro específico com paginação.

        Args:
            model (type[Document]): O modelo do documento base a ser localizado.
            lookup_expr (Any): A expressão de filtro (critérios de busca) para
                encontrar o documento base.
            source_model (type[Document]): O modelo que contém os registros
                vinculados a serem retornados.
            link_field (str): O nome do campo no `source_model` que armazena a
                referência (link) para o documento base.
            exception (Exception): A instância da exceção a ser lançada caso o
                documento base não seja encontrado.
            params (Params): Os parâmetros de paginação.
            fetch_links (bool, opcional): Indica se os relacionamentos dos
                documentos finais devem ser resolvidos. Padrão é False.

        Returns:
            Page[Any]: Um objeto de resposta paginada contendo os documentos
                do `source_model` que estão vinculados ao registro base.

        Raises:
            Exception: A exceção fornecida no argumento `exception` se a
                consulta inicial no `model` não retornar nenhum documento.
        """
        doc = await model.find_one(lookup_expr)  # type: ignore

        if not doc:
            raise exception

        assert doc is not None
        query = source_model.find(
            {f"{link_field}.$id": doc.id}, fetch_links=fetch_links
        )

        return await apaginate(query, params)

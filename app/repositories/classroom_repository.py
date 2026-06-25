from beanie import PydanticObjectId
from fastapi_pagination import Page, Params

from app.models.classroom import Classroom
from app.models.subject import Subject
from app.repositories.base_repository import BaseRepository

from app.core.exceptions.custom_exceptions import SubjectNotFoundException


class ClassroomRepository(BaseRepository[Classroom]):
    """
    Repositório para gerenciar as operações de banco de dados da entidade Classroom.

    Esta classe herda de BaseRepository e fornece métodos de consulta específicos
    para a entidade de turmas (Classroom), permitindo listagens filtradas por
    relacionamentos com suporte a paginação e carregamento ansioso (eager loading).
    """

    def __init__(self) -> None:
        """
        Inicializa o repositório de turmas.
        """
        super().__init__(model=Classroom)

    async def find_by(self, **filters) -> Classroom | None:
        return await self.model.find_one(filters)

    async def list_by_professor(
        self, professor_id: PydanticObjectId, params: Params, fetch_links: bool = False
    ) -> Page[Classroom]:
        """
        Lista de forma paginada todas as turmas associadas a um determinado professor.

        Args:
            professor_id: O identificador único do professor.
            params (Params): Parâmetros de paginação fornecidos pelo fastapi-pagination
                (página atual e limite de itens).
            fetch_links: Se True, carrega os documentos relacionados (links).

        Returns:
            Page[Classroom]: Objeto paginado contendo a lista de turmas encontradas
                e os metadados de paginação.
        """
        if isinstance(professor_id, str):
            professor_id = PydanticObjectId(professor_id)

        query = self.model.find(
            self.model.professor.id == professor_id, fetch_links=fetch_links
        )

        total = await query.count()

        skip = (params.page - 1) * params.size

        items = await query.skip(skip).limit(params.size).to_list()

        return Page.create(items=items, total=total, params=params)

    async def list_by_subject(
        self, subject_cod: str, params: Params, fetch_links: bool = False
    ) -> Page[Classroom]:
        """
        Lista de forma paginada todas as turmas vinculadas a uma determinada disciplina.

        Args:
            subject_cod (str): O código de identificação da disciplina (ex: "QXD123").
            params (Params): Parâmetros de paginação fornecidos pelo fastapi-pagination.
            fetch_links: Se True, carrega os documentos relacionados (links).

        Returns:
            Page[Classroom]: Objeto paginado contendo a lista de turmas encontradas
                e os metadados de paginação.
        """
        subject = await Subject.find_one(Subject.cod == subject_cod)
        if not subject:
            raise SubjectNotFoundException()

        query = self.model.find(
            self.model.subject.id == subject.id, fetch_links=fetch_links
        )

        total = await query.count()

        skip = (params.page - 1) * params.size
        items = await query.skip(skip).limit(params.size).to_list()

        return Page.create(items=items, total=total, params=params)

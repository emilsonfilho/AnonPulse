from datetime import datetime
from typing import Any

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.beanie import apaginate

from app.models import (
    Classroom,
    Monitor, Student
)
from app.models.feedback import Feedback
from app.models.monitor_assignment import MonitorAssignment
from app.models.subject import Subject
from app.repositories.base_repository import BaseRepository
from app.core.exceptions.custom_exceptions import MonitorNotFoundException, StudentNotFoundException

class FeedbackRepository(BaseRepository[Feedback]):
    """
    Repositório para gerenciar as operações de banco de dados da entidade Feedback.

    Esta classe herda de BaseRepository e implementa as consultas complexas e
    específicas exigidas pelo TP2, incluindo buscas textuais parciais, filtros
    por intervalo de datas, agrupamentos, contagens e joins multi-entidades.
    """

    def __init__(self) -> None:
        """
        Inicializa o repositório de feedbacks.
        """
        super().__init__(model=Feedback)

    async def search_by_text(self, term: str, params: Params) -> Page[Feedback]:
        """
        Realiza uma busca paginada por texto parcial no conteúdo dos feedbacks.

        Atende ao requisito de busca por texto parcial usando correspondência
        insensível a maiúsculas/minúsculas (ILIKE), ordenada pelos mais recentes.

        Args:
            term (str): O termo ou palavra-chave para buscar no texto do feedback.
            params (Params): Parâmetros de paginação do fastapi-pagination.

        Returns:
            Page[Feedback]: Objeto paginado contendo os feedbacks filtrados.
        """
        search_term = f"%{term}%"

        query = self.model.find(
            { "text": { "$regex": search_term, "$options": "i" } }
        ).sort("-created_at")

        return await apaginate(query, params)

    async def list_by_monitor(
            self,
            monitor_registration: str,
            params: Params,
            fetch_links: bool = False
    ) -> Page[Feedback]:
        """
        Lista de forma paginada os feedbacks recebidos por um monitor específico.

        Realiza um relacionamento implícito (JOIN) com a atribuição de monitoria
        para filtrar as mensagens destinadas à matrícula informada.

        Args:
            monitor_registration (str): A matrícula do monitor alvo do filtro.
            params (Params): Parâmetros de paginação do fastapi-pagination.
            fetch_links: Se True, carrega os documentos relacionados (links).

        Returns:
            Page[Feedback]: Objeto paginado com os feedbacks vinculados ao monitor.
        """

        pipeline = [
            {
                "$lookup": {
                    "from": "monitor_assignments",
                    "localField": "assignment.$id",
                    "foreignField": "_id",
                    "as": "assignment"
                }
            },
            {"$unwind": "$assignment"},
            {
                "$lookup": {
                    "from": "monitors",
                    "localField": "assignment.monitor.$id",
                    "foreignField": "_id",
                    "as": "monitor"
                }
            },
            {"$unwind": "$monitor"},
            {
                "$match": {
                    "monitor.registration": monitor_registration
                }
            },
            BaseRepository._facet_stage(params)
        ]

        return await self._paginate_aggregation(pipeline, params)

    async def count_by_monitor(self, params: Params) -> Page[Any]:
        """
        Realiza uma agregação estatística computando o total de feedbacks por monitor.

        Atende ao requisito de agregações e contagens através do agrupamento (GROUP BY)
        e contagem de registros utilizando funções agregadas do banco de dados.

        Args:
            params (Params): Parâmetros de paginação do fastapi-pagination.

        Returns:
            Page[Any]: Objeto paginado contendo tuplas ou dicionários com a
                matrícula do monitor e a respectiva contagem de feedbacks.
        """

        pipeline = [
            {
                "$group": {
                    "_id": "$monitor_registration",
                    "count": { "$sum": 1 }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "monitor_registration": "$_id",
                    "count": 1
                }
            },
            {
                "$sort": { "count": -1 }
            },
            BaseRepository._facet_stage(params, sort={ "count": -1 })
        ]

        return await self._paginate_aggregation(pipeline, params)

    async def count_by_subject(self, params: Params) -> Page[Any]:
        """
        Executa uma consulta complexa envolvendo múltiplas entidades para contar feedbacks por disciplina.

        Cumpre o requisito de consultas complexas cruzando 4 tabelas relacionais
        (Feedback -> MonitorAssignment -> Classroom -> Subject) para agrupar e
        contar o volume de mensagens por nome de disciplina.

        Args:
            params (Params): Parâmetros de paginação do fastapi-pagination.

        Returns:
            Page[Any]: Objeto paginado contendo o nome da disciplina e a
                quantidade total de feedbacks que ela acumulou.
        """

        pipeline = [
            {
                "$addFields": {
                    "assignment_id": "$assignment.$id",
                }
            },
            {
                "$lookup": {
                    "from": "monitor_assignments",
                    "localField": "assignment_id",
                    "foreignField": "_id",
                    "as": "assignment"
                }
            },
            { "$unwind": "$assignment" },
            {
                "$addFields": {
                    "classroom_id": "$assignment.classroom.$id",
                }
            },
            {
                "$lookup": {
                    "from": "classrooms",
                    "localField": "classroom_id",
                    "foreignField": "_id",
                    "as": "classroom"
                }
            },
            { "$unwind": "$classroom" },
            {
                "$addFields": {
                    "subject_id": "$classroom.subject.$id",
                }
            },
            {
                "$lookup": {
                    "from": "subjects",
                    "localField": "subject_id",
                    "foreignField": "_id",
                    "as": "subject"
                }
            },
            { "$unwind": "$subject" },
            {
                "$group": {
                    "_id": "$subject.name",
                    "feedback_count": { "$sum": 1 }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "subject_name": "$_id",
                    "feedback_count": 1
                }
            },
            BaseRepository._facet_stage(params, sort={ "feedback_count": -1 }),
        ]

        return await self._paginate_aggregation(pipeline, params)

    async def list_by_date_range(
        self,
        params: Params,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        year: int | None = None,
    ) -> Page[Feedback]:
        """
        Filtra os feedbacks registrados dentro de um intervalo de datas específico
        ou por ano.

        Atende ao requisito de filtros por data/ano. Permite limites abertos
        caso apenas uma das datas limitantes seja fornecida. Se `year` for
        informado, filtra apenas pelo ano de criação do feedback.

        Args:
            params (Params): Parâmetros de paginação do fastapi-pagination.
            start_date (datetime | None, opcional): Data e hora inicial do filtro.
            end_date (datetime | None, opcional): Data e hora final do filtro.
            year (int | None, opcional): Ano para filtrar os feedbacks.

        Returns:
            Page[Feedback]: Objeto paginado contendo os feedbacks pertencentes ao período.
        """
        match: dict = {}

        if start_date:
            match.setdefault("created_at", {})["$gte"] = start_date

        if end_date:
           match.setdefault("created_at", {})["$lte"] = end_date

        if year is not None:
            match["$expr"] = {
                "$eq": [
                    { "$year": "$created_at" },
                    year
                ]
            }

        pipeline = [
            *([ { "$match": match } ] if match else []),
            { "$sort": { "created_at": -1 } },
            BaseRepository._facet_stage(params)
        ]

        return await self._paginate_aggregation(pipeline, params)

    async def list_by_student_hash(
            self,
            student_hash: str,
            params: Params,
            fetch_links: bool = False
    ) -> Page[Feedback]:
        """
        Busca de forma paginada todos os feedbacks pertencentes a um hash de aluno.

        Garante a integridade do anonimato mapeando apenas a assinatura digital
        criptografada (hash) do estudante criador sem expor seus dados originais.

        Args:
            student_hash (str): O hash gerado a partir da matrícula do aluno.
            params (Params): Parâmetros de paginação do fastapi-pagination.
            fetch_links: Se True, carrega os documentos relacionados (links).

        Returns:
            Page[Feedback]: Objeto paginado contendo os feedbacks do aluno anônimo.
        """

        query = self.model.find(
            self.model.registration == student_hash,
            fetch_links=fetch_links
        )

        return await apaginate(query, params)
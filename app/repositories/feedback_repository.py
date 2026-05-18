from datetime import datetime
from typing import Any

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.classroom import Classroom
from app.models.feedback import Feedback
from app.models.monitor_assignment import MonitorAssignment
from app.models.subject import Subject
from app.repositories.base_repository import BaseRepository


class FeedbackRepository(BaseRepository[Feedback]):
    """
    Repositório para gerenciar as operações de banco de dados da entidade Feedback.

    Esta classe herda de BaseRepository e implementa as consultas complexas e
    específicas exigidas pelo TP2, incluindo buscas textuais parciais, filtros
    por intervalo de datas, agrupamentos, contagens e joins multi-entidades.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Inicializa o repositório de feedbacks.

        Args:
            session (AsyncSession): Sessão assíncrona do banco de dados
                gerenciada pelo SQLAlchemy/SQLModel.
        """
        super().__init__(model=Feedback, session=session)

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

        query = (
            select(self.model)
            .where(self.model.text.ilike(search_term))
            .order_by(self.model.created_at.desc())
        )

        return await paginate(self.session, query, params)

    async def list_by_monitor(
        self, monitor_registration: str, params: Params
    ) -> Page[Feedback]:
        """
        Lista de forma paginada os feedbacks recebidos por um monitor específico.

        Realiza um relacionamento implícito (JOIN) com a atribuição de monitoria
        para filtrar as mensagens destinadas à matrícula informada.

        Args:
            monitor_registration (str): A matrícula do monitor alvo do filtro.
            params (Params): Parâmetros de paginação do fastapi-pagination.

        Returns:
            Page[Feedback]: Objeto paginado com os feedbacks vinculados ao monitor.
        """
        query = (
            select(self.model)
            .join(MonitorAssignment)
            .where(MonitorAssignment.monitor_registration == monitor_registration)
        )

        return await paginate(self.session, query, params)

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
        query = (
            select(MonitorAssignment.monitor_registration, func.count(self.model.id))
            .join(MonitorAssignment)
            .group_by(MonitorAssignment.monitor_registration)
        )

        return await paginate(self.session, query, params)

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
        query = (
            select(
                Subject.name.label("subject_name"),
                func.count(self.model.id).label("feedback_count"),
            )
            .select_from(self.model)
            .join(MonitorAssignment)
            .join(Classroom)
            .join(Subject)
            .group_by(Subject.name)
        )

        return await paginate(
            self.session,
            query,
            params,
            transformer=lambda items: [
                {
                    "subject_name": item.subject_name,
                    "feedback_count": item.feedback_count,
                }
                for item in items
            ],
        )

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
        query = select(self.model)

        if start_date:
            query = query.where(self.model.created_at >= start_date)

        if end_date:
            query = query.where(self.model.created_at <= end_date)

        if year is not None:
            query = query.where(func.strftime('%Y', self.model.created_at) == str(year))

        query = query.order_by(self.model.created_at.desc())

        return await paginate(self.session, query, params)

    async def list_by_student_hash(
        self, student_hash: str, params: Params, options: list[Any] | None = None
    ) -> Page[Feedback]:
        """
        Busca de forma paginada todos os feedbacks pertencentes a um hash de aluno.

        Garante a integridade do anonimato mapeando apenas a assinatura digital
        criptografada (hash) do estudante criador sem expor seus dados originais.

        Args:
            student_hash (str): O hash gerado a partir da matrícula do aluno.
            params (Params): Parâmetros de paginação do fastapi-pagination.
            options (list[Any] | None, opcional): Lista de estratégias de eager
                loading (joinedload/selectinload) do SQLAlchemy.

        Returns:
            Page[Feedback]: Objeto paginado contendo os feedbacks do aluno anônimo.
        """
        query = select(self.model).where(self.model.registration == student_hash)

        if options:
            query = query.options(*options)

        return await paginate(self.session, query, params)

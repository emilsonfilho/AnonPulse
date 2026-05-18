"""Serviço de Feedback.

Este módulo fornece a implementação do FeedbackService, responsável pelas
operações de criação, listagem e contagem de feedbacks.
"""

from datetime import date, datetime, timezone
from fastapi_pagination import Params, Page
from sqlalchemy.orm import joinedload

from app.core.exceptions.custom_exceptions import FeedbackNotFoundException
from app.core.mapper import Mapper
from app.models.feedback import Feedback
from app.schemas.feedback_schema import (
    CreateFeedbackRequest,
    UpdateFeedbackRequest,
    FeedbackResponse,
    FeedbackSubjectReportResponse,
)
from app.services.base_service import BaseService

from app.core.enums import HashAlgorithm
from app.services.hash_service import HashService

class FeedbackService(BaseService[
    Feedback, 
    CreateFeedbackRequest, 
    UpdateFeedbackRequest, 
    FeedbackResponse
]):
    def __init__(self, repository) -> None:
        """Inicializa o serviço de feedback.

        Args:
            repository: Repositório utilizado para persistência e consulta de
                objetos Feedback.
        """
        super().__init__(
            repository=repository,
            response_schema=FeedbackResponse,
            not_found_exception=FeedbackNotFoundException,
            default_load_options=[
                joinedload(Feedback.type),
                joinedload(Feedback.assignment)
            ]
        )

    async def create(self, request: CreateFeedbackRequest) -> FeedbackResponse:
        """Cria um novo feedback.

        Converte a matrícula do estudante em um hash para manter o anonimato e
        persiste o feedback no repositório.

        Args:
            request: Dados do feedback a ser criado.

        Returns:
            FeedbackResponse: Representação do feedback criado.
        """

        request_data = request.model_dump()

        identificador_aluno = request_data["registration"]
        hash_aluno = HashService.generate_hash(
            identificador_aluno, HashAlgorithm.SHA256
        )

        request_data["registration"] = hash_aluno

        feedback = Feedback(**request_data)

        new_feedback = await self.repository.create(feedback)

        return Mapper.to_response(new_feedback, FeedbackResponse)

    async def list_by_student(self, raw_registration: str, params: Params, options: list | None = None) -> Page[FeedbackResponse]:
        """Lista feedbacks de um estudante a partir da matrícula não-hashed.

        Gera o hash da matrícula fornecida para preservar anonimato e realiza a
        busca paginada dos feedbacks associados a esse hash, carregando
        relacionamentos pré-definidos.

        Args:
            raw_registration: Matrícula em texto puro do estudante.
            params: Parâmetros de paginação.
            options: Opções de carregamento (joinedload) adicionais.

        Returns:
            Page[FeedbackResponse]: Página de respostas de feedback.
        """
        student_hash = HashService.generate_hash(raw_registration, HashAlgorithm.SHA256)

        _options = options or self.default_load_options

        page = await self.repository.list_by_student_hash(student_hash, params, options=_options)
        page.items = [Mapper.to_response(obj, self.response_schema) for obj in page.items]
        
        return page

    async def list_by_monitor(self, monitor_registration: str, params: Params) -> Page[FeedbackResponse]:
        page_result = await self.repository.list_by_monitor(monitor_registration, params)

        page_result.items = [ 
            Mapper.to_response(feedback, self.response_schema) for feedback in page_result.items
        ]

        return page_result

    async def search(self, q: str, params: Params) -> Page[FeedbackResponse]:
        """Busca paginada por texto parcial nos feedbacks e mapeia para respostas.

        Args:
            q: Termo de busca parcial.
            params: Parâmetros de paginação.

        Returns:
            Page[FeedbackResponse]: Página com resultados mapeados.
        """
        page = await self.repository.search_by_text(q, params)
        page.items = [Mapper.to_response(obj, self.response_schema) for obj in page.items]
        return page

    async def report_by_subject(self, params: Params) -> Page[FeedbackSubjectReportResponse]:
        """Relatório paginado de quantidade de feedbacks por disciplina."""
        page = await self.repository.count_by_subject(params)
        return page

    async def list_by_date(
        self,
        params: Params,
        start_date: date | None = None,
        end_date: date | None = None,
        year: int | None = None,
    ) -> Page[FeedbackResponse]:
        """Lista feedbacks filtrados por data ou ano e mapeia para respostas."""
        start_dt = (
            datetime(start_date.year, start_date.month, start_date.day, tzinfo=timezone.utc)
            if start_date
            else None
        )
        end_dt = (
            datetime(
                end_date.year,
                end_date.month,
                end_date.day,
                23,
                59,
                59,
                999999,
                tzinfo=timezone.utc,
            )
            if end_date
            else None
        )

        page = await self.repository.list_by_date_range(
            params, start_date=start_dt, end_date=end_dt, year=year
        )
        page.items = [Mapper.to_response(obj, self.response_schema) for obj in page.items]
        return page

    async def count_feedbacks(self) -> int:
        """Retorna a contagem total de feedbacks.

        Returns:
            int: Número total de feedbacks armazenados.
        """

        return await self.repository.count()

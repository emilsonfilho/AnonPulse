"""Serviço de Feedback.

Este módulo fornece a implementação do FeedbackService, responsável pelas
operações de criação, listagem e contagem de feedbacks.
"""

from datetime import date, datetime, timezone

from beanie import Link
from fastapi_pagination import Params, Page

from app.core.exceptions.custom_exceptions import FeedbackNotFoundException
from app.core.mapper import Mapper
from app.models.feedback import Feedback
from app.models.monitor import Monitor
from app.models.classroom import Classroom
from app.repositories.feedback_repository import FeedbackRepository
from app.schemas.feedback_schema import (
    CreateFeedbackRequest,
    UpdateFeedbackRequest,
    FeedbackResponse,
    FeedbackSubjectReportResponse,
)
from app.services.base_service import BaseService
from app.core.enums import HashAlgorithm
from app.services.hash_service import HashService
from app.utils.pagination_utils import map_page

class FeedbackService(BaseService[
    Feedback, 
    CreateFeedbackRequest, 
    UpdateFeedbackRequest, 
    FeedbackResponse
]):
    repository: FeedbackRepository

    def __init__(self, repository: FeedbackRepository) -> None:
        """Inicializa o serviço de feedback.
        """
        super().__init__(
            repository=repository,
            response_schema=FeedbackResponse,
            not_found_exception=FeedbackNotFoundException,
        )

    async def create(self, request: CreateFeedbackRequest) -> FeedbackResponse:
        """Cria um ‘feedback’.

        Converte a matrícula do estudante em um hash para manter o anonimato e
        persiste o ‘feedback’ no repositório.

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

        await new_feedback.fetch_all_links()

        return Mapper.to_response(new_feedback, FeedbackResponse)

    async def _materialize_feedback_dict(self, fb: Feedback) -> dict:
        """Materializa um feedback em dict serializável com links resolvidos.
        
        Resolve Links aninhados (assignment → monitor/classroom) através de
        fetch() ou consultas explícitas, garantindo campos não-nulos para
        validação Pydantic.
        
        Args:
            fb: Documento Feedback com potenciais Links não materializados.
            
        Returns:
            dict compatível com FeedbackResponse schema.
        """
        data = {
            "id": getattr(fb, "id", None),
            "created_at": getattr(fb, "created_at", None),
            "registration": getattr(fb, "registration", None),
            "text": getattr(fb, "text", None),
            "rating": getattr(fb, "rating", None),
            "type": getattr(fb, "type", None),
            "assignment": None,
        }

        assignment = getattr(fb, "assignment", None)
        if assignment is None:
            return data

        # Materializa Link de assignment
        if isinstance(assignment, Link):
            try:
                assignment = await assignment.fetch()
            except Exception:
                return data

        if assignment is None:
            return data

        assign_dict = {
            "id": getattr(assignment, "id", None),
            "weekly_hours": getattr(assignment, "weekly_hours", None),
        }

        # Materializa monitor
        mon = await self._fetch_or_query(getattr(assignment, "monitor", None), Monitor)
        if mon is not None:
            assign_dict["monitor"] = {
                "registration": getattr(mon, "registration", None) or "",
                "name": getattr(mon, "name", None) or "",
            }

        # Materializa classroom
        clsrm = await self._fetch_or_query(getattr(assignment, "classroom", None), Classroom)
        if clsrm is not None:
            assign_dict["classroom"] = {"cod": getattr(clsrm, "cod", None) or ""}

        data["assignment"] = assign_dict
        return data

    async def _fetch_or_query(self, obj, model_class):
        """Tenta fetch() de Link ou consulta explícita por id.
        
        Args:
            obj: Link ou Document a materializar.
            model_class: Classe do modelo (Monitor, Classroom).
            
        Returns:
            Documento materializado ou None.
        """
        if obj is None:
            return None

        # Se for Link, tente fetch
        if isinstance(obj, Link):
            try:
                return await obj.fetch()
            except Exception:
                pass

        # Se é documento com campos obrigatórios, retorna
        if hasattr(obj, "id") or hasattr(obj, "_id"):
            if (model_class == Monitor and hasattr(obj, "registration")) or \
               (model_class == Classroom and hasattr(obj, "cod")):
                return obj

        # Tenta consulta por id
        obj_id = getattr(obj, "id", None) or getattr(obj, "_id", None)
        if obj_id is not None:
            try:
                return await model_class.find_one(model_class.id == obj_id)
            except Exception:
                pass

        return None

    async def list_by_student(self, raw_registration: str, params: Params) -> Page[FeedbackResponse]:
        """Lista feedbacks de um estudante (anônimo via hash).

        Gera hash da matrícula para preservar anonimato e busca feedbacks
        associados, carregando relacionamentos.

        Args:
            raw_registration: Matrícula em texto puro do estudante.
            params: Parâmetros de paginação.

        Returns:
            Page[FeedbackResponse]: Feedbacks do estudante.
        """
        student_hash = HashService.generate_hash(raw_registration, HashAlgorithm.SHA256)
        page = await self.repository.list_by_student_hash(
            student_hash, params, fetch_links=self.default_fetch_links
        )

        def _map_obj(obj):
            if hasattr(obj, "model_dump"):
                data = obj.model_dump()
            else:
                data = getattr(obj, "__dict__", obj)

            if getattr(obj, "assignment", None) is not None:
                assign = obj.assignment
                assign_dict = data.get("assignment") or {}

                mon = getattr(assign, "monitor", None)
                if mon is not None and hasattr(mon, "registration"):
                    assign_dict["monitor"] = {
                        "registration": mon.registration,
                        "name": getattr(mon, "name", None),
                    }

                clsrm = getattr(assign, "classroom", None)
                if clsrm is not None and hasattr(clsrm, "cod"):
                    assign_dict["classroom"] = {"cod": clsrm.cod}

                data["assignment"] = assign_dict

            return Mapper.to_response(data, self.response_schema)

        return map_page(page, lambda obj: _map_obj(obj))

    async def list_by_monitor(self, monitor_registration: str, params: Params) -> Page[FeedbackResponse]:
        """Lista feedbacks recebidos por um monitor específico.
        
        Args:
            monitor_registration: Matrícula do monitor.
            params: Parâmetros de paginação.
            
        Returns:
            Page[FeedbackResponse]: Feedbacks do monitor.
        """
        page_result = await self.repository.list_by_monitor(monitor_registration, params)
        return map_page(page_result, lambda obj: Mapper.to_response(obj, self.response_schema))

    async def search(self, q: str, params: Params) -> Page[FeedbackResponse]:
        """Busca por texto parcial em feedbacks.

        Args:
            q: Termo de busca parcial.
            params: Parâmetros de paginação.

        Returns:
            Page[FeedbackResponse]: Resultados da busca.
        """
        page = await self.repository.search_by_text(q, params)

        # Materializa cada feedback para garantir validação Pydantic
        items = [await self._materialize_feedback_dict(fb) for fb in page.items]
        page_with_dicts = Page.create(
            items=items, 
            total=page.total, 
            params=Params(page=page.page, size=page.size)
        )

        return map_page(
            page_with_dicts,
            lambda obj: Mapper.to_response(obj, self.response_schema),
        )

    async def report_by_subject(self, params: Params) -> Page[FeedbackSubjectReportResponse]:
        """Relatório de quantidade de feedbacks agrupados por disciplina.
        
        Args:
            params: Parâmetros de paginação.
            
        Returns:
            Page com contagem de feedbacks por disciplina.
        """
        return await self.repository.count_by_subject(params)

    async def list_by_date(
        self,
        params: Params,
        start_date: date | None = None,
        end_date: date | None = None,
        year: int | None = None,
    ) -> Page[FeedbackResponse]:
        """Lista feedbacks filtrados por data ou ano.
        
        Args:
            params: Parametros de paginacao.
            start_date: Data inicial (opcionalmente com hora).
            end_date: Data final (opcionalmente com hora).
            year: Filtro alternativo por ano.
            
        Returns:
            Page[FeedbackResponse]: Feedbacks no periodo.
        """
        # Converte date para datetime UTC
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

        # Busca documentos para poder materializar links
        page = await self.repository.list_by_date_range(
            params, start_date=start_dt, end_date=end_dt, year=year, fetch_documents=True
        )

        # Materializa cada feedback
        items = []
        for fb in page.items:
            try:
                items.append(await self._materialize_feedback_dict(fb))
            except Exception:
                # Fallback: feedback sem relacionamentos
                items.append({
                    "id": getattr(fb, "id", None),
                    "created_at": getattr(fb, "created_at", None),
                    "registration": getattr(fb, "registration", None),
                    "text": getattr(fb, "text", None),
                    "rating": getattr(fb, "rating", None),
                    "type": getattr(fb, "type", None),
                    "assignment": None,
                })

        page_with_dicts = Page.create(
            items=items, 
            total=page.total, 
            params=Params(page=page.page, size=page.size)
        )

        return map_page(
            page_with_dicts,
            lambda obj: Mapper.to_response(obj, self.response_schema),
        )

    async def count_feedbacks(self) -> int:
        """Retorna contagem total de feedbacks no banco.
        
        Returns:
            int: Total de feedbacks.
        """
        return await self.repository.count()


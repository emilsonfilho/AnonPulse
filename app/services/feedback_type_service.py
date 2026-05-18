"""Serviço para gerenciar tipos de feedback.

Este módulo contém a lógica de negócio para operações relacionadas aos tipos
de feedback, incluindo criação e outras operações herdadas da classe base.
"""
from datetime import datetime, timezone

from app.core.exceptions.custom_exceptions import FeedbackNotFoundException
from app.core.mapper import Mapper
from app.models.feedback_type import FeedbackType
from app.repositories.feedback_repository import FeedbackRepository
from app.schemas.feedback_type_schema import (
    CreateFeedbackTypeRequest,
    UpdateFeedbackTypeRequest,
    FeedbackTypeResponse
)
from app.services.base_service import BaseService


class FeedbackTypeService(
    BaseService[
        FeedbackType, CreateFeedbackTypeRequest, UpdateFeedbackTypeRequest, FeedbackTypeResponse
    ]
):
    """Serviço para operações relacionadas aos tipos de feedback.

    Fornece funcionalidades para criar, atualizar, deletar e recuperar
    tipos de feedback do repositório.

    Attributes:
        repository: Repositório para acesso aos dados de feedback.
        response_schema: Schema de resposta para serialização de dados.
        not_found_exception: Exceção lançada quando um tipo não é encontrado.
    """

    def __init__(self, repository: FeedbackRepository) -> None:
        """Inicializa o serviço de tipos de feedback.

        Args:
            repository: Instância do repositório de feedback.
        """
        super().__init__(
            repository=repository,
            response_schema=FeedbackTypeResponse,
            not_found_exception=FeedbackNotFoundException,
        )

    async def create(self, request: CreateFeedbackTypeRequest) -> FeedbackTypeResponse:
        """Cria um novo tipo de feedback.

        Args:
            request: Dados para criar o tipo de feedback.

        Returns:
            FeedbackTypeResponse: Tipo de feedback criado com seus dados.
        """
        feedback = FeedbackType(
            **request.model_dump(), created_at=datetime.now(timezone.utc)
        )

        new_feedback = await self.repository.create(feedback)

        return Mapper.to_response(new_feedback, FeedbackTypeResponse)

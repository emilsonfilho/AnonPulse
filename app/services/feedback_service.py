from datetime import datetime, timezone

from app.api.routers.feedback import CreateFeedbackRequest, UpdateFeedbackRequest
from app.core.enums import HashAlgorithm
from app.core.exceptions.custom_exceptions import ResourceNotFoundException
from app.schemas.feedback_schema import FeedbackResponse
from app.services.hash_service import HashService


class FeedbackService:
    def __init__(self) -> None:
        pass  # Instanciar Session do SQLModel aqui depois

    def validate_feedback_exists(self, feedback_id):
        if not self.feedback_repository.get_by_id(feedback_id):
            raise ResourceNotFoundException(
                f"Feedback com ID {feedback_id} não encontrado."
            )

    def criar_feedback(self, dados: CreateFeedbackRequest) -> FeedbackResponse:
        # data = dados.model_dump()

        identificador_aluno = dados.identificador_aluno

        hash_gerado = HashService.generate_hash(
            identificador_aluno, HashAlgorithm.SHA256
        )

        # Mock para testes (implementar)
        return FeedbackResponse(
            id=1,
            disciplina_id=10,  # ID fake de uma disciplina
            monitor_id=5,  # ID fake de um monitor
            tipo_mensagem=dados.tipo_mensagem,
            texto_feedback=dados.texto_feedback,
            data_submissao=datetime.now(timezone.utc),
            hash_aluno=hash_gerado,
        )

    def obter_feedbacks(self, skip: int, limit: int) -> list[FeedbackResponse]:
        # Mock temporario
        return []

    def obter_feedback_por_id(self, feedback_id: int) -> FeedbackResponse:
        # Lança erro 404 automaticamente para testar o handler, já que não temos banco ainda
        raise ResourceNotFoundException("Mock: Banco de dados ainda não conectado.")

    def deletar_feedback(self, feedback_id: int) -> None:
        pass

    def atualizar_feedback(self, feedback_id: int, novos_dados: UpdateFeedbackRequest):
        pass

    def count_feedbacks(self) -> int:
        return 0

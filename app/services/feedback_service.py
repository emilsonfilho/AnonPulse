from itertools import islice

from app.api.core.enums import HashAlgorithm
from app.api.core.exceptions.custom_exceptions import ResourceNotFoundException
from app.api.routers.feedback import CreateFeedbackRequest, UpdateFeedbackRequest
from app.api.schemas.feedback_schema import FeedbackResponse
from app.database.delta_manager import FeedbackRepository
from app.models.feedback import Feedback
from app.services.hash_service import HashService


class FeedbackService:
    def __init__(self) -> None:
        self.feedback_repository = FeedbackRepository("data/feedbacks_delta")

    def validate_feedback_exists(self, feedback_id):
        if not self.feedback_repository.get_by_id(feedback_id):
            raise ResourceNotFoundException(
                f"Feedback com ID {feedback_id} não encontrado."
            )

    def criar_feedback(self, dados: CreateFeedbackRequest) -> FeedbackResponse:
        data = dados.model_dump()

        identificador_aluno = data.pop("identificador_aluno")

        hash_gerado = HashService.generate_hash(
            identificador_aluno, HashAlgorithm.SHA256
        )

        data["hash_aluno"] = hash_gerado

        new_feedback = Feedback.model_validate(data)

        new_id = self.feedback_repository.insert(new_feedback.model_dump())

        new_feedback.id = new_id

        return FeedbackResponse.model_validate(new_feedback.model_dump())

    def obter_feedbacks(self, skip: int, limit: int) -> list[FeedbackResponse]:
        def iterar_registros():
            for lote in self.feedback_repository.read(batch_size=limit):
                for registro in lote:
                    yield registro

        items = list(islice(iterar_registros(), skip, skip + limit))

        return [FeedbackResponse.model_validate(item) for item in items]

    def obter_feedback_por_id(self, feedback_id: int) -> FeedbackResponse:
        feedback = self.feedback_repository.get_by_id(feedback_id)
        if not feedback:
            raise ResourceNotFoundException(
                f"Feedback com ID {feedback_id} não encontrado."
            )
        return FeedbackResponse.model_validate(feedback)

    def deletar_feedback(self, feedback_id: int) -> None:
        self.validate_feedback_exists(feedback_id)

        self.feedback_repository.delete(feedback_id)

    def atualizar_feedback(self, feedback_id: int, novos_dados: UpdateFeedbackRequest):
        self.validate_feedback_exists(feedback_id)

        self.feedback_repository.update(
            feedback_id, novos_dados.model_dump(exclude_none=True, exclude_unset=True)
        )

    def count_feedbacks(self) -> int:
        return self.feedback_repository.count()

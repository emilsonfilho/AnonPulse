from itertools import islice
from pathlib import Path

from app.api.core.enums import HashAlgorithm
from app.api.routers.feedback import CreateFeedbackRequest, UpdateFeedbackRequest
from app.api.schemas.feedback_schema import FeedbackResponse
from app.database.delta_manager import FeedbackRepository
from app.models.feedback import Feedback
from app.services.hash_service import HashService

table_path = Path("./data/feedback_delta_table")


class FeedbackService:
    def __init__(self):
        self.feedback_repository = FeedbackRepository(table_path.as_posix())

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

    def deletar_feedback(self, feedback_id: int):
        self.feedback_repository.delete(feedback_id)

    def atualizar_feedback(self, feedback_id: int, novos_dados: UpdateFeedbackRequest):
        self.feedback_repository.update(feedback_id, novos_dados.model_dump())

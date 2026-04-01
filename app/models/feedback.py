from pydantic import BaseModel, Field
from api.core.enums import MessageType
from datetime import datetime, timezone


class Feedback(BaseModel):
    id: int = Field(
        default=0
    )  # O Default é necessário para evitar erros de validação, mas será sobrescrito ao criar um novo feedback
    disciplina: str
    nome_monitor: str
    tipo_mensagem: MessageType
    texto_feedback: str
    data_submissao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    hash_aluno: str

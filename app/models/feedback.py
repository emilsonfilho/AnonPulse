from pydantic import BaseModel, Field
from api.core.enums import MessageType
from datetime import datetime, timezone


class Feedback(BaseModel):
    disciplina: str
    nome_monitor: str
    tipo_messagem: MessageType
    texto_feedback: str
    data_submissao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    hash_aluno: str

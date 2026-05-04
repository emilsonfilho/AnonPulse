from datetime import datetime, timezone

from sqlmodel import SQLModel, Field

from app.api.core.enums import MessageType


class Feedback(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    disciplina: str
    nome_monitor: str
    tipo_mensagem: MessageType
    texto_feedback: str
    data_submissao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    hash_aluno: str

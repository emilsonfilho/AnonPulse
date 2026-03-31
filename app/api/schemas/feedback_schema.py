from pydantic import BaseModel, Field
from typing import Annotated
from core.enums import MessageType


class CreateFeedbackRequest(BaseModel):
    disciplina: Annotated[str, Field(min_length=2, max_length=100)]
    nome_monitor: Annotated[str, Field(min_length=2, max_length=100)]
    tipo_messagem: MessageType = Field(default_factory=lambda: MessageType.SUGESTAO)
    texto_feedback: Annotated[str, Field(min_length=2, max_length=100)]
    hash_aluno: Annotated[str, Field(min_length=10, max_length=200)]

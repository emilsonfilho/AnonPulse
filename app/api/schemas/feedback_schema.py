from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from app.api.core.enums import HashAlgorithm, MessageType


class CreateFeedbackRequest(BaseModel):
    disciplina: Annotated[
        str,
        Field(
            min_length=2,
            max_length=100,
            description="Nome da disciplina, deve conter entre 2 e 100 caracteres",
        ),
    ]
    nome_monitor: Annotated[
        str,
        Field(
            min_length=2,
            max_length=100,
            description="Nome do monitor, deve conter entre 2 e 100 caracteres",
        ),
    ]
    tipo_mensagem: MessageType = Field(
        default_factory=lambda: MessageType.SUGESTAO,
        description="Tipo da mensagem, pode ser SUGESTAO, RECLAMACAO ou ELOGIO",
    )
    texto_feedback: Annotated[
        str,
        Field(
            min_length=2,
            max_length=5000,
            description="Texto do feedback, deve conter entre 2 e 5000 caracteres",
        ),
    ]
    identificador_aluno: Annotated[
        str,
        Field(
            min_length=3,
            max_length=100,
            description="Identificador do aluno, como matrícula ou nome",
        ),
    ]


class UpdateFeedbackRequest(BaseModel):
    disciplina: Annotated[str | None, Field(min_length=2, max_length=100)] = None
    nome_monitor: Annotated[str | None, Field(min_length=2, max_length=100)] = None
    tipo_mensagem: MessageType | None = None
    texto_feedback: Annotated[str | None, Field(min_length=2, max_length=100)] = None


class FeedbackResponse(BaseModel):
    id: int
    disciplina: str
    nome_monitor: str
    tipo_mensagem: MessageType
    texto_feedback: str
    data_submissao: datetime
    hash_aluno: str


class HashResponse(BaseModel):
    algoritmo: HashAlgorithm
    hash_aluno: str

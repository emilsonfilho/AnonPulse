from pydantic import BaseModel, Field

from app.core.enums import HashAlgorithm


class HashRequest(BaseModel):
    text: str = Field(
        title="Texto",
        description="Texto para o qual gerar o hash",
        min_length=6,
        max_length=255,
    )


class HashResponse(BaseModel):
    algoritmo: HashAlgorithm
    hash_aluno: str

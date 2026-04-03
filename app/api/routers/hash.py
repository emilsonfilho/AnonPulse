from fastapi import APIRouter, Body
from app.api.core.enums import HashAlgorithm
from app.api.schemas.feedback_schema import HashResponse
from app.services.hash_service import HashService

api_router = APIRouter(prefix="/v1/hash", tags=["Hash"])


@api_router.post(
    path="/{algorithm}",
    response_model=HashResponse,
    name="Gerar Hash",
    description="Recebe um texto e um algoritmo de hash, e retorna o hash correspondente.",
    response_description="Hash gerado com sucesso.",
)
async def generate_hash(
    algorithm: HashAlgorithm,
    text: str = Body(
        title="Texto",
        description="Texto para o qual gerar o hash",
        min_length=6,
        max_length=255,
    ),
) -> HashResponse:
    hash_result = HashService.generate_hash(text, algorithm)
    return HashResponse.model_validate(
        {"algoritmo": algorithm, "hash_aluno": hash_result}
    )

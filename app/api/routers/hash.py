from fastapi import APIRouter
from api.core.enums import HashAlgorithm
from api.schemas.feedback_schema import HashResponse
from services.hash_service import HashService

api_router = APIRouter(prefix="/v1/hash", tags=["Hash"])


@api_router.get(
    path="/",
    response_model=HashResponse,
    name="Gerar Hash",
    description="Recebe um texto e um algoritmo de hash, e retorna o hash correspondente.",
)
async def generate_hash(text: str, algorithm: HashAlgorithm) -> HashResponse:
    hash_result = HashService.generate_hash(text, algorithm)
    return HashResponse.model_validate(
        {"algoritmo": algorithm, "hash_aluno": hash_result}
    )

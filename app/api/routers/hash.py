"""Roteador de API para geração de hashes.

Este módulo expõe uma rota POST para gerar o hash de um texto
usando o algoritmo especificado. A rota segue as convenções
do FastAPI e retorna um HashResponse.
"""

from fastapi import APIRouter

from app.core.enums import HashAlgorithm
from app.schemas.hash_schema import HashRequest, HashResponse
from app.services.hash_service import HashService


api_router = APIRouter(prefix="/v1/hash", tags=["Hash"])


@api_router.post(
    path="/{algorithm}",
    response_model=HashResponse,
    name="Gerar Hash",
    description=(
        "Recebe um texto e um algoritmo de hash, e retorna o hash correspondente."
    ),
    response_description="Hash gerado com sucesso.",
)
async def generate_hash(
    algorithm: HashAlgorithm,
    body: HashRequest,
) -> HashResponse:
    """Gera o hash de um texto usando o algoritmo informado.

    Parameters
    ----------
    algorithm: HashAlgorithm
        Algoritmo de hash a ser utilizado (ex.: SHA256, MD5).
    body: HashRequest
        Objeto contendo o texto a ser hasheado.

    Returns
    -------
    HashResponse
        Objeto com o algoritmo e o hash gerado.
    """

    hash_result = HashService.generate_hash(body.text, algorithm)

    return HashResponse.model_validate(
        {"algoritmo": algorithm, "hash_aluno": hash_result}
    )

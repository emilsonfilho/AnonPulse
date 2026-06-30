from typing import TypeVar, Type
from pydantic import BaseModel, ValidationError

InT = TypeVar("InT")
OutT = TypeVar("OutT", bound=BaseModel)


class Mapper:
    @staticmethod
    def to_response(obj: InT, schema: Type[OutT]) -> OutT:
        """
        Mapeia um objeto de entrada para um esquema de resposta específico (Pydantic).

        Primeiro, tenta realizar a validação direta do objeto utilizando o esquema
        fornecido. Caso ocorra um erro de validação (ValidationError), aplica
        mecanismos de fallback: tenta extrair os dados via `model_dump()`
        (útil para documentos do Beanie ou outros modelos Pydantic) ou através
        do atributo `__dict__` do objeto antes de tentar validar novamente.

        Args:
            - obj (InT): O objeto de entrada contendo os dados a serem mapeados.
            - schema (Type[OutT]): A classe do esquema de saída (Pydantic) desejado.

        Returns:
            OutT: Uma instância do esquema de saída preenchida e validada.

        Raises:
            ValidationError: Se os dados não puderem ser validados no esquema
                fornecido, mesmo após as tentativas de fallback.
        """
        try:
            return schema.model_validate(obj)
        except ValidationError:
            # Fallback: se for um documento/beanie model, tenta validar a partir do dump
            if hasattr(obj, "model_dump"):
                return schema.model_validate(obj.model_dump())
            if hasattr(obj, "__dict__"):
                return schema.model_validate(obj.__dict__)
            raise

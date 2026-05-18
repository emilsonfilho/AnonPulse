from typing import Type, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class Mapper:
    """Mapper para converter objetos de um tipo para outro usando schemas de validação."""
    @staticmethod
    def to_response(obj: T, schema: Type[R]) -> R:
        """Converte um objeto de um tipo para outro usando um schema de validação."""
        return schema.model_validate(obj)

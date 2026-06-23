from typing import TypeVar, Type
from pydantic import BaseModel, ValidationError

InT = TypeVar("InT")
OutT = TypeVar("OutT", bound=BaseModel)


class Mapper:
    @staticmethod
    def to_response(obj: InT, schema: Type[OutT]) -> OutT:
        try:
            return schema.model_validate(obj)
        except ValidationError:
            # Fallback: se for um documento/beanie model, tenta validar a partir do dump
            if hasattr(obj, "model_dump"):
                return schema.model_validate(obj.model_dump())
            if hasattr(obj, "__dict__"):
                return schema.model_validate(obj.__dict__)
            raise
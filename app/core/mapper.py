from typing import TypeVar, Type
from pydantic import BaseModel

InT = TypeVar("InT")
OutT = TypeVar("OutT", bound=BaseModel)

class Mapper:
    @staticmethod
    def to_response(obj: InT, schema: Type[OutT]) -> OutT:
        return schema.model_validate(obj)
from typing import Type, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class Mapper:
    @staticmethod
    def to_response(obj: T, schema: Type[R]) -> R:
        return schema.model_validate(obj)

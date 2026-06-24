from dataclasses import dataclass
from fastapi_pagination import Params


@dataclass
class Pagination:
    skip: int
    limit: int

    @staticmethod
    def from_params(params: Params):
        return Pagination(skip=(params.page - 1) * params.size, limit=params.size)

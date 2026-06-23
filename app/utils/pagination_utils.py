from typing import Callable, TypeVar

from fastapi_pagination import Page, Params

T = TypeVar("T")
R = TypeVar("R")

def map_page(page: Page[T], func: Callable[[T], R]) -> Page[R]:
    params = Params(page=page.page, size=page.size)

    return Page.create(
        items=[func(i) for i in page.items],
        total=page.total,
        params=params,
    )
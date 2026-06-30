from typing import Callable, TypeVar

from fastapi_pagination import Page, Params

T = TypeVar("T")
R = TypeVar("R")


def map_page(page: Page[T], func: Callable[[T], R]) -> Page[R]:
    """
    Aplica uma função de transformação aos itens de uma página e retorna uma nova página.

    Args:
        page (Page[T]): O objeto de página original contendo a lista de itens
            do tipo genérico T e as informações de paginação.
        func (Callable[[T], R]): A função a ser aplicada a cada item da página.
            Deve aceitar um argumento do tipo T e retornar um valor do tipo R.

    Returns:
        Page[R]: Um novo objeto de resposta paginada onde os itens foram
            mapeados e convertidos para o tipo R, mantendo a estrutura
            de paginação intacta.
    """
    params = Params(page=page.page, size=page.size)

    return Page.create(
        items=[func(i) for i in page.items],
        total=page.total,
        params=params,
    )

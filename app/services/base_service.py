from typing import TypeVar, Callable, Awaitable

T = TypeVar("T")

class BaseService:
    async def get_or_raise(
            self, 
            fetcher: Callable[[], Awaitable[T]], 
            exception: type[Exception]
    ) -> T:
        obj = await fetcher()

        if not obj:
            raise exception()
        
        return obj
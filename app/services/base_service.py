class BaseService:
    async def get_or_raise(self, fetcher, exception):
        obj = await fetcher()

        if not obj:
            raise exception()
        
        return obj
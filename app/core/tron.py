from tronpy import AsyncTron
from tronpy.providers.async_http import AsyncHTTPProvider

from app.core.config import settings


async def get_async_tron_client():
    async_provider = AsyncHTTPProvider(
        endpoint_uri="https://api.trongrid.io",
        api_key=settings.trongrid_api_key
    )
    async with AsyncTron(provider=async_provider) as async_client:
        yield async_client

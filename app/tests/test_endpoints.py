import pytest

from httpx import AsyncClient

from app.schemas.tron import AddressWallet
from app.core.config import settings


@pytest.mark.asyncio
async def test_post_wallet(
    async_client: AsyncClient,
    get_auth_header: dict[str, str],
):
    test_wallet = AddressWallet(address=settings.test_wallet)
    response = await async_client.post(
        '/wallet/info',
        headers=get_auth_header,
        json=test_wallet.model_dump())
    data = response.json()
    assert 'trx' in data
    assert 'bandwidth' in data
    assert 'energy' in data

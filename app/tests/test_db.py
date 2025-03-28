import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tron import AddressWallet
from app.database.tron import tron_crud
from app.core.config import settings


@pytest.mark.asyncio
async def test_exists_address(
    async_session: AsyncSession,
):
    test_wallet = AddressWallet(address=settings.test_wallet)
    await tron_crud.add_wallet_address(async_session, test_wallet)
    wallet_db = await tron_crud.get_address(async_session, test_wallet)
    assert test_wallet.address == wallet_db.address

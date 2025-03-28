from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.tron import Wallet
from app.schemas.tron import AddressWallet


class TronCRUD:
    async def add_wallet_address(
        self,
        session: AsyncSession, address_wallet: AddressWallet
    ) -> None:
        new_address = Wallet(**address_wallet.model_dump())
        session.add(new_address)
        await session.commit()

    async def get_all_wallet_address(
            self, session: AsyncSession) -> list[Wallet]:
        db_wallets = await session.execute(
            select(Wallet)
        )
        return db_wallets.scalars().all()

    async def get_address(
        self,
        session: AsyncSession,
        wallet_address: AddressWallet
    ) -> Optional[Wallet]:
        address = await session.execute(
            select(Wallet).where(
                Wallet.address == wallet_address.address
            )
        )
        return address.scalar_one_or_none()


tron_crud = TronCRUD()

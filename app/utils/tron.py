from http import HTTPStatus
from fastapi import HTTPException
from tronpy import AsyncTron

from app.schemas.tron import TrxRead


async def get_data(async_client: AsyncTron, wallet_address: str):
    try:
        balance = await async_client.get_account_balance(
            addr=wallet_address)
        bandwidth = await async_client.get_bandwidth(
            addr=wallet_address
        )
        energy = await async_client.get_account_resource(addr=wallet_address)
        return TrxRead(
            trx=balance,
            bandwidth=bandwidth,
            energy=energy.get('EnergyLimit'))
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={'message': 'Somthing went wrong, please try again!'})

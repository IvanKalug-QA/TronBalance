from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import AsyncTron
from fastapi_pagination import Page
from fastapi_pagination.iterables import paginate

from app.schemas.tron import AddressWallet, TrxRead, AddressReadDB
from app.core.db import get_async_session
from app.core.tron import get_async_tron_client
from app.utils.tron import get_data
from app.database.tron import tron_crud
from app.core.user import current_user

router = APIRouter(tags=['tron'])


@router.post('/wallet/info',
             response_model=TrxRead, dependencies=[Depends(current_user)])
async def get_wallet_info(
    wallet_address: AddressWallet,
    session: AsyncSession = Depends(get_async_session),
    async_client: AsyncTron = Depends(get_async_tron_client)
):
    data = await get_data(async_client, wallet_address.address)
    await tron_crud.add_wallet_address(session, wallet_address)
    return data


@router.get(
    '/get_wallets',

    response_model=Page[AddressReadDB])
async def get_all_address(session: AsyncSession = Depends(get_async_session)):
    data = await tron_crud.get_all_wallet_address(session)
    return paginate(data)

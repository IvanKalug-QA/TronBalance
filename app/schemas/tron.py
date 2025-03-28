from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AddressWallet(BaseModel):
    address: str


class TrxRead(BaseModel):
    trx: float
    bandwidth: int
    energy: int


class AddressReadDB(AddressWallet):
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

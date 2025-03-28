from pydantic import BaseModel, ConfigDict


class AddressWallet(BaseModel):
    address: str


class TrxRead(BaseModel):
    trx: float
    bandwidth: int
    energy: int


class AddressReadDB(AddressWallet):
    model_config = ConfigDict(from_attributes=True)

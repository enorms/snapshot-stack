from pydantic import BaseModel


class CryptoToken(BaseModel):
    address: str
    decimals: int = -1

from pydantic import BaseModel


class StockBase(BaseModel):
    name: str
    symbol: str
    price: float
    quantity: int

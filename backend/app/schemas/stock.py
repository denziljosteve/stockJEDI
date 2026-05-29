from typing import Optional
from pydantic import BaseModel, HttpUrl

class StockBase(BaseModel):
    ticker: str
    name: Optional[str] = None
    source: Optional[str] = None

class StockCreate(StockBase):
    pass

class StockUpdate(StockBase):
    pass

class StockInDBBase(StockBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True

class Stock(StockInDBBase):
    pass

class StockExtractRequest(BaseModel):
    url: HttpUrl

class StockExtractResponse(BaseModel):
    ticker: Optional[str]
    source: str
    is_valid: bool

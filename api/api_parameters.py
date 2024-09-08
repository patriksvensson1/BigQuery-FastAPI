from pydantic import BaseModel
from typing import Optional


class PricesParameters(BaseModel):  # url/something?parameters
    ticker: Optional[str] = None
    date: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    time: Optional[str] = None
    from_time: Optional[str] = None
    to_time: Optional[str] = None


class StocksParameters(BaseModel):  # url/something?parameters
    ticker: Optional[str] = None
    industry: Optional[str] = None
    exchange: Optional[str] = None

from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class PricesParameters(BaseModel):  # url/something?parameters
    name: Optional[str] = None
    ticker: Optional[str] = None
    currency: Optional[str] = None
    at_date: Optional[date] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    at_time: Optional[time] = None
    from_time: Optional[time] = None
    to_time: Optional[time] = None


class StocksParameters(BaseModel):  # url/something?parameters
    ticker: Optional[str] = None
    industry: Optional[str] = None
    exchange: Optional[str] = None

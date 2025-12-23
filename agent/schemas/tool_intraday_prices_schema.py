
from pydantic import BaseModel, Field

from app.data.currencies_validation import ValidCurrency

from typing import Literal

TimeStamp = Literal["1d", "5d", "1wk", "1mo", "3mo", "6mo", "1y"]
Interval = Literal["1m", "2m", "5m", "15m", "30m", "1h"]

class BasePricesSchema(BaseModel):
    """Base schema for intraday prices"""

    currency: ValidCurrency = Field(description="Cryptocurrency name, e.g ('BTC', 'ETH')")
    time_stamp: TimeStamp = Field(description="Time period for cryptocurrency price")
    interval: Interval = Field(description="Interval for cryptocurrency price")

class FetchIntradayPrices(BasePricesSchema):
    """Fetch intraday prices from external API"""

    pass 

class GetIntradayPrices(BasePricesSchema):
    """Get stored prices in database"""

    limit: int = Field(default=20, description="Maximum number of records to return")

from pydantic import BaseModel, Field

from app.data.currencies_validation import ValidCurrency
from typing import Literal

class LongTermPrices(BaseModel):
    currency: ValidCurrency = Field(description="Cryptocurrency name, e.g ('BTC', 'ETH')")
    time_stamp: Literal["DAILY", "WEEKLY", "MONTHLY"] = Field(description="Long time period")

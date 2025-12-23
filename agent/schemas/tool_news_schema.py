from pydantic import BaseModel, Field 

from app.data.currencies_validation import ValidCurrency

class FetchNewsAPI(BaseModel):
    """Fetch news from Alpha Vantage API"""

    currency: ValidCurrency = Field(description="Cryptocurrency name, e.g ('BTC', 'ETH')")

class GetNewsDB(BaseModel):
    """Get news from database"""

    currency: ValidCurrency = Field(description="Cryptocurrency name, e.g ('BTC', 'ETH')")
    limit: int = Field(default=30, description="Maximum number of results to return")

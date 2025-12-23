import httpx

from app.schemas.env_schema import settings
from app.exceptions import ExternalAPIError
from app.utils.logger import get_logger

from typing import Dict

class AlphaVantageClient:
    def __init__(self):
        self.base_url = 'https://www.alphavantage.co/query'
        self.logger = get_logger("main")
        self.api_key = settings.CRYPTO_API_KEY

    async def fetch(self, params: Dict) -> Dict:
        """Generic fetch"""
        params["apikey"] = self.api_key

        try:
            async with httpx.AsyncClient() as client:
                    response = await client.get(self.base_url, params=params)
                    response.raise_for_status()
                    data = response.json()

        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP Error during API call: {str(e)}")
            raise ExternalAPIError("AlphaVantage", f"HTTP {e.response.status_code}")

        except httpx.RequestError as e:
            self.logger.error(f"Network error: {str(e)}")
            raise ExternalAPIError("AlphaVantage", "Network Error")

        return data


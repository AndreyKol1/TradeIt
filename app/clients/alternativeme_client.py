import httpx

from app.utils.logger import get_logger
from app.exceptions import ExternalAPIError

class AlternativeMeClient:
    def __init__(self):
        self.base_url = 'https://api.alternative.me/fng/' 
        self.logger = get_logger("main")

    async def fetch(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url)
                response.raise_for_status()
                data = response.json()

        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP Error during API call: {str(e)}")
            raise ExternalAPIError("AlternativeMe", f"HTTP {e.response.status_code}")

        except httpx.RequestError as e:
            self.logger.error(f"Network error: {str(e)}")
            raise ExternalAPIError("AlternativeMe", "Network Error")

        self.logger.info("Successfully extracted fear and greed index!")
        return data


import httpx

from app.utils.logger import get_logger 
from app.schemas.prices_schema import CryptoPricesDataSchema
from app.schemas.env_schema import settings
from typing import List, Dict


class GetPricesCrypto:
    def __init__(self):
        self.logger = get_logger("main")
        self.crypto_key = settings.CRYPTO_API_KEY

    async def fetch_prices(self, currency: str = "BTC", time_period: str = "DAILY") -> List[CryptoPricesDataSchema]:
        """Fetch prices based on provided crypto currency and time period:
           Possible periods: DAILY, WEEKLY, MONTHLY"""
        currency = currency.upper()
        self._validate_time_period(time_period)
        prices_info_json = await self._get_data(currency, time_period)
        prices = self._extract_price_data(currency, time_period, prices_info_json)
        return prices
        
    async def _get_data(self, currency: str, time_period: str) -> Dict:
        try:
            url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_{time_period}&symbol={currency}&market=USD&apikey={self.crypto_key}'
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

        except httpx.HTTPError as e:
            self.logger.error(f"HTTP error during API call: {str(e)}")
            raise

        except Exception as e:
            self.logger.exception(f"Unexpected error during API call: {str(e)}")
            raise

        self.logger.info("Successfully extracted prices information from API")
        return data

    def _extract_price_data(self, currency: str, time_period: str, data: Dict) -> List[CryptoPricesDataSchema]:
        full_prices_info: List[CryptoPricesDataSchema] = []

        try:
            for date, prices in data[f"Time Series (Digital Currency {time_period.lower().capitalize()})"].items():
                currency_item = CryptoPricesDataSchema(
                        date_price = date,
                        currency = currency,
                        time_period = time_period.upper(),
                        open_price = prices["1. open"],
                        high = prices["2. high"],
                        low = prices["3. low"],
                        close = prices["4. close"],
                        volume = prices["5. volume"]
                )
                full_prices_info.append(currency_item)

        except KeyError as e:
            self.logger.error(f"Missing expected field in API response: {str(e)}")
            raise

        except Exception as e:
            self.logger.exception(f"Unexpected error while parsing data: {str(e)}")
            raise

        self.logger.info(f"""Successfully extracted date, open price, highest price, 
                                lowest price, close price and volume for the {currency}""")

        return full_prices_info

    @staticmethod
    def _validate_time_period(time_period: str):
        available_periods = ["DAILY", "WEEKLY", "MONTHLY"]
        if time_period.upper() not in available_periods:
            raise ValueError(f"Invalid period: {time_period}")

import pandas as pd 
import asyncio

from app.utils.logger import get_logger
from app.schemas.prices_schema import CryptoPricesDataSchema
from app.schemas.intr_prices_valid_schema import YahooRequestSchema
from app.clients.yahoo_finance_client import YahooFinanceClient
from app.exceptions import DataParsingError

from typing import List

class IntraDayPricesService:
    def __init__(self):
        self.logger = get_logger("main")
        self.client = YahooFinanceClient()


    async def fetch_intraday_prices(self, currency: str, time_stamp: str, interval: str):
        """Fetch data for provided currency within user given timestamp"""

        currency = currency.upper()
        YahooRequestSchema(currency=currency, time_stamp=time_stamp, interval=interval) # validate if currency exists. Could be some mismatches

        # run sync yfinance async to align to project structure 
        hist_data = await asyncio.to_thread(self.client.fetch, currency, time_stamp, interval)
        prices = self._extract_data(hist_data, currency, time_stamp, interval)

        return prices

    def _extract_data(self, data_prices: pd.DataFrame, currency: str, time_stamp: str = "1d", interval: str = "1h"):
        """Extract data based on user provided parameters"""

        prices_df = data_prices.reset_index()
        
        price_info: List[CryptoPricesDataSchema] = []

        try:
            for index, row in prices_df.iterrows(): 
                extracted_data = CryptoPricesDataSchema(
                    date_price = row["Datetime"],
                    currency = currency,
                    time_period = time_stamp,
                    interval = interval,
                    open_price = row["Open"],
                    high = row["High"],
                    low = row["Low"],
                    close = row["Close"],
                    volume = row["Volume"],
                    )

                price_info.append(extracted_data)

        except KeyError as e:
            self.logger.error(f"Missing expected field in response: {str(e)}")
            raise DataParsingError(f"Missing field: {str(e)}")

        except Exception as e:
            self.logger.exception(f"Unexpected error while parsing data: {str(e)}")
            raise
            
        self.logger.info(f"""Successfully retrieved information about prices
                         for interval: {interval}, during period: {time_stamp}""")

        return price_info

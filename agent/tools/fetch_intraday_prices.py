import requests

from typing import Literal, Dict
from agent.schemas.tool_intraday_prices_schema import FetchIntradayPrices 
from app.schemas.env_schema import settings 
from app.utils.logger import get_logger

from langchain.tools import tool

logger = get_logger("main")

@tool(args_schema=FetchIntradayPrices)
def fetch_intraday_prices(currency: str,
                      time_stamp: Literal["1d", "5d", "1wk", "1mo", "3mo", "6mo", "1y"],
                      interval: Literal["1m", "2m", "5m", "15m", "30m", "1h"]) -> Dict | str:

    """Fetch fresh intraday prices from external API and store in database

       Use this when price data is missing or stale.

       Args:
        - currency: Name of the cryptocurrency
        - time_stamp: Time period to fetch ("1d", "5d", "1wk", "1mo", "3mo", "6mo", "1y"),
        - interval: Price interval ("1m", "2m", "5m", "15m", "30m", "1h")

       Returns:
         Dict: A dict of intradayPrices objects with date, currency, time period, interval, 
                open price, highest price, lowest price, close_price, volume.

        """
    logger.info(f"Fetching intraday prices for {currency}: ({time_stamp}, {interval})")

    url = f"{settings.API_BASE_URL}/get_intraday_prices"
    params = {
        "currency": currency,
        "time_stamp": time_stamp,
        "interval": interval
    }
    try:
        response = requests.post(url, params=params, timeout=20)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        logger.error(f"Timeout fetching prices for {currency}")
        return f"Request timed out. The API may be slow or unavailable"

    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error for fetching prices for {currency}")
        return f"Could not connect to API endpoint. Check network connection."

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        logger.error (f"HTTP {status} for fetching prices for {currency}: {str(e)}")

        if status == 400:
            return f"Currency {currency} not found"

        elif status == 422:
            return f"Invalid parameters passed"

        elif status >= 502:
            return f"Yahoo Finance failed to get data"

        return f"API Error (HTTP {status}) fetching prices for currency {currency}"

    except Exception as e:
        logger.exception(f"Unexpected error happened while fetching prices for {currency}")
        return f"Unexpected error occurred while fetching prices"



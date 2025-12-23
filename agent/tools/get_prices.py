import psycopg

from psycopg.rows import dict_row
from app.database.config import CONN_STRING 
from typing import List, Dict

from agent.schemas.tool_intraday_prices_schema import GetIntradayPrices
from app.utils.logger import get_logger

from langchain.tools import tool

logger = get_logger("main")

@tool(args_schema=GetIntradayPrices)

def get_prices(currency: str, time_stamp: str, interval: str, limit: int = 50) -> List[Dict]:
    """Query historical cryptocurrency prices from database.

    Use this when you need to get information about prices at specific time stamp with specific
    interval range. Use this when you need to conduct a deeper analysis on user provided cryptocurrency.

    Args:
        currency: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
        time_stamp: Time period for the data (e.g., '1d', '5d', '1mo')
        interval: Price interval (e.g., '1h', '15m', '1d')
        limit: Maximum number of records to return

    Returns:
        List of price records, each containing:
            - id: Record ID
            - timestamp: DateTime of the price point
            - currency: Cryptocurrency symbol
            - time_period: Requested time period
            - interval: Price interval
            - open: Opening price
            - high: Highest price
            - low: Lowest price
            - close: Closing price
            - volume: Trading volume
            - fetched_at: When the data was fetched
    """
    try:

        with psycopg.connect(CONN_STRING, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT *
                    FROM crypto_prices
                    WHERE currency = %s
                        AND time_period = %s
                        AND interval = %s
                    ORDER BY fetched_at DESC
                    LIMIT %s
                    """,
                    (currency, time_stamp, interval, limit))

                rows = cur.fetchall()

                return rows

    except ConnectionError:
        logger.critical("Unable to connect to database!")
        raise DataBaseConnectionError("Service unavailable")

    except Exception as e:
        logger.error(f"Unexpected database error: {str(e)}")
        raise


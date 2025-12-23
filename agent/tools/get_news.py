import psycopg
from psycopg.rows import dict_row
from app.database.config import CONN_STRING 
from langchain.tools import tool
from typing import List, Dict
from app.utils.logger import get_logger

from agent.schemas.tool_news_schema import GetNewsDB 

logger = get_logger("main")

@tool(args_schema=GetNewsDB)
def get_news(currency: str, limit) -> List[Dict]:
    """Query historical cryptocurrency news from database.

       Use this tool when news are outdated or there is lack of news.

       Args:
            - currency: Name of the cryptocurrency.
            - limit: Maximum number of records to get.

       Returns:
       List of news records, each containing:
            - id: Record ID
            - title: Title of the article
            - summary: Short summary of the article
            - publish_time: When the article was published
            - currency: Cryptocurrency symbol
            - relevance_score: How relevant the news is to provided cryptocurrency
            - ticker_sentiment: Sentiment score of the news
            - fetched_at: When the data was fetched
    """

    try:
        with psycopg.connect(CONN_STRING, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT *
                    FROM crypto_news
                    WHERE currency = %s
                    ORDER BY fetched_at DESC
                    LIMIT %s
                    """,
                    (currency, limit))

                rows = cur.fetchall()

                return rows

    except ConnectionError:
        logger.critical("Unable to connect to database!")
        raise DataBaseConnectionError("Service unavailable")

    except Exception as e:
        logger.error(f"Unexpected database error: {str(e)}")
        raise


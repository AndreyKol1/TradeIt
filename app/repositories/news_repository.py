from typing import List 

from app.schemas.news_schema import CryptoNewsDataSchema


async def insert_news(conn, news: List[CryptoNewsDataSchema]):
    async with conn.cursor() as cursor:
        for doc in news:
            await cursor.execute("""INSERT INTO crypto_news
                                    (title, summary, publish_time, currency, relevance_score, ticker_sentiment)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                    ON CONFLICT (currency, title, publish_time) DO NOTHING""",
                                    
                                    (doc.title, doc.summary, doc.date_published,
                                     doc.currency, doc.relevance_score, doc.ticker_sentiment_score))

        await conn.commit()




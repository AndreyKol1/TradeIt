from fastapi import APIRouter, Depends

from app.dependencies import get_conn
from app.dependencies import get_news_fetcher
from app.repositories.news_repository import insert_news

router = APIRouter()

@router.post("/get_news")
async def add_news(currency: str, conn=Depends(get_conn)):
    news_class_cached = get_news_fetcher()
    news = await news_class_cached.fetch_news(currency)

    await insert_news(conn, news)
    
    return {"message": "Values successfully written to the database"}

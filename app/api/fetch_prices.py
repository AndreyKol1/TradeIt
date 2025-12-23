from app.repositories.prices_repository import insert_prices
from fastapi import APIRouter, Depends

from app.dependencies import get_conn
from app.dependencies import get_price_fetcher

from typing import Dict

router = APIRouter()

@router.post("/get_prices")
async def add_prices(currency: str, period: str = "DAILY", conn=Depends(get_conn)) -> Dict:
    price_class_cached = get_price_fetcher()
    prices = await price_class_cached.fetch_prices(currency, period)

    await insert_prices(conn, prices)

    return {"message": f"Successfully fetched prices for {currency}!"}

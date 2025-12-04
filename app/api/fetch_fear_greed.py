from fastapi import APIRouter, Depends

from app.dependencies import get_conn, get_fear_greed_fetcher
from app.repositories.fear_greed_idx_repository import insert_fear_greed_index

from typing import Dict

router = APIRouter()

@router.post("/get_fear_greed_index")
async def add_index(conn=Depends(get_conn)) -> Dict:
    fear_greed_class_cached = get_fear_greed_fetcher()
    results = await fear_greed_class_cached.fetch_fear_greed_index()

    await insert_fear_greed_index(conn, results)

    return {"message": "Successfully inserted fear and greed index to the database"}




from app.schemas.fear_greed_idx_schema import FearGreedIndexSchema

async def insert_fear_greed_index(conn, idx_info: FearGreedIndexSchema) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute("""INSERT INTO fear_greed_index
                                (classification, value, time_stamp)

                                VALUES (%s, %s, %s)
                                ON CONFLICT (time_stamp) DO NOTHING
                                """,
                             (idx_info.classification, idx_info.value, idx_info.time_stamp))

        await conn.commit()
                             
        

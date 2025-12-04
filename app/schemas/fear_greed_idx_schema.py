from pydantic import BaseModel 
from datetime import date 

class FearGreedIndexSchema(BaseModel):
    classification: str 
    value: int 
    time_stamp: date 

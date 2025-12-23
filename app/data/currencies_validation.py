import csv 

from functools import lru_cache
from typing import Annotated

from pydantic import BeforeValidator

@lru_cache
def get_valid_currency():
        with open("app/data/cryptocurrency_list.csv", newline="") as f:
            reader = csv.DictReader(f)
            vals = {row["from_currency"].upper() for row in reader}
            return vals

def validate_currency(v):
        v = v.upper()
        vals = get_valid_currency()
        if v not in vals:
            raise ValueError(f"Invalid crypto name: {v}. Should be like not 'Bitcoin' but 'BTC'!")

        return v

ValidCurrency = Annotated[str, BeforeValidator(validate_currency)]

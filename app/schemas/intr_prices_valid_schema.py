from pydantic import BaseModel, field_validator

from app.data.currencies_validation import get_valid_currency 

ALLOWED_PERIODS = {
    "1d", "5d", "1mo", "3mo", "6mo",
    "1y", "2y", "5y", "10y", "ytd", "max"
}

ALLOWED_INTERVALS = {
    "1m", "2m", "5m", "15m", "30m",
    "60m", "90m", "1h",
    "1d", "5d", "1wk", "1mo", "3mo"
}

class YahooRequestSchema(BaseModel):
    currency: str 
    time_stamp: str 
    interval: str 

    @field_validator("time_stamp")
    @classmethod 
    def validate_time_stamp(cls, v):
        if v not in ALLOWED_PERIODS:
            raise ValueError(f"""Invalid time_stamp provided: {v}.
                                Allowed: {ALLOWED_PERIODS}""")

        return v

    @field_validator("interval")
    @classmethod 
    def validate_interval(cls, v):
        if v not in ALLOWED_INTERVALS:
            raise ValueError(f"""Invalid time_stamp provided: {v}.
                                Allowed: {ALLOWED_INTERVALS}""")

        return v

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v):
        vals = get_valid_currency()
        if v not in vals:
            raise ValueError(f"Invalid crypto name: {v}")

        return v

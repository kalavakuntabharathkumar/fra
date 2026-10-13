from pydantic import BaseModel, Field, ConfigDict

class Transaction(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    transaction_id: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0, le=1_000_000)
    merchant_category: str = Field(min_length=1, max_length=60)
    country: str = Field(min_length=2, max_length=2)
    account_age_days: int = Field(ge=0, le=100_000)
    transactions_last_hour: int = Field(ge=0, le=10_000)

class ScoreResponse(BaseModel):
    transaction_id: str
    fraud_probability: float
    decision: str
    model_version: str
    cached: bool = False

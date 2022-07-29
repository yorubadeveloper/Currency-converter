from typing import Dict
from pydantic import BaseModel


class SupportedCurrencies(BaseModel):
    currencies: Dict[str, str]

    class Config:
        schema_extra = {
            "example": {
                "currency": {
                    "CAD": "Canadian Dollar",
                    "EUR": "Euro",
                    "NGN": "Nigerian Naira",
                    "USD": "United States Dollar",

                }
            }
        }


class ConvertCurrencies(BaseModel):
    base: str
    to: str
    amount: float
    exchange_rate: float
    result: float

    class Config:
        schema_extra = {
            "example": {
                "base": "EUR",
                "to": "USD",
                "amount": 15.5,
                "exchange_rate": 1.164428,
                "result": 18.048634,
            }
        }

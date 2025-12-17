from decimal import Decimal
from enum import StrEnum
from pydantic import BaseModel


class Currency(StrEnum):
    BRL = "BRL"
    USD = "USD"


class MonetaryValue(BaseModel):
    amount: Decimal
    currency: Currency
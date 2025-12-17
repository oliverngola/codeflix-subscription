from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field


class ValueObject(BaseModel):
    model_config = {
        "frozen": True,
    }


class Currency(StrEnum):
    BRL = "BRL"
    USD = "USD"


class MonetaryValue(ValueObject):
    amount: Decimal = Field(gt=0)
    currency: Currency = Currency.BRL
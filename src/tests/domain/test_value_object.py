import pytest
from pydantic import ValidationError

from src.domain.value_objects import MonetaryValue, Currency


def test_equals_compare_attributes():
    mv1 = MonetaryValue(amount=100, currency=Currency.USD)
    mv2 = MonetaryValue(amount=100, currency=Currency.USD)

    assert mv1 == mv2


def test_not_equals_compare_attributes():
    mv1 = MonetaryValue(amount=100, currency=Currency.USD)
    mv2 = MonetaryValue(amount=200, currency=Currency.USD)

    assert mv1 != mv2


def test_cannot_mutate_attributes():
    mv = MonetaryValue(amount=100, currency=Currency.USD)

    with pytest.raises(ValidationError, match=r"Instance is frozen"):
        mv.amount = 200
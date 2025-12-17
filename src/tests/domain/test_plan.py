from src.domain.plan import Plan
from src.domain.value_objects import MonetaryValue, Currency


def test_create_plan_with_name_and_price():
    plan = Plan(name="Basic", price=MonetaryValue(amount=100, currency=Currency.BRL))
    assert plan.id is not None
    assert plan.name == "Basic"
    assert plan.price == MonetaryValue(amount=100, currency=Currency.BRL)


def test_raise_error_for_invalid_price():
    try:
        plan = Plan(name="Basic", price=MonetaryValue(amount=100, currency="ABC"))
    except ValueError as e:
        assert "Input should be 'BRL' or 'USD'" in str(e)
    else:
        assert False
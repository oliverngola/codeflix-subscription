import pytest

from src.application.create_plan import CreatePlanUseCase, CreatePlanInput
from src.application.exceptions import DuplicatePlanError
from src.domain.plan import Plan
from src.domain.value_objects import MonetaryValue
from src.tests.fixtures.infra.repositories import InMemoryPlanRepository


class TestCreatePlan:
    def test_when_plan_with_name_exists_then_return_error(self):
        basic_plan = Plan(name="Basic", price=MonetaryValue(amount=100, currency="BRL"))
        repo = InMemoryPlanRepository()
        repo.save(basic_plan)

        create_plan = CreatePlanUseCase(repository=repo)

        with pytest.raises(DuplicatePlanError):
            create_plan.execute(CreatePlanInput(
                name="Basic",
                price=MonetaryValue(amount=100, currency="BRL")
            ))

    def test_create_plan(self):
        repo = InMemoryPlanRepository()
        create_plan = CreatePlanUseCase(repository=repo)

        output = create_plan.execute(CreatePlanInput(
            name="Basic",
            price=MonetaryValue(amount=100, currency="BRL")
        ))

        assert repo.find_by_name("Basic") is not None

        assert output.id is not None
        assert output.name == "Basic"
        assert output.price == MonetaryValue(amount=100, currency="BRL")
from uuid import UUID

from pydantic import BaseModel

from src.application.exceptions import DuplicatePlanError
from src.domain.plan import Plan
from src.domain.value_objects import MonetaryValue


class CreatePlanInput(BaseModel):
    name: str
    price: MonetaryValue


class CreatePlanOutput(BaseModel):
    id: UUID
    name: str
    price: MonetaryValue


class CreatePlanUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, input: CreatePlanInput) -> CreatePlanOutput:
        existing_plan = self.repository.find_by_name(input.name)
        if existing_plan:
            raise DuplicatePlanError()

        plan = Plan(name=input.name, price=input.price)
        self.repository.save(plan)

        return CreatePlanOutput(
            id=plan.id,
            name=plan.name,
            price=plan.price,
        )
from uuid import UUID

from src.domain.plan import Plan
from src.domain.repositories import PlanRepository


class InMemoryPlanRepository(PlanRepository):
    def __init__(self, plans: list[Plan] = None) -> None:
        self.plans = plans or []

    def find_by_name(self, name: str) -> Plan | None:
        for plan in self.plans:
            if plan.name == name:
                return plan
        return None

    def find_by_id(self, plan_id: UUID) -> Plan | None:
        for plan in self.plans:
            if plan.id == plan_id:
                return plan
        return

    def save(self, plan: Plan) -> None:
        if self.find_by_name(plan.name):
            return None

        self.plans.append(plan)
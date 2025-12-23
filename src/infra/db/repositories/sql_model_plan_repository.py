from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from src.domain.plan import Plan
from src.domain.repositories import (
    PlanRepository,
)
from src.infra.db.models.plan_model import PlanModel


class SQLModelPlanRepository(PlanRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_name(self, name: str) -> Optional[Plan]:
        statement = select(PlanModel).where(PlanModel.name == name)
        result = self.session.exec(statement).first()
        return PlanModel.to_entity(result) if result else None

    def find_by_id(self, plan_id: UUID) -> Optional[Plan]:
        statement = select(PlanModel).where(PlanModel.id == plan_id)
        result = self.session.exec(statement).first()
        return PlanModel.to_entity(result) if result else None

    def save(self, plan: Plan) -> None:
        model = PlanModel.from_entity(plan)
        self.session.add(model)
        self.session.commit()

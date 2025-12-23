from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlmodel import Field, SQLModel

from src.domain.plan import Plan
from src.domain.value_objects import Currency, MonetaryValue


class PlanModel(SQLModel, table=True):
    __tablename__ = "plans"

    id: UUID = Field(primary_key=True)
    name: str = Field(index=True, unique=True)
    price_amount: Decimal = Field()
    price_currency: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)

    @classmethod
    def from_entity(cls, plan: Plan) -> "PlanModel":
        return cls(
            id=plan.id,
            name=plan.name,
            price_amount=plan.price.amount,
            price_currency=plan.price.currency,
            created_at=plan.created_at,
            updated_at=plan.updated_at,
            is_active=plan.is_active,
        )

    @classmethod
    def to_entity(cls, plan_model: "PlanModel") -> Plan:
        return Plan(
            id=plan_model.id,
            name=plan_model.name,
            price=MonetaryValue(
                amount=plan_model.price_amount,
                currency=Currency(plan_model.price_currency),
            ),
            created_at=plan_model.created_at,
            updated_at=plan_model.updated_at,
            is_active=plan_model.is_active,
        )

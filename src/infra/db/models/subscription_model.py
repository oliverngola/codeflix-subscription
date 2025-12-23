from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel

from src.domain.subscription import Subscription, SubscriptionStatus


class SubscriptionModel(SQLModel, table=True):
    __tablename__ = "subscriptions"

    id: UUID = Field(primary_key=True)
    user_id: UUID = Field(foreign_key="user_accounts.id", index=True)
    plan_id: UUID = Field(foreign_key="plans.id", index=True)
    start_date: datetime
    end_date: datetime
    is_trial: bool = Field(default=False)
    status: str = Field(default=SubscriptionStatus.ACTIVE)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def from_entity(cls, subscription: Subscription) -> "SubscriptionModel":
        return cls(
            id=subscription.id,
            user_id=subscription.user_id,
            plan_id=subscription.plan_id,
            start_date=subscription.start_date,
            end_date=subscription.end_date,
            status=subscription.status,
            is_trial=subscription.is_trial,
            created_at=subscription.created_at,
            updated_at=subscription.updated_at,
        )

    def to_entity(self) -> Subscription:
        return Subscription(
            id=self.id,
            user_id=self.user_id,
            plan_id=self.plan_id,
            start_date=self.start_date,
            end_date=self.end_date,
            status=SubscriptionStatus(self.status),
            is_trial=self.is_trial,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

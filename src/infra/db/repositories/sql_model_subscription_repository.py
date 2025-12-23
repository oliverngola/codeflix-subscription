from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from src.domain.repositories import SubscriptionRepository
from src.domain.subscription import Subscription
from src.infra.db.models.subscription_model import SubscriptionModel


class SQLModelSubscriptionRepository(SubscriptionRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, subscription_id: UUID) -> Optional[Subscription]:
        statement = select(SubscriptionModel).where(
            SubscriptionModel.id == subscription_id
        )
        result = self.session.exec(statement).first()
        return result.to_entity() if result else None

    def find_by_user_id(self, user_id: UUID) -> Optional[Subscription]:
        statement = select(SubscriptionModel).where(
            SubscriptionModel.user_id == user_id
        )
        result = self.session.exec(statement).first()
        return result.to_entity() if result else None

    def save(self, subscription: Subscription) -> None:
        subscription.updated_at = datetime.now()
        model = SubscriptionModel.from_entity(subscription)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

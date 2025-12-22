from uuid import UUID

from pydantic import BaseModel

from src.application.exceptions import SubscriptionNotFoundError
from src.domain.repositories import SubscriptionRepository


class CancelSubscriptionInput(BaseModel):
    subscription_id: UUID


class CancelSubscriptionUseCase:
    def __init__(self, repository: SubscriptionRepository):
        self.repo = repository

    def execute(self, input: CancelSubscriptionInput) -> None:
        subscription = self.repo.find_by_id(input.subscription_id)
        if not subscription:
            raise SubscriptionNotFoundError(f"Subscription with ID {input.subscription_id} not found")

        subscription.cancel()
        self.repo.save(subscription)
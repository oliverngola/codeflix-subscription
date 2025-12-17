from uuid import UUID

from pydantic import BaseModel

from src.application.exceptions import SubscriptionNotFoundError


class CancelSubscriptionInput(BaseModel):
    subscription_id: UUID


class CancelSubscriptionUseCase:
    def __init__(self, repository):
        self.repo = repository

    def execute(self, input: CancelSubscriptionInput) -> None:
        subscription = self.repo.get_by_id(input.subcription_id)
        if not subscription:
            raise SubscriptionNotFoundError("...")

        subscription.cancel()
        self.repo.save(subscription)
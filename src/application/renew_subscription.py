from uuid import UUID
import logging

from pydantic import BaseModel


logger = logging.getLogger(__name__)


class RenewSubscriptionInput(BaseModel):
    subscription_id: UUID
    payment_token: str


class RenewSubscriptionUseCase:
    def __init__(self, subscription_repository, payment_gateway, user_account_repository, notification_service):
        self._subscription_repository = subscription_repository
        self._payment_gateway = payment_gateway
        self._user_account_repository = user_account_repository
        self._notification_service = notification_service

    def execute(self, input: RenewSubscriptionInput) -> None:
        subscription = self._subscription_repository.find_by_id(input.subscription_id)
        if not subscription:
            logger.error(f"Subscription with id {input.subscription_id} not found")
            return None

        user_account = self._user_account_repository.find_by_id(subscription.user_id)

        payment_result = self._payment_gateway.process_payment(
            payment_token=input.payment_token,
            billing_address=user_account.billing_address,
        )

        if payment_result.success:
            subscription.renew()
        else:
            self._notification_service.notify(f"Payment failed for subscription {input.subscription_id}")
            if subscription.is_trial:
                subscription.cancel()
            else:
                subscription.convert_to_trial()
        self._subscription_repository.save(subscription)
"""
Subscribe to Plan:
Input: user, plan, payment info (token)
Output: subscription id
Side effects:
- Charge customer
- Notify if failure
- Create a subscription
"""

from uuid import UUID

from pydantic import BaseModel

from src.application.exceptions import PlanNotFoundError, SubscriptionConflictError, UserNotFoundError
from src.domain.repositories import (
    PlanRepository, 
    SubscriptionRepository, 
    UserAccountRepository
)
from src.domain.subscription import Subscription
from src.infra.notification import NotificationService
from src.infra.payment import PaymentGateway


class SubscribeToPlanInput(BaseModel):
    user_id: UUID
    plan_id: UUID
    payment_token: str


class SubscribeToPlanOutput(BaseModel):
    subscription_id: UUID


class SubscribeToPlanUseCase:
    def __init__(
        self,
        payment_gateway: PaymentGateway,
        notification_service: NotificationService,
        subscription_repository: SubscriptionRepository,
        user_account_repository: UserAccountRepository,
        plan_repository: PlanRepository,
    ):
        self.payment_gateway = payment_gateway
        self.notification_service = notification_service
        self.subscription_repository = subscription_repository
        self.user_account_repository = user_account_repository
        self.plan_repository = plan_repository

    def execute(self, input: SubscribeToPlanInput) -> SubscribeToPlanOutput:
        user = self.user_account_repository.find_by_id(input.user_id)
        if not user:
            raise UserNotFoundError(input.user_id)

        if not self.plan_repository.find_by_id(input.plan_id):
            raise PlanNotFoundError(input.plan_id)

        subscription = self.subscription_repository.find_by_user_id(input.user_id)
        if subscription and subscription.is_active:
            raise SubscriptionConflictError("User already has active subscription")

        payment = self.payment_gateway.process_payment(
            payment_token=input.payment_token,
            billing_address=user.billing_address,
        )
        if payment.success:
            subscription = Subscription.create_regular(
                user_id=input.user_id, plan_id=input.plan_id
            )
        else:
            self.notification_service.notify("Payment failed")
            subscription = Subscription.create_trial(
                user_id=input.user_id, plan_id=input.plan_id
            )

        self.subscription_repository.save(subscription)
        return SubscribeToPlanOutput(subscription_id=subscription.id)
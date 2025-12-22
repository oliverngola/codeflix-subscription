from decimal import Decimal
from uuid import uuid4

import pytest

from src.application.cancel_subscription import (
    CancelSubscriptionUseCase,
    CancelSubscriptionInput,
)
from src.domain.plan import Plan
from src.domain.subscription import Subscription
from src.domain.user_account import UserAccount, Address
from src.domain.value_objects import MonetaryValue
from src.tests.fixtures.infra.repositories import InMemorySubscriptionRepository


@pytest.fixture
def user_account():
    return UserAccount(
        iam_user_id="123456789012",
        name="test-user",
        email="test@user.com",
        billing_address=Address(
            street="123 Main St",
            city="Anytown",
            state="NY",
            zip_code="12345",
            country="BRL",
        ),
    )


@pytest.fixture
def basic_plan():
    return Plan(
        name="Basic", price=MonetaryValue(amount=Decimal("49.90"), currency="BRL")
    )


@pytest.fixture
def active_subscription(user_account, basic_plan):
    return Subscription.create_regular(
        user_id=user_account.id,
        plan_id=basic_plan.id,
    )


class TestCancelSubscription:
    def test_when_subscription_exists_then_cancel_it(
        self, user_account, active_subscription
    ):
        # Arrange
        subscription_repo = InMemorySubscriptionRepository([active_subscription])
        use_case = CancelSubscriptionUseCase(repository=subscription_repo)
        input_data = CancelSubscriptionInput(subscription_id=active_subscription.id)
        assert active_subscription.is_active

        # Act
        use_case.execute(input_data)

        # Assert
        assert active_subscription.is_canceled

    def test_when_subscription_does_not_exist_then_return_error(self):
        # Arrange
        subscription_repo = InMemorySubscriptionRepository([])
        use_case = CancelSubscriptionUseCase(repository=subscription_repo)
        input_data = CancelSubscriptionInput(subscription_id=uuid4())

        # Act/Assert
        with pytest.raises(Exception) as exc_info:
            use_case.execute(input_data)

        assert "not found" in str(exc_info.value)

    def test_when_subscription_already_canceled_then_remains_canceled(
        self, user_account, active_subscription
    ):
        # Arrange
        subscription_repo = InMemorySubscriptionRepository([active_subscription])
        use_case = CancelSubscriptionUseCase(repository=subscription_repo)
        input_data = CancelSubscriptionInput(subscription_id=active_subscription.id)
        active_subscription.cancel()
        assert active_subscription.is_canceled

        # Act
        use_case.execute(input_data)

        # Assert
        assert active_subscription.is_canceled
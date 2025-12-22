from datetime import date
from decimal import Decimal
from unittest.mock import create_autospec, Mock

import pytest
from dateutil.relativedelta import relativedelta

from src.application.renew_subscription import RenewSubscriptionUseCase, RenewSubscriptionInput
from src.domain.plan import Plan
from src.domain.subscription import Subscription
from src.domain.user_account import UserAccount, Address
from src.domain.value_objects import MonetaryValue
from src.infra.payment_gateway import PaymentGateway, Payment
from src.tests.infra.in_memory_subscription_repository import InMemorySubscriptionRepository
from src.tests.infra.in_memory_user_account_repository import InMemoryUserAccountRepository
from uuid import uuid4


@pytest.fixture
def user_account():
    return UserAccount(
        iam_user_id='123456789012',
        name='test-user',
        email='test@user.com',
        billing_address=Address(
            street='123 Main St',
            city='Anytown',
            state='NY',
            zip_code='12345',
            country='BRL'
        )
    )


@pytest.fixture
def basic_plan():
    return Plan(
        name="Basic",
        price=MonetaryValue(amount=Decimal("49.90"), currency="BRL")
    )


@pytest.fixture
def regular_subscription(user_account, basic_plan):
    return Subscription.create_regular(
        user_id=user_account.id,
        plan_id=basic_plan.id,
    )


@pytest.fixture
def trial_subscription(user_account, basic_plan):
    return Subscription.create_trial(
        user_id=user_account.id,
        plan_id=basic_plan.id,
    )


class TestRenewSubscription:
    def test_when_payment_succeeds_then_renew_subscription(
        self,
        user_account,
        regular_subscription,
    ):
        account_repo = InMemoryUserAccountRepository([user_account])
        subscription_repo = InMemorySubscriptionRepository([regular_subscription])
        payment_gateway = create_autospec(PaymentGateway)
        payment_gateway.process_payment.return_value = Payment(success=True)

        use_case = RenewSubscriptionUseCase(
            subscription_repository=subscription_repo,
            payment_gateway=payment_gateway,
            user_account_repository=account_repo,
            notification_service=None,
        )
        input = RenewSubscriptionInput(
            subscription_id=regular_subscription.id,
            payment_token="payment_token123"
        )

        previous_end_date = regular_subscription.end_date
        use_case.execute(input)
        new_end_date = regular_subscription.end_date

        assert new_end_date == previous_end_date + relativedelta(days=30)
        payment_gateway.process_payment.assert_called_once_with(
            payment_token="payment_token123",
            billing_address=user_account.billing_address,
        )

    def test_when_payment_succeeds_and_subscription_is_trial_then_upgrade_it(
        self,
        user_account,
        trial_subscription,
    ):
        account_repo = InMemoryUserAccountRepository([user_account])
        subscription_repo = InMemorySubscriptionRepository([trial_subscription])
        payment_gateway = create_autospec(PaymentGateway)
        payment_gateway.process_payment.return_value = Payment(success=True)

        use_case = RenewSubscriptionUseCase(
            subscription_repository=subscription_repo,
            payment_gateway=payment_gateway,
            user_account_repository=account_repo,
            notification_service=None,
        )
        input = RenewSubscriptionInput(
            subscription_id=trial_subscription.id,
            payment_token="payment_token123"
        )

        use_case.execute(input)

        assert trial_subscription.is_trial is False
        assert trial_subscription.start_date.date() == date.today()
        assert trial_subscription.end_date.date() == date.today() + relativedelta(days=30)
        payment_gateway.process_payment.assert_called_once_with(
            payment_token="payment_token123",
            billing_address=user_account.billing_address,
        )

    def test_when_payment_fails_then_notify_and_convert_to_trial_subscription(
        self,
        user_account,
        regular_subscription,
    ):
        account_repo = InMemoryUserAccountRepository([user_account])
        subscription_repo = InMemorySubscriptionRepository([regular_subscription])
        payment_gateway = create_autospec(PaymentGateway)
        payment_gateway.process_payment.return_value = Payment(success=False)
        notification_service = Mock()

        use_case = RenewSubscriptionUseCase(
            subscription_repository=subscription_repo,
            payment_gateway=payment_gateway,
            user_account_repository=account_repo,
            notification_service=notification_service,
        )
        input = RenewSubscriptionInput(
            subscription_id=regular_subscription.id,
            payment_token="payment_token123"
        )

        use_case.execute(input)

        assert regular_subscription.is_trial is True
        notification_service.notify.assert_called_once_with(
            f"Payment failed for subscription {regular_subscription.id}"
        )

    def test_when_payment_fails_and_subscription_is_trial_then_cancel_it(
        self,
        user_account,
        trial_subscription,
    ):
        account_repo = InMemoryUserAccountRepository([user_account])
        subscription_repo = InMemorySubscriptionRepository([trial_subscription])
        payment_gateway = create_autospec(PaymentGateway)
        payment_gateway.process_payment.return_value = Payment(success=False)
        notification_service = Mock()

        use_case = RenewSubscriptionUseCase(
            subscription_repository=subscription_repo,
            payment_gateway=payment_gateway,
            user_account_repository=account_repo,
            notification_service=notification_service,
        )
        input = RenewSubscriptionInput(
            subscription_id=trial_subscription.id,
            payment_token="payment_token123"
        )

        use_case.execute(input)

        assert trial_subscription.is_canceled is True
        notification_service.notify.assert_called_once_with(
            f"Payment failed for subscription {trial_subscription.id}"
        )

    def test_when_subscription_does_not_exist_then_log_error(
        self,
        user_account,
    ):
        account_repo = InMemoryUserAccountRepository([user_account])
        subscription_repo = InMemorySubscriptionRepository([])
        payment_gateway = create_autospec(PaymentGateway)
        notification_service = create_autospec(spec=['notify'])

        use_case = RenewSubscriptionUseCase(
            subscription_repository=subscription_repo,
            payment_gateway=payment_gateway,
            user_account_repository=account_repo,
            notification_service=notification_service,
        )
        non_existent_id = uuid4()
        input = RenewSubscriptionInput(
            subscription_id=non_existent_id,
            payment_token="payment_token123"
        )

        result = use_case.execute(input)

        assert result is None
        payment_gateway.process_payment.assert_not_called()
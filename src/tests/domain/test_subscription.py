from datetime import datetime, date
from uuid import uuid4

from dateutil.relativedelta import relativedelta

from src.domain.subscription import Subscription


class TestCreateRegularSubscription:
    def test_create_regular_subscription_with_30_days_duration(self):
        user_id = uuid4()
        plan_id = uuid4()
        subscription = Subscription.create_regular(user_id, plan_id)

        assert subscription.id is not None
        assert subscription.start_date is not None
        assert (subscription.end_date - subscription.start_date).days == 30
        assert subscription.is_trial is False
        assert subscription.is_active is True


class TestCreateTrialSubscription:
    def test_create_trial_subscription_with_7_days_trial(self):
        user_id = uuid4()
        plan_id = uuid4()
        subscription = Subscription.create_trial(user_id, plan_id)

        assert subscription.id is not None
        assert subscription.start_date is not None
        assert (subscription.end_date - subscription.start_date).days == 7
        assert subscription.is_trial is True
        assert subscription.is_active is True


class TestIsExpired:
    def test_end_date_before_today_then_expired_subscription(self):
        user_id = uuid4()
        plan_id = uuid4()
        subscription = Subscription.create_regular(user_id, plan_id)
        subscription.end_date = datetime.today() - relativedelta(days=1)
        assert subscription.is_expired is True

    def test_end_date_after_today_then_not_expired_subscription(self):
        user_id = uuid4()
        plan_id = uuid4()
        subscription = Subscription.create_regular(user_id, plan_id)
        subscription.end_date = datetime.today() + relativedelta(days=1)
        assert subscription.is_expired is False

    def test_end_date_on_today_then_not_expired_subscription(self):
        user_id = uuid4()
        plan_id = uuid4()
        subscription = Subscription.create_regular(user_id, plan_id)
        subscription.end_date = datetime.today()
        assert subscription.is_expired is False


class TestRenewSubscription:
    def test_when_is_trial_then_upgrade_to_regular(self):
        user_id = uuid4()
        plan_id = uuid4()
        subscription = Subscription.create_trial(user_id, plan_id)

        subscription.renew()

        assert subscription.is_trial is False
        assert (subscription.end_date.date() - date.today()).days == 30

    def test_when_is_regular_and_not_expired_then_extend_duration(self):
        user_id = uuid4()
        plan_id = uuid4()
        subscription = Subscription.create_regular(user_id, plan_id)
        previous_end_date = subscription.end_date

        subscription.renew()

        assert subscription.end_date > previous_end_date

    def test_when_is_regular_and_expired_then_extend_duration_starting_today(self):
        user_id = uuid4()
        plan_id = uuid4()
        subscription = Subscription.create_regular(user_id, plan_id)
        subscription.start_date = datetime.today() - relativedelta(days=31)
        subscription.end_date = datetime.today() - relativedelta(days=10)
        previous_start_date = subscription.start_date
        previous_end_date = subscription.end_date

        assert subscription.is_expired
        subscription.renew()

        assert subscription.start_date == previous_start_date
        assert (subscription.end_date - previous_end_date).days == 30

    def test_when_subscription_is_canceled_then_cannot_renew(self):
        user_id = uuid4()
        plan_id = uuid4()
        subscription = Subscription.create_regular(user_id, plan_id)
        subscription.cancel()

        try:
            subscription.renew()
        except ValueError as e:
            assert str(e) == "Cannot renew a cancelled subscription"
        else:
            assert False, "Should have raised an exception"


class TestConvertToTrial:
    def test_when_subscription_is_trial_then_raise_exception(self):
        subscription = Subscription.create_trial(user_id=uuid4(), plan_id=uuid4())

        try:
            subscription.convert_to_trial()
        except ValueError as e:
            assert str(e) == "Subscription is already a trial"
        else:
            assert False, "Should have raised an exception"

    def test_when_subscription_is_regular_then_convert_to_trial_with_7_days_duration(self):
        subscription = Subscription.create_regular(user_id=uuid4(), plan_id=uuid4())

        subscription.convert_to_trial()

        assert subscription.is_trial is True
        assert (subscription.end_date.date() - subscription.start_date.date()).days == 7
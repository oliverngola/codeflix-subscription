from dataclasses import Field
from datetime import datetime, date
from enum import StrEnum
from uuid import UUID

from dateutil.relativedelta import relativedelta

from src.domain.entity import Entity


class SubscriptionStatus(StrEnum):
    ACTIVE = 'ACTIVE'
    CANCELLED = 'CANCELLED'


class Subscription(Entity):
    user_id: UUID
    plan_id: UUID
    start_date: datetime
    end_date: datetime
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    is_trial: bool = False

    @classmethod
    def create_regular(cls, user_id: UUID, plan_id: UUID) -> "Subscription":
        now = datetime.now()
        subscription = cls(
            user_id=user_id,
            plan_id=plan_id,
            start_date=now,
            end_date=now + relativedelta(days=30),
            status=SubscriptionStatus.ACTIVE,
            is_active=True,
            is_trial=False,
        )
        return subscription

    @classmethod
    def create_trial(cls, user_id: UUID, plan_id: UUID) -> "Subscription":
        now = datetime.now()
        subscription = cls(
            user_id=user_id,
            plan_id=plan_id,
            start_date=now,
            end_date=now + relativedelta(days=7),
            status=SubscriptionStatus.ACTIVE,
            is_active=True,
            is_trial=True,
        )
        return subscription

    def renew(self) -> None:
        if self.is_canceled:
            raise ValueError("Cannot renew a cancelled subscription")

        if self.is_trial:
            self._upgrade()
        else:
            self._extend()

    def convert_to_trial(self) -> None:
        if self.is_trial:
            raise ValueError("Subscription is already a trial")

        self.is_trial = True
        self.start_date = datetime.now()
        self.end_date = self.start_date + relativedelta(days=7)

    def _extend(self):
        self.end_date += relativedelta(days=30)

    def _upgrade(self) -> None:
        if not self.is_trial:
            raise ValueError("Only trial subscriptions can be upgraded")

        self.is_trial = False
        self.start_date = datetime.now()
        self.end_date = self.start_date + relativedelta(days=30)

    def cancel(self):
        self.status = SubscriptionStatus.CANCELLED

    @property
    def is_expired(self):
        return self.end_date.date() < date.today()

    @property
    def is_canceled(self):
        return self.status == SubscriptionStatus.CANCELLED

    @property
    def is_active(self):
        return self.status == SubscriptionStatus.ACTIVE
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.plan import Plan
from src.domain.subscription import Subscription
from src.domain.user_account import UserAccount


class PlanRepository(ABC):
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Plan]:
        pass

    @abstractmethod
    def find_by_id(self, plan_id: UUID) -> Optional[Plan]:
        pass

    @abstractmethod
    def save(self, plan: Plan) -> None:
        pass


class UserAccountRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: UUID) -> Optional[UserAccount]:
        pass

    @abstractmethod
    def save(self, user_account: UserAccount) -> None:
        pass


class SubscriptionRepository(ABC):
    @abstractmethod
    def find_by_id(self, subscription_id: UUID) -> Optional[Subscription]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: UUID) -> Optional[Subscription]:
        pass

    @abstractmethod
    def save(self, subscription: Subscription) -> None:
        pass
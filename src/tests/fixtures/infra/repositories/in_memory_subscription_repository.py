from src.domain.repositories import SubscriptionRepository
from src.domain.subscription import Subscription


class InMemorySubscriptionRepository(SubscriptionRepository):
    def __init__(self, subscriptions: list[Subscription] = None) -> None:
        self.subscriptions = subscriptions or []

    def save(self, subscription: Subscription) -> None:
        self.subscriptions.append(subscription)

    def find_by_id(self, subscription_id) -> Subscription | None:
        for subscription in self.subscriptions:
            if subscription.id == subscription_id:
                return subscription
        return None

    def find_by_user_id(self, user_id) -> Subscription | None:
        for subscription in self.subscriptions:
            if subscription.user_id == user_id:
                return subscription
        return None
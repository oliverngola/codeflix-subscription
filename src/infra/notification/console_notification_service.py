from typing import Optional

from src.infra.notification.notification_service import NotificationService


class ConsoleNotificationService(NotificationService):
    """A simple notification service that just prints to console"""

    def notify(self, message: str, recipient: Optional[str] = None) -> None:
        recipient_info = f" to {recipient}" if recipient else ""
        print(f"NOTIFICATION{recipient_info}: {message}")

from abc import ABC, abstractmethod


class NotificationService(ABC):
    @abstractmethod
    def notify(self, message: str, recipient: str = None) -> None:
        """
        Send a notification with the given message

        Args:
            message: The notification message
            recipient: Optional recipient identifier (email, phone, etc.)
        """
        pass

import logging
from dataclasses import dataclass
from typing import Optional

from pydantic_settings import BaseSettings

from src.infra.notification.notification_service import NotificationService


class EmailSettings(BaseSettings):
    smtp_server: str = "smtp.example.com"
    smtp_port: int = 587
    smtp_username: str = "username"
    smtp_password: str = "password"
    sender_email: str = "noreply@subscriptionservice.com"

    class Config:
        env_prefix = "EMAIL_"


@dataclass
class EmailNotification:
    recipient: str
    subject: str
    body: str
    sent_at: Optional[str] = None
    status: str = "PENDING"


class EmailNotificationService(NotificationService):
    def __init__(self, settings: Optional[EmailSettings] = None):
        self.settings = settings or EmailSettings()
        self.logger = logging.getLogger(__name__)
        self.notifications: list[EmailNotification] = []

    def notify(self, message: str, recipient: Optional[str] = None) -> None:
        """
        Send an email notification

        Args:
            message: The notification message
            recipient: Email address to send to (if None, will use default from settings)
        """
        if not recipient:
            self.logger.warning("No recipient provided for notification, skipping")
            return

        notification = EmailNotification(
            recipient=recipient,
            subject="Subscription Service Notification",
            body=message,
        )

        try:
            self._send_email(notification)
            notification.status = "SENT"
        except Exception as e:
            self.logger.error(f"Failed to send email notification: {e}")
            notification.status = "FAILED"

        self.notifications.append(notification)

    def _send_email(self, notification: EmailNotification) -> None:
        """
        Send an email via SMTP

        In production, you would implement actual SMTP sending.
        This implementation just logs the message.
        """
        self.logger.info(
            f"NOTIFICATION - To: {notification.recipient}, Subject: {notification.subject}, "
            f"Message: {notification.body}"
        )

        # In a real implementation, you would do something like:
        """
        msg = EmailMessage()
        msg['Subject'] = notification.subject
        msg['From'] = self.settings.sender_email
        msg['To'] = notification.recipient
        msg.set_content(notification.body)

        with smtplib.SMTP(self.settings.smtp_server, self.settings.smtp_port) as server:
            server.starttls()
            server.login(self.settings.smtp_username, self.settings.smtp_password)
            server.send_message(msg)
        """

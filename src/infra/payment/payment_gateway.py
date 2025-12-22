import uuid
from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.user_account import Address


class Payment(BaseModel):
    success: bool
    transaction_id: UUID = Field(default_factory=uuid.uuid4)


class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, payment_token: str, billing_address: Address) -> Payment:
        pass
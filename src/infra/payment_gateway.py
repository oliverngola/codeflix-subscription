from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.domain.user_account import Address


class Payment(BaseModel):
    success: bool
    # transaction_id: str


class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, payment_token: str, billing_address: Address) -> Payment:
        pass
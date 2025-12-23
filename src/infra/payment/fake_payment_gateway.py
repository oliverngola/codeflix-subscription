import uuid
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel

from src.domain.user_account import Address
from src.infra.payment.payment_gateway import Payment, PaymentGateway


class PaymentMethod(StrEnum):
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    PIX = "PIX"


class PaymentStatus(StrEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class PaymentDetails(BaseModel):
    transaction_id: str
    success: bool
    amount: Decimal
    currency: str
    created_at: datetime
    status: PaymentStatus
    payment_method: PaymentMethod


class FakePaymentGateway(PaymentGateway):
    def __init__(self, success: bool = True):
        self.success = success
        self.payments: dict[str, PaymentDetails] = {}

    def process_payment(self, payment_token: str, billing_address: Address) -> Payment:
        # TODO: pass Plan to fetch price (amount/currency)
        transaction_id = str(uuid.uuid4())
        # Store payment details
        payment_details = PaymentDetails(
            transaction_id=transaction_id,
            success=self.success,
            amount=Decimal("99.99"),
            currency="BRL",
            status=PaymentStatus.COMPLETED if self.success else PaymentStatus.FAILED,
            payment_method=PaymentMethod.CREDIT_CARD,
            created_at=datetime.now(),
        )
        # Could be stored in a database or any other storage
        self.payments[transaction_id] = payment_details

        return Payment(
            success=self.success,
            transaction_id=transaction_id,
        )

    def get_payment_details(self, transaction_id: str) -> Optional[PaymentDetails]:
        return self.payments.get(transaction_id)

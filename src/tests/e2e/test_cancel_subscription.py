from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.infra.api.dependencies import get_payment_gateway
from src.infra.api.fastapi import app
from src.infra.db.repositories.sql_model_subscription_repository import (
    SQLModelSubscriptionRepository,
)
from src.infra.payment.fake_payment_gateway import FakePaymentGateway


@pytest.fixture
def account_payload() -> dict:
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepassword",
        "billing_address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip_code": "12345",
            "country": "USA",
        },
    }


@pytest.fixture
def plan_payload() -> dict:
    return {
        "name": "Premium Plan",
        "price": {
            "amount": "19.99",
            "currency": "BRL",
        },
    }


@pytest.fixture
def user_id(client: TestClient, account_payload: dict) -> str:
    response = client.post("/accounts/", json=account_payload)
    assert response.status_code == 201
    return response.json()["user_id"]


@pytest.fixture
def plan_id(client: TestClient, plan_payload: dict) -> str:
    response = client.post("/plans/", json=plan_payload)
    assert response.status_code == 201
    return response.json()["id"]


@pytest.fixture
def subscription_payload(user_id: str, plan_id: str) -> dict:
    return {
        "user_id": user_id,
        "plan_id": plan_id,
        "payment_token": "secure-token-123",
    }


@pytest.fixture
def subscription_id(client: TestClient, subscription_payload: dict) -> str:
    response = client.post("/subscriptions/", json=subscription_payload)
    assert response.status_code == 201
    return response.json()["subscription_id"]


def test_cancel_subscription_success(
    client: TestClient,
    subscription_id: str,
    session: Session,
) -> None:
    # Cancel the subscription
    cancel_response = client.delete(f"/subscriptions/{subscription_id}/")
    assert cancel_response.status_code == 200

    # Verify that the subscription is marked as canceled in the repository
    subscription = SQLModelSubscriptionRepository(session).find_by_id(
        UUID(subscription_id)
    )
    assert subscription is not None
    assert subscription.is_canceled


def test_cancel_subscription_not_found(client: TestClient) -> None:
    non_existent_subscription_id = str(uuid4())
    response = client.delete(f"/subscriptions/{non_existent_subscription_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Subscription with ID {non_existent_subscription_id} not found"
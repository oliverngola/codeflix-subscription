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


def test_subscribe_to_plan_success(
    client: TestClient,
    user_id: str,
    plan_id: str,
    subscription_payload: dict,
    session: Session,
) -> None:
    response = client.post("/subscriptions/", json=subscription_payload)

    assert response.status_code == 201
    data = response.json()
    assert "subscription_id" in data
    subscription = SQLModelSubscriptionRepository(session).find_by_id(
        UUID(data["subscription_id"])
    )
    assert subscription is not None
    assert not subscription.is_trial


def test_when_payment_fails_then_create_trial_subscription(
    user_id: str,
    plan_id: str,
    subscription_payload: dict,
    client: TestClient,
    session: Session,
) -> None:
    app.dependency_overrides[get_payment_gateway] = lambda: FakePaymentGateway(
        success=False
    )

    response = client.post("/subscriptions/", json=subscription_payload)

    assert response.status_code == 201
    data = response.json()
    assert "subscription_id" in data
    subscription = SQLModelSubscriptionRepository(session).find_by_id(
        UUID(data["subscription_id"])
    )
    assert subscription is not None
    assert subscription.is_trial


def test_subscribe_to_plan_user_not_found(
    client: TestClient,
    plan_id: str,
    subscription_payload: dict,
) -> None:
    # Modify the user_id to a non-existent one
    subscription_payload["user_id"] = str(uuid4())

    response = client.post("/subscriptions/", json=subscription_payload)

    assert response.status_code == 404
    assert "Could not find user" in response.json()["detail"]


def test_subscribe_to_plan_duplicate_subscription(
    client: TestClient,
    user_id: str,
    plan_id: str,
    subscription_payload: dict,
) -> None:
    # First subscription
    response = client.post("/subscriptions/", json=subscription_payload)
    assert response.status_code == 201

    # Attempt to create a duplicate subscription
    response = client.post("/subscriptions/", json=subscription_payload)
    assert response.status_code == 409
    assert "User already has active subscription" in response.json()["detail"]

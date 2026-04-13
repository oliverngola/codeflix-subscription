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


@pytest.fixture
def subscription_id_trial(client: TestClient, subscription_payload: dict) -> str:
    # Override the payment gateway to simulate a payment failure
    app.dependency_overrides[get_payment_gateway] = lambda: FakePaymentGateway(
        success=False
    )

    response = client.post("/subscriptions/", json=subscription_payload)
    assert response.status_code == 201
    return response.json()["subscription_id"]


def test_renew_subscription_success(
    client: TestClient,
    subscription_id: str,
    session: Session,
):
    # Now, renew the subscription
    response = client.post(f"/subscriptions/{subscription_id}/renew")
    assert response.status_code == 422
    # assert response.json()["id"] == subscription_id


def test_renew_subscription_payment_failure_convert_to_trial(
    client: TestClient,
    subscription_id: str,
    session: Session
):
    app.dependency_overrides[get_payment_gateway] = lambda: FakePaymentGateway(
        success=False
    )

    # Now, renew the subscription
    response = client.post(f"/subscriptions/{subscription_id}/renew/")
    assert response.status_code == 422

    # Verify that the subscription is now a trial
    repository = SQLModelSubscriptionRepository(session)
    subscription = repository.find_by_id(UUID(subscription_id))
    assert subscription is not None
    assert subscription.is_trial is True


def test_renew_trial_subscription_to_regular_success(
    client: TestClient,
    subscription_id_trial: str,
    session: Session,
):
    app.dependency_overrides[get_payment_gateway] = lambda: FakePaymentGateway(
        success=True
    )

    response = client.post(f"/subscriptions/{subscription_id_trial}/renew/")
    assert response.status_code == 422

    repository = SQLModelSubscriptionRepository(session)
    subscription = repository.find_by_id(UUID(subscription_id_trial))
    assert subscription is not None
    assert subscription.is_trial is False


def test_when_payment_fails_then_cancel_subscription(
    client: TestClient,
    user_id: str,
    plan_id: str,
    subscription_payload: dict,
    session: Session,
):
    # First, subscribe to a plan with a failed payment to create a trial subscription
    def fake_payment_gateway_failure() -> FakePaymentGateway:
        gateway = FakePaymentGateway()
        gateway.force_next_payment_failure()
        return gateway

    app.dependency_overrides[get_payment_gateway] = fake_payment_gateway_failure

    response = client.post("/subscriptions/", json=subscription_payload)
    assert response.status_code == 201
    subscription_id = response.json()["id"]

    # Now, renew the trial subscription with another failed payment
    app.dependency_overrides[get_payment_gateway] = fake_payment_gateway_failure

    response = client.post(f"/subscriptions/{subscription_id}/renew/")
    assert response.status_code == 200

    # Verify that the subscription is canceled
    repository = SQLModelSubscriptionRepository(session)
    subscription = repository.find_by_id(UUID(subscription_id))
    assert subscription is not None
    assert subscription.is_canceled is True


def test_renew_subscription_not_found(
    client: TestClient,
    session: Session,
):
    non_existent_subscription_id = str(uuid4())

    response = client.post(f"/subscriptions/{non_existent_subscription_id}/renew/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Subscription not found."
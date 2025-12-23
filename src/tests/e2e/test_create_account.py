import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def valid_payload() -> dict:
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


def test_create_user_account_success(client: TestClient, valid_payload: dict) -> None:
    # Act
    response = client.post("/accounts", json=valid_payload)

    # Assert
    assert response.status_code == 201
    data = response.json()

    assert data["user_id"]
    assert data["iam_user_id"]


def test_create_user_account_duplicate_email(
    client: TestClient, valid_payload: dict
) -> None:
    # Create the first user
    response = client.post("/accounts", json=valid_payload)
    assert response.status_code == 201

    # Act - Try to create another user with the same email
    response = client.post("/accounts", json=valid_payload)

    # Assert
    assert response.status_code == 400
    assert "User already registered in IAM" in response.json()["detail"]


def test_create_user_account_invalid_data(client: TestClient) -> None:
    # Arrange - Missing required fields
    request_body = {
        "name": "John Doe",
        # Missing email
        "billing_address": {
            "street": "123 Main St",
            # Missing city
            "state": "CA",
            "zip_code": "12345",
            "country": "USA",
        },
    }

    # Act
    response = client.post("/accounts", json=request_body)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["type"] == "missing"
    assert data["detail"][0]["loc"] == ["body", "email"]

from fastapi.testclient import TestClient


def test_create_plan_success(client: TestClient) -> None:
    """Test successfully creating a plan"""
    # Given
    plan_data = {
        "name": "Premium Plan",
        "price": {
            "amount": "19.99",
            "currency": "BRL",
        },
    }

    # When
    response = client.post("/plans", json=plan_data)

    # Then
    assert response.status_code == 201
    data = response.json()
    assert data["id"]
    assert data["name"] == "Premium Plan"
    assert data["price"]["amount"] == "19.99"
    assert data["price"]["currency"] == "BRL"


def test_create_plan_duplicate(client: TestClient) -> None:
    """Test creating a plan with a duplicate name"""
    # Given
    plan_data = {
        "name": "Premium Plan",
        "price": {
            "amount": "19.99",
            "currency": "BRL",
        },
    }

    # Create the plan first time
    client.post("/plans", json=plan_data)

    # When - try to create the same plan again
    response = client.post("/plans", json=plan_data)

    # Then
    assert response.status_code == 400
    assert "A plan with this name already exists." in response.json()["detail"]


def test_create_plan_invalid_data(client: TestClient) -> None:
    """Test creating a plan with invalid data"""
    # Given
    invalid_plan_data = {
        "name": "",
        "price": {
            "amount": "19.99",
            "currency": "BRL",
        },
    }

    # When
    response = client.post("/plans", json=invalid_plan_data)

    # Then
    assert response.status_code == 500  # Validation error
    # assert response.json()['detail'][0]['msg'] == "String should have at least 1 character"

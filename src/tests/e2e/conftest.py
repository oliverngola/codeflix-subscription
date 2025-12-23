import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from src.infra.api.dependencies import get_auth_service
from src.infra.api.fastapi import app
from src.infra.auth.in_memory_auth_service import InMemoryAuthService
from src.infra.db import get_session


@pytest.fixture(scope="function")
def session():
    engine = create_engine(
        "sqlite:///:memory:",  # In-memory database for testing
        connect_args={"check_same_thread": False},  # Access db from multiple threads
        poolclass=StaticPool,  # Use same in-memory db object from different threads
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def auth_service():
    return InMemoryAuthService()


@pytest.fixture
def client(session, auth_service):
    def get_session_override():
        return session

    def get_auth_service_override():
        return auth_service

    app.dependency_overrides[get_auth_service] = get_auth_service_override
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

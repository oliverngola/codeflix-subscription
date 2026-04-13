import os

from sqlmodel import Session, SQLModel, create_engine

from .repositories.sql_model_plan_repository import SQLModelPlanRepository
from .repositories.sql_model_user_account_repository import SQLModelUserAccountRepository
from .repositories.sql_model_subscription_repository import SQLModelSubscriptionRepository

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./subscription_service.db")
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


__all__ = [
    "SQLModelPlanRepository",
    "SQLModelUserAccountRepository",
    'SQLModelSubscriptionRepository',
    "create_db_and_tables",
    "get_session",
]

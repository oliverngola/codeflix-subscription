from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from src.domain.repositories import UserAccountRepository
from src.domain.user_account import UserAccount
from src.infra.db.models.user_account_model import UserAccountModel


class SQLModelUserAccountRepository(UserAccountRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, user_id: UUID) -> Optional[UserAccount]:
        statement = select(UserAccountModel).where(UserAccountModel.id == user_id)
        result = self.session.exec(statement).first()
        return result.to_entity() if result else None

    def find_by_email(self, email: str) -> Optional[UserAccount]:
        statement = select(UserAccountModel).where(UserAccountModel.email == email)
        result = self.session.exec(statement).first()
        return result.to_entity() if result else None

    def save(self, user_account: UserAccount) -> None:
        model = UserAccountModel.from_entity(user_account)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

from src.domain.repositories import UserAccountRepository
from src.domain.user_account import UserAccount


class InMemoryAuthService(UserAccountRepository):
    def __init__(self, users: list[UserAccount] | None = None):
        self.users = users or []

    def find_by_email(self, email: str) -> str | None:
        for user in self.users:
            if user == email:
                return user
        return None

    def create_user(self, email: str, _: str) -> str:
        self.users.append(email)
        return "abcdef"
from src.domain.user_account import UserAccount


class InMemoryUserAccountRepository:
    def __init__(self, user_accounts: list[UserAccount] = None) -> None:
        self.user_accounts = user_accounts or []

    def save(self, user_account: UserAccount) -> None:
        self.user_accounts.append(user_account)

    def find_by_id(self, user_id) -> UserAccount:
        for user_account in self.user_accounts:
            if user_account.id == user_id:
                return user_account
        return None
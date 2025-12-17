class InMemoryAuthService:
    def __init__(self, users: list[str] | None = None):
        self.users = users or []

    def find_by_email(self, email: str) -> str | None:
        for user in self.users:
            if user == email:
                return user
        return None

    def create_user(self, email: str, _: str) -> str:
        self.users.append(email)
        return "abcdef"
from abc import ABC, abstractmethod


class AuthService(ABC):

    @abstractmethod
    def find_by_email(self, email: str) -> str | None:
        pass

    @abstractmethod
    def create_user(self, email: str, password: str) -> str:  # IAM ID
        pass

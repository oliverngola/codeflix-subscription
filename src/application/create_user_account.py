from uuid import UUID

from pydantic import BaseModel, EmailStr, SecretStr

from src.application.exceptions import UserAlreadyExistsError
from src.domain.user_account import Address, UserAccount
from src.infra.auth_service import AuthService


class CreateUserAccountInput(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr
    billing_address: Address


class CreateUserAccountOutput(BaseModel):
    user_id: UUID
    iam_user_id: str


class CreateUserAccountUseCase:
    def __init__(self, auth_service: AuthService, user_repository):
        self._auth_service = auth_service
        self._user_repo = user_repository

    def execute(self, input: CreateUserAccountInput):
        iam_user = self._auth_service.find_by_email(input.email)
        if iam_user:
            raise UserAlreadyExistsError(f"User already registered IAM")

        iam_user_id = self._auth_service.create_user(
            email=input.email,
            password=input.password.get_secret_value(),
        )

        user_account = UserAccount(
            iam_user_id=iam_user_id,
            name=input.name,
            email=input.email,
            billing_address=input.billing_address,
        )
        self._user_repo.save(user_account)

        return CreateUserAccountOutput(user_id=user_account.id, iam_user_id=iam_user_id)
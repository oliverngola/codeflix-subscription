from unittest.mock import create_autospec

import pytest

from src.application.create_user_account import CreateUserAccountUseCase, CreateUserAccountInput
from src.application.exceptions import UserAlreadyExistsError
from src.domain.user_account import Address
from src.infra.auth_service import AuthService
from src.infra.in_memory_user_account_repository import InMemoryUserAccountRepository

account_input = CreateUserAccountInput(  # pytest.fixture
    name="John Doe",
    email="john@codeflix.com",
    password="123456",
    billing_address=Address(
        street="Main Street",
        city="Springfield",
        state="IL",
        zip_code="62701",
        country="USA",
    )
)


class TestCreatePlan:
    def test_when_email_is_registered_in_auth_service_then_raise_error(self):
        mock_auth_service = create_autospec(AuthService)
        mock_auth_service.find_by_email.return_value = "abcdef"

        use_case = CreateUserAccountUseCase(
            auth_service=mock_auth_service,
            user_repository=None,
        )

        with pytest.raises(UserAlreadyExistsError):
            use_case.execute(input=account_input)

    def test_create_user_account_with_iam_id(self):
        mock_auth_service = create_autospec(AuthService)
        mock_auth_service.find_by_email.return_value = None
        mock_auth_service.create_user.return_value = "iamid_123"
        user_account_repo = InMemoryUserAccountRepository()

        use_case = CreateUserAccountUseCase(
            auth_service=mock_auth_service,
            user_repository=user_account_repo,
        )

        output = use_case.execute(input=account_input)

        assert output.user_id is not None
        assert output.iam_user_id == "iamid_123"

        assert len(user_account_repo.user_accounts) == 1
        mock_auth_service.create_user.assert_called_once_with(
            email=account_input.email,
            password=account_input.password.get_secret_value(),
        )
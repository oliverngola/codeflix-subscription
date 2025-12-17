from src.domain.user_account import UserAccount, Address


def test_create_valid_user_account():
    user_account = UserAccount(
        iam_user_id='123456789012',
        name='test-user',
        email='test@user.com',
        billing_address=Address(
            street='123 Main St',
            city='Anytown',
            state='NY',
            zip_code='12345',
            country='BRL'
        )
    )

    assert user_account.id is not None
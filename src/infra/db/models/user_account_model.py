from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel

from src.domain.user_account import Address, UserAccount


class UserAccountModel(SQLModel, table=True):
    __tablename__ = "user_accounts"

    id: UUID = Field(primary_key=True)
    iam_user_id: str = Field(unique=True)
    name: str
    email: str = Field(unique=True)
    billing_address_street: str = Field()
    billing_address_city: str = Field()
    billing_address_state: str = Field()
    billing_address_zip_code: str = Field()
    billing_address_country: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)

    @classmethod
    def from_entity(cls, user: UserAccount) -> "UserAccountModel":
        return cls(
            id=user.id,
            iam_user_id=user.iam_user_id,
            name=user.name,
            email=user.email,
            billing_address_street=user.billing_address.street,
            billing_address_city=user.billing_address.city,
            billing_address_state=user.billing_address.state,
            billing_address_zip_code=user.billing_address.zip_code,
            billing_address_country=user.billing_address.country,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
        )

    def to_entity(self) -> UserAccount:
        address = Address(
            street=self.billing_address_street,
            city=self.billing_address_city,
            state=self.billing_address_state,
            zip_code=self.billing_address_zip_code,
            country=self.billing_address_country,
        )

        return UserAccount(
            id=self.id,
            iam_user_id=self.iam_user_id,
            name=self.name,
            email=self.email,
            billing_address=address,
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_active=self.is_active,
        )

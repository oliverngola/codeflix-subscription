from pydantic import EmailStr

from src.domain.entity import Entity
from src.domain.value_objects import ValueObject


class Address(ValueObject):
    street: str
    city: str
    state: str
    zip_code: str
    country: str


class UserAccount(Entity):
    iam_user_id: str
    name: str
    email: EmailStr
    billing_address: Address
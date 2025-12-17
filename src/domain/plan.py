from src.domain.entity import Entity
from src.domain.value_objects import MonetaryValue


class Plan(Entity):
    name: str
    price: MonetaryValue
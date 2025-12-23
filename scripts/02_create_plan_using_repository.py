from src.domain.plan import Plan
from src.domain.value_objects import MonetaryValue
from src.infra.db import get_session
from src.infra.db.repositories import SQLModelPlanRepository

plan = Plan(name="Standard", price=MonetaryValue(amount=10, currency="BRL"))
repo = SQLModelPlanRepository(get_session())
repo.save(plan)
repo.find_by_name("Standard")
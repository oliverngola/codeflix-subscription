from src.domain.plan import Plan
from src.domain.value_objects import MonetaryValue
from src.infra.db import create_db_and_tables, get_session
from src.infra.db.models.plan_model import PlanModel

plan = Plan(name="Standard", price=MonetaryValue(amount=10, currency="BRL"))
model = PlanModel.from_entity(plan)

create_db_and_tables()
session = get_session()
session.add(model)
session.commit()


"""
sqlite3 subscription_service.db
.tables
select * from plans;
delete from plans where name = 'Standard';
drop plans;
"""
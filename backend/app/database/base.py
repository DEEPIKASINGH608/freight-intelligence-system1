from sqlalchemy.orm import declarative_base


Base = declarative_base()


from app.database.session import Base
from app.models.vessel import Vessel
from app.models.route import Route
from app.models.freight_rate import FreightRate
from app.models.decision import DecisionHistory



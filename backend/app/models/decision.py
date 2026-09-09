# Import Base and all ORM models here so Alembic or Base.metadata.create_all recognizes them
from app.database.session import Base
from app.models.vessel import Vessel
from app.models.route import Route
from app.models.freight_rate import FreightRate
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.sql import func
from app.database.session import Base

class DecisionHistory(Base):
    __tablename__ = "decision_history"

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    cargo_type = Column(String(50), nullable=False)
    cargo_quantity_tons = Column(Float, nullable=False)
    recommended_action = Column(String(50), nullable=False) # e.g., "CHARTER NOW", "WAIT"
    expected_freight_rate = Column(Float, nullable=False)
    selected_vessels = Column(JSON, nullable=False)          # List of vessel names and capacities
    total_estimated_cost_inr_cr = Column(Float, nullable=False)
    estimated_savings_inr_cr = Column(Float, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    reasoning = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
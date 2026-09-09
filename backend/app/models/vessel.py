from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.database.session import Base

class Vessel(Base):
    __tablename__ = "vessels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    vessel_type = Column(String(50), nullable=False, default="Capesize") # Capesize, Panamax, Supramax
    capacity_dwt = Column(Float, nullable=False)                         # Deadweight Tonnage (tons)
    daily_charter_rate = Column(Float, nullable=False)                  # Daily rental cost ($/day)
    fuel_consumption_ton_day = Column(Float, nullable=False)            # Fuel burn rate (tons/day)
    speed_knots = Column(Float, nullable=False, default=14.0)           # Average speed
    current_port = Column(String(100), nullable=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.sql import func
from app.database.session import Base

class FreightRate(Base):
    __tablename__ = "freight_rates"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    route_id = Column(Integer, nullable=False, index=True)
    origin = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    cargo_type = Column(String(50), nullable=False)      # e.g., Iron Ore, Coal, Grain
    freight_rate_usd_per_ton = Column(Float, nullable=False) # Target variable ($/ton)
    bunker_fuel_price_usd = Column(Float, nullable=False)    # Fuel cost ($/ton VLSFO)
    cargo_demand_index = Column(Float, nullable=False)       # 50 - 150 scale
    vessel_availability_index = Column(Float, nullable=False)# 50 - 150 scale
    port_congestion_days = Column(Float, nullable=False)     # Average waiting time
    created_at = Column(DateTime(timezone=True), server_default=func.now())
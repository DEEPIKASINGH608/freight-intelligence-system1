from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database.session import Base

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    origin_port = Column(String(100), nullable=False)
    destination_port = Column(String(100), nullable=False)
    distance_nautical_miles = Column(Float, nullable=False)
    average_transit_days = Column(Float, nullable=False)
    port_congestion_index = Column(Float, default=1.0) # Multiplier (1.0 = normal, 1.5 = high congestion)
    weather_risk_index = Column(Float, default=1.0)    # Multiplier for seasonal weather hazards
    created_at = Column(DateTime(timezone=True), server_default=func.now())
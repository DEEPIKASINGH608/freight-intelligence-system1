import sys
import os
import random
from datetime import datetime, timedelta

# Add backend directory to path so imports work cleanly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.database.session import engine, SessionLocal
from app.database.base import Base
from app.models.vessel import Vessel
from app.models.route import Route
from app.models.freight_rate import FreightRate

def seed_database():
    print("Creating database tables if they do not exist...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        if db.query(Vessel).count() > 0:
            print("Database already contains data. Skipping initial seeding.")
            return

        print("Seeding Vessel Fleet Data...")
        vessels = [
            Vessel(name="MV Ocean Titan", vessel_type="Capesize", capacity_dwt=120000, daily_charter_rate=28000, fuel_consumption_ton_day=42, speed_knots=14.0, current_port="Dhamra", is_available=True),
            Vessel(name="MV Maritime Pioneer", vessel_type="Capesize", capacity_dwt=100000, daily_charter_rate=24000, fuel_consumption_ton_day=38, speed_knots=13.5, current_port="Paradip", is_available=True),
            Vessel(name="MV Iron Express", vessel_type="Panamax", capacity_dwt=75000, daily_charter_rate=18500, fuel_consumption_ton_day=29, speed_knots=14.2, current_port="Visakhapatnam", is_available=True),
            Vessel(name="MV Bengal Star", vessel_type="Panamax", capacity_dwt=70000, daily_charter_rate=17000, fuel_consumption_ton_day=27, speed_knots=13.8, current_port="Chennai", is_available=True),
            Vessel(name="MV Eastern Carrier", vessel_type="Supramax", capacity_dwt=55000, daily_charter_rate=14000, fuel_consumption_ton_day=22, speed_knots=13.0, current_port="Haldia", is_available=True),
            Vessel(name="MV Global Shield", vessel_type="Capesize", capacity_dwt=110000, daily_charter_rate=26000, fuel_consumption_ton_day=40, speed_knots=14.1, current_port="Singapore", is_available=True),
            Vessel(name="MV Pacific Voyager", vessel_type="Panamax", capacity_dwt=65000, daily_charter_rate=16000, fuel_consumption_ton_day=25, speed_knots=13.2, current_port="Port Klang", is_available=True),
            Vessel(name="MV Southern Cross", vessel_type="Supramax", capacity_dwt=50000, daily_charter_rate=13000, fuel_consumption_ton_day=20, speed_knots=12.8, current_port="Mumbai", is_available=True),
        ]
        db.add_all(vessels)

        print("Seeding Maritime Routes Data...")
        routes = [
            Route(origin_port="Paradip, India", destination_port="Qingdao, China", distance_nautical_miles=3850, average_transit_days=11.5, port_congestion_index=1.3, weather_risk_index=1.1),
            Route(origin_port="Dhamra, India", destination_port="Rotterdam, Netherlands", distance_nautical_miles=6450, average_transit_days=19.2, port_congestion_index=1.1, weather_risk_index=1.2),
            Route(origin_port="Visakhapatnam, India", destination_port="Gwangyang, South Korea", distance_nautical_miles=4100, average_transit_days=12.2, port_congestion_index=1.2, weather_risk_index=1.0),
            Route(origin_port="Mormugao, India", destination_port="Chiba, Japan", distance_nautical_miles=4600, average_transit_days=13.8, port_congestion_index=1.4, weather_risk_index=1.3),
        ]
        db.add_all(routes)
        db.commit()

        print("Generating 2 years of daily historical freight rates for ML training...")
        start_date = datetime.now().date() - timedelta(days=730)
        freight_records = []

        base_rate = 38.0
        bunker_fuel = 620.0

        for i in range(730):
            current_date = start_date + timedelta(days=i)

            # Simulate realistic market fluctuations (random walk with seasonal trend)
            bunker_fuel += random.uniform(-4.0, 4.2)
            bunker_fuel = max(450.0, min(850.0, bunker_fuel))

            cargo_demand = 100 + random.uniform(-15, 15)
            vessel_avail = 100 + random.uniform(-15, 15)
            congestion = max(0.5, random.uniform(1.0, 5.5))

            # Freight rate formula with economic correlation + noise
            rate = base_rate + (bunker_fuel - 600) * 0.03 + (cargo_demand - vessel_avail) * 0.15 + congestion * 0.8 + random.uniform(-1.5, 1.5)
            rate = round(max(20.0, rate), 2)

            freight_records.append(
                FreightRate(
                    date=current_date,
                    route_id=1,
                    origin="Paradip, India",
                    destination="Qingdao, China",
                    cargo_type="Iron Ore",
                    freight_rate_usd_per_ton=rate,
                    bunker_fuel_price_usd=round(bunker_fuel, 2),
                    cargo_demand_index=round(cargo_demand, 1),
                    vessel_availability_index=round(vessel_avail, 1),
                    port_congestion_days=round(congestion, 1)
                )
            )

        db.add_all(freight_records)
        db.commit()
        print("Database Seeding Completed Successfully!")

    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()